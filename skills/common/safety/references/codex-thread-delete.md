# 검토한 Codex 작업 영구 삭제

등록 실행기는 `python -m woon_core.environment.codex_thread_delete`다. 기본은 읽기 전용
검증이며 `--apply`가 있을 때만 공식 `thread/delete`를 호출한다. 내용 검토와 현재 사용자
승인이 완료된 exact root와 전체 descendant closure만 입력한다. 준비 조회기의
`ReadOnlyAppServer.request` 허용 목록은 읽기 전용으로 유지된다.

## 입력

`codex_thread_review plan`의 JSON을 수정하지 않고 `plan.json`으로 저장한다. 원본 파일
bytes의 SHA-256을 `review.json`과 실행 명령에 고정한다. review는 다음 구조다.

```json
{
  "version": 1,
  "plan_sha256": "<exact-plan-file-sha256>",
  "root_ids": ["<reviewed-root-id>"],
  "protected_ids": ["<protected-id>"],
  "operator_thread_id": "<executing-operator-id>",
  "authorization": {
    "effect": "permanent-root-and-descendants",
    "request_reference": "<current-user-authorization-reference>"
  },
  "content_reviews": [
    {
      "thread_id": "<affected-id>",
      "reviewer_thread_id": "<content-reviewer-id>",
      "all_history_reviewed": true,
      "retention": "no-unique-material",
      "content_sha256": "<full-official-thread-turns-sha256>",
      "evidence": {"path": "/absolute/content-review.json", "sha256": "<evidence-file-sha256>"}
    }
  ],
  "desktop_evidence": [
    {
      "thread_id": "<affected-id>",
      "observed_at": "<fresh-UTC-ISO-time>",
      "evidence": {"path": "/absolute/raw-desktop-read-thread.json", "sha256": "<file-sha256>"}
    }
  ]
}
```

content/desktop 항목은 root뿐 아니라 plan의 **모든 affected ID에 하나씩** 필요하다.
보호 목록·operator·reviewer·현재 실행 중인 `CODEX_THREAD_ID`와 겹치는 root/descendant는
삭제하지 않는다. 증거는 실존하는 일반 파일의 exact bytes hash로 확인한다.
`retention: preserved`라면 `preserved_evidence`에 보존한 정본 파일의 `{path, sha256}`
목록을 추가한다. 본문 검토의 의미 판정은 담당자의 attestation이며 코드가 대신 판단하지 않는다.

`content_sha256`은 공식 `thread/read`의 `includeTurns: true` 결과에서 `thread.turns`를
`hashlib.sha256(json.dumps(turns, sort_keys=True).encode()).hexdigest()`로 계산한다.
실행기는 삭제 직전 같은 공식 전체 turns를 다시 읽어 비교하고 본문은 receipt에 복제하지 않는다.

Desktop 근거는 공식 `mcp__codex_app__read_thread`의 raw JSON이다. `content[].text`로
감싸진 tool 결과도 지원한다. exact ID·`kind: codex`·`hostId: local`·cwd·updatedAt이 plan과
일치하고 newest-first여야 한다. 관찰 시각은 적용 시점 기준 5분 이내여야 한다.
`status.type: idle`을 인정한다. `notLoaded`는 **실제 Desktop raw 결과에서** 가장 최근
turn이 completed 또는 interrupted이며 error=null/completedAt 존재이고 반환된 turns에 실행 중/알 수 없는 상태가
없을 때 인정한다. 공식 Turn schema는 completedAt=null을 허용하고 interrupted는 종료 상태이므로,
구형 기록은 최신 turn이 completed 또는 interrupted이고 error와 completedAt 필드가 명시적 null일 때 별도 호환 경로를 쓴다.
이때 Desktop 전체 페이지가 끝났음(hasMore=false/nextCursor=null), 반환된 모든 turn이
completed 또는 interrupted이고 명시적 error=null임, 최신 turn의 startedAt 필드가
명시적 null이거나 `0 < startedAt <= reviewed updatedAt`인 정수임을 모두 확인한다.
nextCursor 필드도 명시적으로 존재해야 하며 정수 metadata 시각은
`0 < reviewed updatedAt < observed_at`이어야 한다. 누락된 필드를 null로 간주하지 않는다.
5분 freshness·exact metadata·전체 내용 hash·보호 closure와 삭제 직전 재조회는 그대로 적용한다.
failed, inProgress·unknown, 불완전한 페이지·오류 근거·유효하지 않은 시각은 이 예외로 허용하지 않는다.
별도 stdio 서버의 `notLoaded` 단독 결과는 이 증거를 대신할 수 없다. 상태를 임의로 idle로
바꾸거나 상태 확인을 위해 작업을 resume하지 않는다. [공식 종료 상태 계약](https://learn.chatgpt.com/ko-KR/docs/app-server)

### 여러 Desktop 페이지의 종료 근거

구형 기록이 Desktop 한 페이지에 들어가지 않으면 `desktop_evidence[].evidence`가
아래 manifest 파일의 경로와 SHA-256을 가리키게 한다. 바깥 `thread_id`·`observed_at`과
review 전체 hash 계약은 그대로 유지한다. 각 `evidence`는 실제 `read_thread` raw 파일이다.

```json
{
  "schemaVersion": 1,
  "kind": "codex-desktop-read-thread-pages",
  "threadId": "<affected-id>",
  "pages": [
    {
      "request_cursor": null,
      "observed_at": "<first-page-UTC-ISO-time>",
      "evidence": {"path": "/absolute/page-00.json", "sha256": "<raw-sha256>"}
    },
    {
      "request_cursor": "<first-page-nextCursor>",
      "observed_at": "<second-page-UTC-ISO-time>",
      "evidence": {"path": "/absolute/page-01.json", "sha256": "<raw-sha256>"}
    }
  ]
}
```

최초 요청 cursor는 명시적 null이고 이후에는 직전 raw의 nextCursor와 정확히 같아야 한다.
모든 페이지의 raw hash·5분 freshness·thread/host/kind/cwd/updatedAt·동일 Desktop status와
newest-first 순서를 확인한다. 중간 페이지는 hasMore=true와 서로 다른 유효 nextCursor,
마지막은 hasMore=false와 명시적 nextCursor=null이어야 한다. 중복·빈 turn ID, 빈 페이지,
failed/inProgress/unknown 또는 error 누락·오류가 있는 turn은 거부한다. manifest 중첩도 허용하지 않는다.
전체 페이지를 이 순서로 확인한 뒤에만 완료된 이력으로 판정하며 최신 turn은 항상 첫 페이지의
첫 turn이다. 마지막 페이지를 최신 근거로 대신 사용하거나 hasMore guard를 제거하지 않는다.
실행 직전에도 manifest와 각 raw hash·freshness를 다시 검사한다. 수집 중 5분을 넘겼으면
관찰 시각을 바꾸지 말고 실제 페이지를 다시 조회한다. 단일 raw 입력 경로도 계속 지원한다.

## 실행과 재조회

```bash
python -m woon_core.environment.codex_thread_delete \
  --plan /absolute/plan.json --review /absolute/review.json \
  --expected-plan-sha256 <plan-file-sha256> --expected-review-sha256 <review-file-sha256> \
  --receipt-dir /absolute/private-delete-receipts
```

preview가 통과하면 동일 명령에 `--apply`를 추가한다. private receipt directory는 owner-only
여야 한다. 기존 동일 plan/review 시도는 자동 재실행하지 않는다. 여러 root는 직렬로 처리하며
각 root 직전에 새 metadata·전체 descendant closure·본문 hash·Desktop 관찰 freshness를 확인한다.

공식 API는 root와 생성된 모든 descendants의 기록·metadata를 영구 삭제한다. 각 요청의
`{}` 응답과 affected ID 전부의 `thread/deleted` 알림을 수집한 뒤, 같은 cwd의 active/archived
모든 source 종류와 페이지를 재조회해야 성공 receipt를 남긴다. 알림은 응답 전후 모두 수집한다.
예상 밖 deleted ID, 응답 오류, 알림 누락, 목록 pagination 오류나 남은 ID가 있으면 다음 root를
진행하지 않고 `failed-or-uncertain` attempt를 남긴다. 삭제 여부가 불확실한 요청은 자동 재시도하지 않는다.

성공은 `<plan-sha>-<review-sha>.receipt.json`, 진행·실패는 같은 key의 `.attempt.json`이다.
오류 뒤 `all_absent: true`만으로 성공으로 바꾸지 않는다. 이미 일부 root가 삭제됐을 수 있으므로
attempt의 delete_responses·notifications·root_results·requery를 확인한 뒤 남은 범위를 새로 검토한다.
DB·session 파일 직접 삭제, UI 우회, 프로젝트 등록 제거는 제공하지 않는다.

현재 공식 `thread/delete`에는 조건부 revision 인자가 없다. 실행 직전 조회와 최신 Desktop
근거로 범위를 좁히지만 조회와 삭제 사이의 새 활동을 원자적으로 잠글 수는 없다. 담당자는
적용 중 대상 작업을 다시 시작하거나 하위 작업을 만들지 않는 상태를 유지한다. 파일 backup이나
자동 복구를 제공하는 것으로 표현하지 않는다. [공식 삭제 계약](https://learn.chatgpt.com/ko-KR/docs/app-server)
