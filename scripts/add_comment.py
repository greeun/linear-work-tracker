#!/usr/bin/env python3
"""
Linear Comment Adder - Adds a comment to an existing Linear issue

Usage:
    python add_comment.py --issue-id "ISSUE-123" --body "Comment text"

Options:
    --issue-id    Issue identifier (e.g., ENG-123) or UUID (required)
    --body        Comment body text (required)
    --type        Comment type: progress, start, complete, analysis, fix, delete, warning

Examples:
    python add_comment.py --issue-id "ENG-123" --body "Started working on this"
    python add_comment.py --issue-id "ENG-123" --body "Fixed the bug" --type complete
"""

import os
import sys
import argparse
import requests
from datetime import datetime

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY")
ENDPOINT = "https://api.linear.app/graphql"

# Comment type prefixes
COMMENT_PREFIXES = {
    "start": "🚀 작업 시작",
    "progress": "📝 진행상황 업데이트",
    "complete": "✅ 작업 완료",
    "analysis": "🔍 분석/조사",
    "fix": "🔧 수정/수리",
    "delete": "🗑️ 삭제",
    "warning": "⚠️ 주의사항",
    "refactor": "🔄 리팩토링",
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

def get_issue_uuid(identifier):
    """Get issue UUID from identifier (e.g., ENG-123)."""
    # If it looks like a UUID, return as is
    if len(identifier) > 20 and "-" in identifier:
        return identifier

    query = """
    query GetIssue($identifier: String!) {
      issue(id: $identifier) {
        id
        identifier
        title
      }
    }
    """

    # Try as identifier first
    result = execute_query(query, {"identifier": identifier})

    if "errors" not in result and result.get("data", {}).get("issue"):
        return result["data"]["issue"]["id"]

    # Search by identifier pattern
    query = """
    query SearchIssue($filter: IssueFilter!) {
      issues(filter: $filter, first: 1) {
        nodes {
          id
          identifier
          title
        }
      }
    }
    """

    # Parse identifier (e.g., ENG-123)
    if "-" in identifier:
        team_key, number = identifier.rsplit("-", 1)
        result = execute_query(query, {
            "filter": {
                "team": {"key": {"eq": team_key}},
                "number": {"eq": int(number)}
            }
        })

        issues = result.get("data", {}).get("issues", {}).get("nodes", [])
        if issues:
            return issues[0]["id"]

    print(f"Error: Could not find issue with identifier '{identifier}'")
    sys.exit(1)

def add_comment(args):
    """Add a comment to a Linear issue."""
    issue_id = get_issue_uuid(args.issue_id)

    # Format body with type prefix if specified
    body = args.body
    if args.type and args.type in COMMENT_PREFIXES:
        prefix = COMMENT_PREFIXES[args.type]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        body = f"**{prefix}** ({timestamp})\n\n{args.body}"

    query = """
    mutation CreateComment($input: CommentCreateInput!) {
      commentCreate(input: $input) {
        success
        comment {
          id
          body
          createdAt
          issue {
            identifier
            title
          }
        }
      }
    }
    """

    result = execute_query(query, {
        "input": {
            "issueId": issue_id,
            "body": body
        }
    })

    if "errors" in result:
        print(f"Error: {result['errors']}")
        sys.exit(1)

    comment_data = result.get("data", {}).get("commentCreate", {})

    if not comment_data.get("success"):
        print("Error: Failed to add comment")
        sys.exit(1)

    comment = comment_data["comment"]
    issue = comment["issue"]

    print(f"✅ Comment added successfully!")
    print(f"   Issue: {issue['identifier']} - {issue['title']}")
    print(f"   Comment ID: {comment['id']}")
    print(f"   Created: {comment['createdAt']}")

    return comment

def main():
    parser = argparse.ArgumentParser(description="Add a comment to a Linear issue")
    parser.add_argument("--issue-id", "-i", required=True,
                        help="Issue identifier (e.g., ENG-123) or UUID")
    parser.add_argument("--body", "-b", required=True, help="Comment body text")
    parser.add_argument("--type", "-t",
                        choices=list(COMMENT_PREFIXES.keys()),
                        help="Comment type for automatic prefix")

    args = parser.parse_args()
    add_comment(args)

if __name__ == "__main__":
    main()
