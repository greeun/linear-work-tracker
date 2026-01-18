# Linear Work Tracker

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai)
[![Linear](https://img.shields.io/badge/Linear-Integration-5E6AD2)](https://linear.app)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 개발 작업을 Linear 이슈에 자동으로 추적하고 업데이트하는 스킬

[English Documentation](README.md)

## 개요

Linear Work Tracker는 개발 활동을 Linear 이슈에 자동으로 기록하는 Claude Code 스킬입니다. 다양한 작업 유형(기능, 버그, 수정, 삭제)에 대한 워크플로우 템플릿과 Linear API 연동을 위한 스크립트를 제공합니다.

## 주요 기능

- **워크플로우 템플릿**: Feature, Bug Fix, Modification, Deletion 작업을 위한 사전 정의된 워크플로우
- **자동 로깅**: 일관된 작업 문서화를 위한 이모지 prefix 코멘트 템플릿
- **Linear API 스크립트**: 이슈 생성, 코멘트, 상태 업데이트를 위한 Python 스크립트
- **GraphQL 레퍼런스**: 커스터마이징을 위한 완전한 Linear API 문서

## 설치

### 사전 요구사항

- Claude Code CLI
- Python 3.8+
- Linear API 키

### 설정

1. **스킬 클론**:
   ```bash
   git clone https://github.com/greeun/linear-work-tracker.git ~/.claude/skills/linear-work-tracker
   ```

2. **Linear API 키 설정**:
   ```bash
   export LINEAR_API_KEY="lin_api_xxxxxxxxxxxxx"
   ```

   API 키 발급 방법:
   1. Linear 설정 → API → Personal API keys 이동
   2. 새 키 생성
   3. 쉘 프로필에 추가 (`~/.zshrc` 또는 `~/.bashrc`)

3. **의존성 설치**:
   ```bash
   pip install requests
   ```

## 사용법

### 자동 활성화

작업 추적을 언급하면 스킬이 활성화됩니다:

```
"이 기능을 Linear에 기록해줘"
"Linear 이슈에 진행상황 업데이트해줘"
"이 버그 수정에 대한 Linear 이슈 생성해줘"
"이 작업을 Linear에서 추적해줘"
```

### 워크플로우 유형

#### 1. 기능 개발 (Feature)

```markdown
🚀 작업 시작
- 목표: [기능 설명]
- 예상 변경 파일: [파일 목록]
- 시작 시간: [타임스탬프]

📝 진행상황 업데이트
- 완료: [완료된 항목]
- 진행중: [현재 작업]
- 변경된 파일: [파일 목록]

✅ 작업 완료
- 변경 요약: [요약]
- 변경된 파일: [파일 목록]
- 커밋: [커밋 해시]
```

#### 2. 버그 수정 (Bug Fix)

```markdown
🔍 버그 분석
- 증상: [버그 현상]
- 원인: [근본 원인]
- 영향 범위: [영향받는 기능]

🔧 수정 완료
- 수정 내용: [변경사항]
- 테스트 결과: [검증 내용]
- 회귀 테스트: [결과]
```

#### 3. 코드 수정 / 리팩토링 (Modification)

```markdown
🔄 코드 수정
- 수정 유형: [리팩토링/성능개선/코드정리]
- 대상: [파일/함수/클래스]
- 변경 전: [이전 상태]
- 변경 후: [변경 후 상태]
- 이유: [수정 사유]
```

#### 4. 코드 삭제 (Deletion)

```markdown
🗑️ 코드 삭제
- 삭제 대상: [파일/함수/클래스]
- 삭제 이유: [사유]
- 영향 범위: [의존성 확인 결과]
- 대체 방안: [있다면 설명]
```

### Python 스크립트

#### 이슈 생성

```bash
python scripts/create_issue.py \
  --title "새 로그인 기능" \
  --team "ENG" \
  --description "OAuth 로그인 구현" \
  --priority 2 \
  --status "in_progress"
```

옵션:
| 옵션 | 설명 |
|------|------|
| `--title` | 이슈 제목 (필수) |
| `--team` | 팀 키 또는 ID (필수) |
| `--description` | 이슈 설명 |
| `--priority` | 0=없음, 1=긴급, 2=높음, 3=중간, 4=낮음 |
| `--status` | backlog, todo, in_progress, done |
| `--labels` | 쉼표로 구분된 라벨 ID |
| `--assignee` | 담당자 사용자 ID |
| `--project` | 프로젝트 ID |

#### 코멘트 추가

```bash
python scripts/add_comment.py \
  --issue-id "ENG-123" \
  --body "로그인 UI 완료" \
  --type progress
```

코멘트 유형:
| 유형 | 이모지 | 설명 |
|------|--------|------|
| `start` | 🚀 | 작업 시작 |
| `progress` | 📝 | 진행상황 업데이트 |
| `complete` | ✅ | 작업 완료 |
| `analysis` | 🔍 | 분석/조사 |
| `fix` | 🔧 | 수정/수리 |
| `delete` | 🗑️ | 삭제 |
| `warning` | ⚠️ | 주의/이슈 |
| `refactor` | 🔄 | 리팩토링 |

#### 상태 업데이트

```bash
python scripts/update_status.py \
  --issue-id "ENG-123" \
  --status "done" \
  --comment "구현 완료"
```

상태 옵션: `backlog`, `todo`, `in_progress`, `in_review`, `done`, `canceled`

## 프로젝트 구조

```
linear-work-tracker/
├── SKILL.md                          # 메인 워크플로우 가이드
├── TEST_SCENARIOS.md                 # 검증 테스트 케이스
├── references/
│   └── linear-api.md                 # Linear GraphQL API 레퍼런스
└── scripts/
    ├── create_issue.py               # 이슈 생성
    ├── add_comment.py                # 코멘트 추가
    └── update_status.py              # 상태 업데이트
```

## API 레퍼런스

`references/linear-api.md`에 포함된 내용:

- 인증 설정
- 일반적인 GraphQL 쿼리 및 뮤테이션
- 이슈 CRUD 작업
- 코멘트 관리
- 워크플로우 상태 처리
- Python 코드 예시
- 오류 처리 가이드
- Rate limit 정보

### 빠른 API 예시

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

## 환경 변수

| 변수 | 설명 | 필수 |
|------|------|------|
| `LINEAR_API_KEY` | Linear API 키 | 예 |

## 테스트 시나리오

`TEST_SCENARIOS.md` 파일에 포함된 검증 테스트:

- **Happy Path**: 스킬이 트리거되어야 하는 표준 요청
- **Edge Cases**: 비정상적이지만 유효한 요청
- **Out of Scope**: 트리거되지 않아야 하는 요청

## 기여

기여를 환영합니다! Pull Request를 자유롭게 제출해주세요.

## 라이선스

MIT 라이선스 - 자세한 내용은 [LICENSE](LICENSE)를 참조하세요.

## 관련 링크

- [Linear API 문서](https://developers.linear.app/docs)
- [Claude Code 스킬](https://docs.anthropic.com/claude-code/skills)
- [skill-wizard](https://github.com/greeun/skill-wizard) - 이 스킬을 만드는 데 사용된 도구
