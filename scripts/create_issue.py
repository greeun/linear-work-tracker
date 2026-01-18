#!/usr/bin/env python3
"""
Linear Issue Creator - Creates a new issue in Linear

Usage:
    python create_issue.py --title "Issue Title" --team "TEAM_KEY" [options]

Options:
    --title       Issue title (required)
    --team        Team key or ID (required)
    --description Issue description
    --priority    Priority (0=none, 1=urgent, 2=high, 3=medium, 4=low)
    --labels      Comma-separated label IDs
    --assignee    Assignee user ID
    --project     Project ID
    --status      Initial status (backlog, todo, in_progress)

Examples:
    python create_issue.py --title "New Feature" --team "ENG"
    python create_issue.py --title "Bug Fix" --team "ENG" --priority 1 --description "Fix login bug"
"""

import os
import sys
import argparse
import requests
from datetime import datetime

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY")
ENDPOINT = "https://api.linear.app/graphql"

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

def get_team_id(team_key):
    """Get team ID from team key."""
    query = """
    query GetTeam($key: String!) {
      teams(filter: { key: { eq: $key } }) {
        nodes {
          id
          name
          key
        }
      }
    }
    """
    result = execute_query(query, {"key": team_key})

    teams = result.get("data", {}).get("teams", {}).get("nodes", [])
    if not teams:
        # Try as ID directly
        return team_key

    return teams[0]["id"]

def get_state_id(team_id, state_name):
    """Get workflow state ID by name."""
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

    state_map = {
        "backlog": "backlog",
        "todo": "unstarted",
        "in_progress": "started",
        "in_review": "started",
        "done": "completed"
    }

    target_type = state_map.get(state_name.lower(), state_name.lower())

    for state in states:
        if state["type"].lower() == target_type or state["name"].lower() == state_name.lower():
            return state["id"]

    return None

def create_issue(args):
    """Create a new Linear issue."""
    team_id = get_team_id(args.team)

    # Build input
    input_data = {
        "teamId": team_id,
        "title": args.title,
    }

    if args.description:
        input_data["description"] = args.description

    if args.priority is not None:
        input_data["priority"] = args.priority

    if args.labels:
        input_data["labelIds"] = [l.strip() for l in args.labels.split(",")]

    if args.assignee:
        input_data["assigneeId"] = args.assignee

    if args.project:
        input_data["projectId"] = args.project

    if args.status:
        state_id = get_state_id(team_id, args.status)
        if state_id:
            input_data["stateId"] = state_id

    query = """
    mutation CreateIssue($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        success
        issue {
          id
          identifier
          title
          url
          state {
            name
          }
        }
      }
    }
    """

    result = execute_query(query, {"input": input_data})

    if "errors" in result:
        print(f"Error: {result['errors']}")
        sys.exit(1)

    issue_data = result.get("data", {}).get("issueCreate", {})

    if not issue_data.get("success"):
        print("Error: Failed to create issue")
        sys.exit(1)

    issue = issue_data["issue"]
    print(f"✅ Issue created successfully!")
    print(f"   ID: {issue['identifier']}")
    print(f"   Title: {issue['title']}")
    print(f"   Status: {issue['state']['name']}")
    print(f"   URL: {issue['url']}")

    return issue

def main():
    parser = argparse.ArgumentParser(description="Create a Linear issue")
    parser.add_argument("--title", "-t", required=True, help="Issue title")
    parser.add_argument("--team", "-T", required=True, help="Team key or ID")
    parser.add_argument("--description", "-d", help="Issue description")
    parser.add_argument("--priority", "-p", type=int, choices=[0, 1, 2, 3, 4],
                        help="Priority (0=none, 1=urgent, 2=high, 3=medium, 4=low)")
    parser.add_argument("--labels", "-l", help="Comma-separated label IDs")
    parser.add_argument("--assignee", "-a", help="Assignee user ID")
    parser.add_argument("--project", "-P", help="Project ID")
    parser.add_argument("--status", "-s", help="Initial status (backlog, todo, in_progress)")

    args = parser.parse_args()
    create_issue(args)

if __name__ == "__main__":
    main()
