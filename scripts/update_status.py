#!/usr/bin/env python3
"""
Linear Status Updater - Updates the status of a Linear issue

Usage:
    python update_status.py --issue-id "ISSUE-123" --status "done"

Options:
    --issue-id    Issue identifier (e.g., ENG-123) or UUID (required)
    --status      Target status: backlog, todo, in_progress, in_review, done, canceled
    --comment     Optional comment to add with the status change

Examples:
    python update_status.py --issue-id "ENG-123" --status "in_progress"
    python update_status.py --issue-id "ENG-123" --status "done" --comment "Completed implementation"
"""

import os
import sys
import argparse
import requests
from datetime import datetime

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY")
ENDPOINT = "https://api.linear.app/graphql"

# Status type mapping
STATUS_TYPES = {
    "backlog": "backlog",
    "triage": "triage",
    "todo": "unstarted",
    "in_progress": "started",
    "in_review": "started",
    "done": "completed",
    "canceled": "canceled",
    "cancelled": "canceled",
}

def execute_query(query, variables=None):
    """Execute GraphQL query against Linear API."""
    if not LINEAR_API_KEY:
        print("Error: LINEAR_API_KEY environment variable not set")
        sys.exit(1)

    headers = {
        "Authorization": LINEAR_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        ENDPOINT,
        json={"query": query, "variables": variables or {}},
        headers=headers
    )

    if response.status_code != 200:
        print(f"Error: API request failed with status {response.status_code}")
        print(response.text)
        sys.exit(1)

    return response.json()

def get_issue_info(identifier):
    """Get issue UUID and team ID from identifier."""
    # If it looks like a UUID, fetch directly
    if len(identifier) > 20 and identifier.count("-") >= 4:
        query = """
        query GetIssue($id: String!) {
          issue(id: $id) {
            id
            identifier
            title
            team {
              id
            }
            state {
              name
            }
          }
        }
        """
        result = execute_query(query, {"id": identifier})
        if result.get("data", {}).get("issue"):
            issue = result["data"]["issue"]
            return issue["id"], issue["team"]["id"], issue

    # Search by identifier pattern (e.g., ENG-123)
    if "-" in identifier:
        team_key, number = identifier.rsplit("-", 1)

        query = """
        query SearchIssue($filter: IssueFilter!) {
          issues(filter: $filter, first: 1) {
            nodes {
              id
              identifier
              title
              team {
                id
              }
              state {
                name
              }
            }
          }
        }
        """

        try:
            result = execute_query(query, {
                "filter": {
                    "team": {"key": {"eq": team_key.upper()}},
                    "number": {"eq": int(number)}
                }
            })

            issues = result.get("data", {}).get("issues", {}).get("nodes", [])
            if issues:
                issue = issues[0]
                return issue["id"], issue["team"]["id"], issue
        except ValueError:
            pass

    print(f"Error: Could not find issue with identifier '{identifier}'")
    sys.exit(1)

def get_state_id(team_id, status_name):
    """Get workflow state ID by name or type."""
    query = """
    query GetStates($teamId: String!) {
      workflowStates(filter: { team: { id: { eq: $teamId } } }) {
        nodes {
          id
          name
          type
        }
      }
    }
    """
    result = execute_query(query, {"teamId": team_id})

    states = result.get("data", {}).get("workflowStates", {}).get("nodes", [])

    # Get target type from mapping
    target_type = STATUS_TYPES.get(status_name.lower(), status_name.lower())

    # First try exact name match
    for state in states:
        if state["name"].lower() == status_name.lower():
            return state["id"], state["name"]

    # Then try type match
    for state in states:
        if state["type"].lower() == target_type:
            return state["id"], state["name"]

    # List available states
    print(f"Error: Could not find status '{status_name}'")
    print("Available states:")
    for state in states:
        print(f"  - {state['name']} ({state['type']})")
    sys.exit(1)

def update_status(args):
    """Update the status of a Linear issue."""
    issue_id, team_id, issue_info = get_issue_info(args.issue_id)
    state_id, state_name = get_state_id(team_id, args.status)

    query = """
    mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) {
        success
        issue {
          id
          identifier
          title
          state {
            name
          }
        }
      }
    }
    """

    result = execute_query(query, {
        "id": issue_id,
        "input": {"stateId": state_id}
    })

    if "errors" in result:
        print(f"Error: {result['errors']}")
        sys.exit(1)

    update_data = result.get("data", {}).get("issueUpdate", {})

    if not update_data.get("success"):
        print("Error: Failed to update issue status")
        sys.exit(1)

    issue = update_data["issue"]
    old_state = issue_info.get("state", {}).get("name", "Unknown")

    print(f"✅ Status updated successfully!")
    print(f"   Issue: {issue['identifier']} - {issue['title']}")
    print(f"   Status: {old_state} → {issue['state']['name']}")

    # Add comment if specified
    if args.comment:
        comment_query = """
        mutation CreateComment($input: CommentCreateInput!) {
          commentCreate(input: $input) {
            success
          }
        }
        """

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        status_emoji = "✅" if args.status.lower() == "done" else "📝"
        comment_body = f"**{status_emoji} 상태 변경** ({timestamp})\n\n{old_state} → {state_name}\n\n{args.comment}"

        execute_query(comment_query, {
            "input": {
                "issueId": issue_id,
                "body": comment_body
            }
        })
        print(f"   Comment added: {args.comment[:50]}...")

    return issue

def main():
    parser = argparse.ArgumentParser(description="Update Linear issue status")
    parser.add_argument("--issue-id", "-i", required=True,
                        help="Issue identifier (e.g., ENG-123) or UUID")
    parser.add_argument("--status", "-s", required=True,
                        help="Target status (backlog, todo, in_progress, in_review, done, canceled)")
    parser.add_argument("--comment", "-c",
                        help="Optional comment to add with the status change")

    args = parser.parse_args()
    update_status(args)

if __name__ == "__main__":
    main()
