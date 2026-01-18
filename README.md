# Linear Work Tracker

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai)
[![Linear](https://img.shields.io/badge/Linear-Integration-5E6AD2)](https://linear.app)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Automatic Linear issue tracking and updates for development work.

[한국어 문서](README.ko.md)

## Overview

Linear Work Tracker is a Claude Code skill that automatically logs your development activities to Linear issues. It provides workflow templates for different work types (features, bugs, modifications, deletions) and scripts for seamless Linear API integration.

## Features

- **Workflow Templates**: Pre-defined workflows for Feature, Bug Fix, Modification, and Deletion tasks
- **Auto-Logging**: Emoji-prefixed comment templates for consistent work documentation
- **Linear API Scripts**: Python scripts for issue creation, commenting, and status updates
- **GraphQL Reference**: Complete Linear API documentation for customization

## Installation

### Prerequisites

- Claude Code CLI
- Python 3.8+
- Linear API key

### Setup

1. **Clone the skill**:
   ```bash
   git clone https://github.com/greeun/linear-work-tracker.git ~/.claude/skills/linear-work-tracker
   ```

2. **Set up Linear API key**:
   ```bash
   export LINEAR_API_KEY="lin_api_xxxxxxxxxxxxx"
   ```

   To get your API key:
   1. Go to Linear Settings → API → Personal API keys
   2. Create a new key
   3. Add to your shell profile (`~/.zshrc` or `~/.bashrc`)

3. **Install dependencies**:
   ```bash
   pip install requests
   ```

## Usage

### Automatic Activation

The skill activates when you mention work tracking:

```
"Log this feature to Linear"
"Update the Linear issue with my progress"
"Create a Linear issue for this bug fix"
"Track this work in Linear"
```

### Workflow Types

#### 1. Feature Development

```markdown
🚀 작업 시작
- Goal: [Feature description]
- Expected files: [File list]
- Start time: [Timestamp]

📝 진행상황 업데이트
- Completed: [Done items]
- In progress: [Current work]
- Changed files: [File list]

✅ 작업 완료
- Summary: [Changes summary]
- Files changed: [File list]
- Commit: [Commit hash]
```

#### 2. Bug Fix

```markdown
🔍 버그 분석
- Symptom: [Bug behavior]
- Root cause: [Cause]
- Impact: [Affected features]

🔧 수정 완료
- Fix: [What was changed]
- Test result: [Verification]
- Regression test: [Results]
```

#### 3. Code Modification / Refactoring

```markdown
🔄 코드 수정
- Type: [Refactoring/Performance/Cleanup]
- Target: [File/Function/Class]
- Before: [Previous state]
- After: [New state]
- Reason: [Why changed]
```

#### 4. Code Deletion

```markdown
🗑️ 코드 삭제
- Target: [File/Function/Class]
- Reason: [Why deleted]
- Impact: [Dependency check result]
- Alternative: [If applicable]
```

### Python Scripts

#### Create Issue

```bash
python scripts/create_issue.py \
  --title "New Login Feature" \
  --team "ENG" \
  --description "Implement OAuth login" \
  --priority 2 \
  --status "in_progress"
```

Options:
| Option | Description |
|--------|-------------|
| `--title` | Issue title (required) |
| `--team` | Team key or ID (required) |
| `--description` | Issue description |
| `--priority` | 0=none, 1=urgent, 2=high, 3=medium, 4=low |
| `--status` | backlog, todo, in_progress, done |
| `--labels` | Comma-separated label IDs |
| `--assignee` | Assignee user ID |
| `--project` | Project ID |

#### Add Comment

```bash
python scripts/add_comment.py \
  --issue-id "ENG-123" \
  --body "Completed the login UI" \
  --type progress
```

Comment types:
| Type | Emoji | Description |
|------|-------|-------------|
| `start` | 🚀 | Work started |
| `progress` | 📝 | Progress update |
| `complete` | ✅ | Work completed |
| `analysis` | 🔍 | Analysis/Investigation |
| `fix` | 🔧 | Fix/Repair |
| `delete` | 🗑️ | Deletion |
| `warning` | ⚠️ | Warning/Issue |
| `refactor` | 🔄 | Refactoring |

#### Update Status

```bash
python scripts/update_status.py \
  --issue-id "ENG-123" \
  --status "done" \
  --comment "Implementation complete"
```

Status options: `backlog`, `todo`, `in_progress`, `in_review`, `done`, `canceled`

## Project Structure

```
linear-work-tracker/
├── SKILL.md                          # Main workflow guide
├── TEST_SCENARIOS.md                 # Validation test cases
├── references/
│   └── linear-api.md                 # Linear GraphQL API reference
└── scripts/
    ├── create_issue.py               # Create new issues
    ├── add_comment.py                # Add comments to issues
    └── update_status.py              # Update issue status
```

## API Reference

The `references/linear-api.md` includes:

- Authentication setup
- Common GraphQL queries and mutations
- Issue CRUD operations
- Comment management
- Workflow state handling
- Python code examples
- Error handling guide
- Rate limit information

### Quick API Example

```python
import os
import requests

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY")
ENDPOINT = "https://api.linear.app/graphql"

def create_issue(team_id, title):
    query = """
    mutation CreateIssue($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        success
        issue { id identifier title url }
      }
    }
    """
    response = requests.post(
        ENDPOINT,
        json={
            "query": query,
            "variables": {"input": {"teamId": team_id, "title": title}}
        },
        headers={"Authorization": LINEAR_API_KEY}
    )
    return response.json()
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `LINEAR_API_KEY` | Your Linear API key | Yes |

## Test Scenarios

The `TEST_SCENARIOS.md` file contains validation tests:

- **Happy Path**: Standard requests that should trigger the skill
- **Edge Cases**: Unusual but valid requests
- **Out of Scope**: Requests that should NOT trigger

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related

- [Linear API Documentation](https://developers.linear.app/docs)
- [Claude Code Skills](https://docs.anthropic.com/claude-code/skills)
- [skill-wizard](https://github.com/greeun/skill-wizard) - Tool used to create this skill
