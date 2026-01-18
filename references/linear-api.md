# Linear API Reference

Linear GraphQL API를 사용한 이슈 관리 가이드.

## Authentication

### API Key 획득

1. Linear 설정 → API → Personal API keys
2. 새 키 생성
3. 환경변수로 설정:

```bash
export LINEAR_API_KEY="lin_api_xxxxxxxxxxxxx"
```

### API Endpoint

```
https://api.linear.app/graphql
```

## Common Operations

### 이슈 조회

```graphql
query GetIssue($id: String!) {
  issue(id: $id) {
    id
    identifier
    title
    description
    state {
      name
    }
    assignee {
      name
    }
    labels {
      nodes {
        name
      }
    }
  }
}
```

### 이슈 생성

```graphql
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue {
      id
      identifier
      title
      url
    }
  }
}
```

**Input 예시:**
```json
{
  "input": {
    "teamId": "TEAM_ID",
    "title": "새 기능 개발",
    "description": "기능 설명",
    "priority": 2,
    "labelIds": ["LABEL_ID"]
  }
}
```

### 이슈 상태 업데이트

```graphql
mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
    issue {
      id
      state {
        name
      }
    }
  }
}
```

**상태 변경 예시:**
```json
{
  "id": "ISSUE_ID",
  "input": {
    "stateId": "STATE_ID"
  }
}
```

### 코멘트 추가

```graphql
mutation CreateComment($input: CommentCreateInput!) {
  commentCreate(input: $input) {
    success
    comment {
      id
      body
      createdAt
    }
  }
}
```

**Input 예시:**
```json
{
  "input": {
    "issueId": "ISSUE_ID",
    "body": "작업 진행상황 업데이트"
  }
}
```

### 이슈 검색

```graphql
query SearchIssues($filter: IssueFilter) {
  issues(filter: $filter) {
    nodes {
      id
      identifier
      title
      state {
        name
      }
    }
  }
}
```

**필터 예시:**
```json
{
  "filter": {
    "team": { "key": { "eq": "TEAM" } },
    "state": { "name": { "in": ["In Progress", "Todo"] } }
  }
}
```

## Workflow States

### 일반적인 상태 흐름

```
Backlog → Todo → In Progress → In Review → Done
                      ↓
                  Canceled
```

### 상태 ID 조회

```graphql
query GetWorkflowStates($teamId: String!) {
  workflowStates(filter: { team: { id: { eq: $teamId } } }) {
    nodes {
      id
      name
      type
    }
  }
}
```

## Python 사용 예시

### 기본 설정

```python
import os
import requests

LINEAR_API_KEY = os.environ.get("LINEAR_API_KEY")
ENDPOINT = "https://api.linear.app/graphql"

headers = {
    "Authorization": LINEAR_API_KEY,
    "Content-Type": "application/json"
}

def execute_query(query, variables=None):
    response = requests.post(
        ENDPOINT,
        json={"query": query, "variables": variables or {}},
        headers=headers
    )
    return response.json()
```

### 이슈 생성

```python
def create_issue(team_id, title, description=""):
    query = """
    mutation CreateIssue($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        success
        issue { id identifier title url }
      }
    }
    """
    variables = {
        "input": {
            "teamId": team_id,
            "title": title,
            "description": description
        }
    }
    return execute_query(query, variables)
```

### 코멘트 추가

```python
def add_comment(issue_id, body):
    query = """
    mutation CreateComment($input: CommentCreateInput!) {
      commentCreate(input: $input) {
        success
        comment { id body }
      }
    }
    """
    variables = {
        "input": {
            "issueId": issue_id,
            "body": body
        }
    }
    return execute_query(query, variables)
```

### 상태 업데이트

```python
def update_status(issue_id, state_id):
    query = """
    mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
      issueUpdate(id: $id, input: $input) {
        success
        issue { id state { name } }
      }
    }
    """
    variables = {
        "id": issue_id,
        "input": {"stateId": state_id}
    }
    return execute_query(query, variables)
```

## Error Handling

### 일반적인 오류

| 오류 | 원인 | 해결 |
|------|------|------|
| 401 Unauthorized | API 키 누락/오류 | API 키 확인 |
| 403 Forbidden | 권한 없음 | 팀 멤버십 확인 |
| 404 Not Found | 이슈/팀 없음 | ID 확인 |
| Rate Limit | 요청 과다 | 잠시 후 재시도 |

### Rate Limits

- 분당 1,500 요청
- 복잡한 쿼리는 더 많은 비용 소모
- `X-RateLimit-*` 헤더로 상태 확인

## Team/Project IDs 찾기

```graphql
# 팀 목록
query {
  teams {
    nodes {
      id
      name
      key
    }
  }
}

# 프로젝트 목록
query {
  projects {
    nodes {
      id
      name
    }
  }
}

# 라벨 목록
query {
  issueLabels {
    nodes {
      id
      name
      color
    }
  }
}
```
