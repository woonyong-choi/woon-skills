---
name: tasks
description: Obsidian의 반복 할 일·일일 기록을 관리하고 사용자가 요청한 Google Calendar 일정·동기화를 등록 adapter와 영수증·재조회 경계에서 처리할 때 사용한다. 지식·Novel 원고는 task로 등록하지 않는다.
---

# Tasks

할 일의 정본은 private `woon-knowledge`의 Markdown이다. 반복 routine은 `inbox/tasks/routines/`, 오늘의 실행 항목은 `inbox/daily/`의 `<!-- woon-tasks:start -->`와 `<!-- woon-tasks:end -->` 사이만 소유한다. 시간 약속의 외부 연동은 Google Calendar를 사용한다. Apple Calendar 수집·EventKit 쓰기·Markdown/ICS projection 생성은 퇴역했으며 기존 일정 문서는 보존한다.

## Trigger

- 반복 할 일·습관을 만들거나 바꿔 달라는 요청
- 오늘의 할 일·일일 기록을 생성하거나 완료해 달라는 요청
- Obsidian에서 할 일을 찾거나 중복 없이 다시 반영해 달라는 요청
- Google Calendar 일정 또는 선택한 Markdown 일정 source의 동기화를 요청하는 경우
- 시간·제목이 있는 Google Calendar 일정의 생성·변경을 직접 요청하는 경우

지식 노트 저장은 `$archive`, Google 동기화 설정·plugin 운영은 `$obsidian-plugin`, Novel 원고는 Novel skill의 책임이다.

## Workflow

요청한 동작에 필요한 단계만 적용한다. routine 생성·변경은 아래 흐름을 따르고, 기존 항목 완료는 조회→`woon_tasks_complete`→재조회로 끝낸다. Calendar 요청은 아래 Calendar Boundary를 따르며 routine이나 goal을 만들지 않는다. 현재 대화에서 이미 확인한 목적·종료 기준은 재사용한다.

1. 먼저 `woon_tasks_find`로 같은 제목·목적의 routine과 오늘 항목을 확인한다.
2. 반복 routine에는 사용자가 말했거나 확인한 `purpose`가 있는지 확인한다. 목적이 없으면 추정하거나 과거 문서에서 만들어 내지 말고, 목적 한 문장을 요청한다. 종료 가능한 목표라면 종료 기준도 확인한다.
3. 목표가 있는 routine은 먼저 `woon_tasks_upsert_goal`로 `goal_id`, 목표, 종료 기준, 필요하면 종료일 또는 사용자 확인 측정값을 저장한다. 목표 문서는 `inbox/tasks/goals/`의 사용자가 직접 고칠 수 있는 Markdown 정본이다.
4. `woon_tasks_upsert_recurring_todo`로 `task_id`, 제목, 목적, 영역, 시작일, 연결한 `goal_id`를 저장한다. 제목은 동사로 시작하고 한 번에 검증할 수 있어야 한다.
5. `woon_tasks_materialize_due`로 해당 KST 날짜의 `woon-tasks` 관리 구역만 갱신한다. 일일 자유 메모·Codex block·일정 원자료·Wiki는 읽거나 승격하지 않는다. 목표가 달성·중단되었거나 종료일을 지났다면 routine은 다음 날짜부터 자동 제외되어야 한다.
6. 생성·수정·완료 뒤 같은 MCP로 다시 조회해 routine과 일일 항목이 하나씩인지 확인하고, receipt가 local runtime state에 남았는지 확인한다.
7. 완료는 `woon_tasks_complete`로 해당 날짜의 해당 항목만 표시한다. 이 작업은 Calendar event나 활동 이력을 완료 처리하지 않는다.

일일 이력은 실제 변경·완료 체크·사용자 메모가 있을 때 남긴다. 현재 날짜의 실행할 routine은 표시하되, 미완료 기본 routine을 지난 날짜마다 복제하거나 routine이 없는 날짜의 빈 문서를 만들지 않는다. 명시적으로 요청한 과거 항목 완료는 실제 체크 기록으로 보존한다. 오늘의 기존 파일에서는 종료된 routine의 미완료 행만 제거하고 완료 체크·자유 메모·다른 writer 구역은 유지한다. Codex 원본 미발견·대기·승격 미완료는 runtime 오류/재개 상태이며 일일 본문·Review 카드·성공 checkpoint를 만들지 않는다. 독자 화면에는 날짜와 실제 핵심 내용을 표시하고 처리 상태·파일 mtime을 활동 이력으로 내세우지 않는다.

사용자가 반복 정의와 이전 기록의 삭제를 함께 요청하면 위의 기본 완료 보존보다 그 명시 지시가 우선한다. `woon tasks preview-deletion --ids <exact-id,...>`로 정의·동일 ID 관리행·완료행·빈 날짜 후보·revision을 확인하고, 검토한 request를 `woon tasks delete-recurring --request <file>`로 적용한다. 요청 필드는 Core README의 Tasks 삭제 계약을 따른다. 이름이 같다는 이유로 다른 ID·사용자 본문·실제 일정·다른 목표를 삭제하지 않는다. 삭제 영수증과 재조회로 정의 및 관리행 부재, 빈 날짜 제거, 동일 입력 재실행을 확인한다.

일기의 내용 기준은 `repo://knowledge/inbox/daily/README.md`가 소유한다. 사용자가 직접 예약·기억해 달라고 한 일정과 메모, 실제 쓴 일기, 당일 의미 있는 작업·대화 결과를 해당 날짜 H1 아래 키워드 H2와 블릿으로 정리한다. 빈 섹션·미발견·AI 처리 로그는 기록하지 않는다. 예정과 실제 발생을 구분하며, 이 규칙을 바꿨다는 이유로 과거 채팅 전체 수집이나 일일·메일 자동화를 재개하지 않는다.

## Calendar Boundary

- 외부 전송과 source 소유권은 `repo://knowledge/docs/obsidian-calendar-integration.md`를 따른다. Google 계정·Calendar·선택 source와 현재 요청의 변경 범위를 확인하고 기존의 구체적 승인은 재사용한다.
- Google 쓰기는 실제 등록된 adapter와 해당 작업의 receipt·원격 재조회가 있을 때만 실행한다. 연결·설치·로컬 hash만으로 원격 일정 반영을 주장하지 않는다. 아직 없는 adapter 명령을 만들어 호출하지 않고, 독립적인 로컬 준비를 완료한 뒤 실제 누락된 연결·대상만 확인한다.
- 같은 일정의 변경은 기존 Calendar·event ID와 sync record를 재사용한다. 일부 필드 수정은 나머지 제목·시간·장소·메모를 보존한다. 응답이 불명확하면 재조회로 결과를 확인하기 전에 같은 생성을 다시 전송하지 않는다.
- 일반 Markdown source는 Link Calendar의 실제 profile과 속성 mapping으로 읽는다. 로컬 편집 권한과 Google 전송 허용을 구분한다. 선택된 source의 동기화에서 `external_sync: deny` 일정만 명시적으로 제외하고 `access: local-only`만으로 차단하지 않는다.
- 메일·문서의 날짜는 후보이며 외부 일정 생성 권한이 아니다. 자동 후보 수집과 사용자가 직접 요청한 일정 적용을 구분한다. 예정된 일정이나 task 체크를 실제 활동·개인 성과·인물 사실로 승격하지 않는다.
- 기존 Apple 일정 문서와 이미 Google에 올라간 기록은 자동 삭제·재생성하지 않는다. 퇴역 source 해제는 `$obsidian-plugin`의 등록 adapter로 해당 ID만 처리한다.

## Prohibited

- 퇴역한 외부 할 일 앱, URL Scheme, 앱 데이터베이스, AppleScript, 화면 UI 자동화로 할 일을 만들거나 고치지 않는다.
- 퇴역한 Apple Calendar CLI·MCP·Swift·EventKit 경로를 복원하거나 앱 UI로 우회하지 않는다.
- Obsidian 파일을 정규 path 밖에서 직접 수정하지 않는다. task service가 소유한 routine과 marker 구역만 MCP/CLI로 바꾼다.
- purpose를 LLM이 추정해 사실처럼 기록하지 않는다.
- task 체크만으로 학습·경력·활동 완료를 확정하거나 지식·원본·인물·Novel 자료를 task로 저장하지 않는다.
- 사용자가 확인하지 않은 체중·출석·성과·마감 달성을 추정해 목표를 끝내지 않는다. 측정 목표는 `measurement_confirmed: true`일 때만 자동 종료 판단에 쓴다.
