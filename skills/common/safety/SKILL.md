---
name: safety
description: 삭제, 덮어쓰기, Git history 재작성, force push, 배포, 운영 변경처럼 복구가 어렵거나 외부에 영향이 있는 작업 전에 사용한다.
---

# Safety

1. 현재 요청과 대화에서 해당 대상·범위·효과에 대한 권한을 확인한다. 이미 확보한 구체적 승인은 재사용한다.
2. read-only 명령으로 정확한 대상, 범위, 현재 상태를 확정한다.
3. broad path, unresolved variable, glob을 destructive target으로 쓰지 않는다.
4. backup, branch, trash, dry-run처럼 가장 쉽게 복구할 방법을 우선한다.
5. account 생성, OAuth grant, token 발급, publish는 별도 권한 없이는 멈춘다.
6. 실행 뒤 대상과 영향, 복구 가능 여부를 다시 확인한다.

승인이 더 필요하면 허가된 가역적 준비·검증을 먼저 완료해 검토 가능한 대상·영향·복구 방법을 제시한다. 중단을 요구한 정확한 skill 조항과 적용 이유를 함께 밝힌다. 진단만 요청받았으면 수정하지 않는다.

## Codex 작업 영구 삭제 준비와 실행

공식 `thread/delete`는 지정한 persisted 작업과 그 작업이 생성한 모든 하위 작업의 기록·metadata를 영구 삭제한다. archive나 저장 프로젝트 등록 제거와 다르다. 현재 설치 CLI의 `app-server generate-json-schema`로 지원을 확인하고 [공식 App Server 계약](https://learn.chatgpt.com/docs/app-server)을 대조한다.

등록된 읽기 전용 준비 adapter는 Core의 `python -m woon_core.environment.codex_thread_review plan --thread-id <exact-id> --protected-thread-id <protected-id>`다. 여러 ID는 옵션을 반복한다. `ancestorThreadId`, 명시한 전체 source 종류, active·archived 양쪽 cursor를 끝까지 읽어 정확한 영향 목록과 metadata hash를 반환하며 삭제 호출은 하지 않는다. 원문을 수집하거나 내용 검토 완료를 대신 주장하지 않는다. 별도 stdio 서버의 `notLoaded`는 Desktop에서 실행 중이 아님을 증명하지 않는다.

명시 대상과 전체 하위 작업의 내용을 검토해 보존 가치를 먼저 구분한다. 가치 있는 개인 생각·경력과 이력·사용자가 지정한 보호 자료·실제 개발 학습과 질문은 보존하며, 보존할 내용이 있는 삭제 후보만 내용 담당의 정본 반영 근거를 확인한다. 의미 없는 단순 조작·반복 보고는 기술 키워드가 있다는 이유로 보존하거나 Wiki·별도 보존 archive를 만들지 않고 `no-unique-material`로 검토할 수 있다. 사용자가 삭제를 금지한 자료·관련 사본은 대상에서 제외하고, 관계나 보호 여부가 불명확하면 해당 작업과 이를 포함하는 삭제 부모를 보존한다. 실제 Desktop 실행 상태 확인을 먼저 완료하며, 프로젝트 폴더·DB·세션 파일 직접 삭제나 비공개 endpoint·UI로 우회하지 않는다. 저장 프로젝트 등록 제거는 별도 공식 지원 경로가 확인되기 전에는 실행하지 않는다.

실제 삭제에는 [검토한 작업 삭제 실행기](references/codex-thread-delete.md)의 exact plan/review hash, 전체 내용 검토와 보존 근거, 보호 ID, 최신 실제 Desktop raw 근거를 사용한다. `python -m woon_core.environment.codex_thread_delete`는 기본 preview이며 명시적 `--apply`에서만 검토한 root allowlist의 공식 API를 호출한다. `{}` 응답과 모든 영향 ID의 삭제 알림을 기록하고 같은 cwd의 active·archived 전체 페이지 재조회가 성공해야 success receipt를 남긴다. 조회 오류나 부재 관찰만으로 성공 처리하지 않고 불확실한 삭제를 자동 재시도하지 않는다. 실제 Desktop의 notLoaded는 최근 turn의 종료 상태·오류 부재·실행 중 turn 부재를 함께 확인한다. 시각이 명시적 null인 구형 completed·interrupted의 좁은 호환 조건은 위 실행기 reference를 따르며, latest failed나 별도 stdio의 notLoaded를 비활성 근거로 대신 쓰지 않는다.
