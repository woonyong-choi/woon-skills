---
name: obsidian-plugin
description: Woon Obsidian Vault의 Community Plugin 상태와 실행 정책을 확인하고, 승인된 build 설치·설정·원격 실행 차단·활성화·제거를 receipt·backup·hash로 관리할 때 사용한다.
---

# Obsidian Plugin

실패한 companion의 orphan은 `recover-runnable-companion-orphan --pid <exact-pid>`로 preview한 뒤 그 `expected_state`를 고정해 처리한다. 이 경로는 관리 state가 없는 exact artifact의 orphan만 다루며 현재 사용자의 PID·시작 signature·PGID·cwd를 확인하고 PID 하나에 SIGTERM만 보낸다. 임의 kill·group 종료·config 재작성으로 우회하지 않는다. 복구와 새 시작의 절차는 [관리 companion 연결](references/runnable-companion.md)에 있다.

승인된 Runnable 로컬 companion 시작과 SecretStorage pairing은 [관리 companion 연결](references/runnable-companion.md)을 따른다. `start-runnable-companion`·`pair-runnable-companion`은 각각 preview의 `expected_state`를 고정하고 적용하며, `runnable-companion-status`로 소유한 PID·artifact·인증 capabilities를 재조회한다. 기존 config·다른 token·동시 변경을 보존하고 remote 실행은 false로 유지한다. 연결 receipt는 실제 코드 실행 증거를 대신하지 않는다.

Obsidian plugin은 UI 조작이나 임의 폴더 복사로 관리하지 않는다. `$obsidian-plugin`은 Core의 receipt 기반 adapter만 사용한다.

```bash
woon knowledge obsidian-plugin status --vault <vault>
woon knowledge obsidian-plugin install --plugin <approved-id> --vault <vault>
woon knowledge obsidian-plugin install-local-build --plugin <approved-development-id> \
  --source-dir <built-plugin-directory> --version <exact-version> --vault <vault>
woon knowledge obsidian-plugin remove-detected-mindmaps --vault <vault>
woon knowledge obsidian-plugin retire-apple-calendar-source --vault <vault>
woon knowledge obsidian-plugin retire-apple-calendar-source --vault <vault> \
  --apply --expected-settings-sha256 <preview-before-sha256>
woon knowledge obsidian-plugin configure-google-two-way-source --vault <vault>
woon knowledge obsidian-plugin configure-google-two-way-source --vault <vault> \
  --apply --expected-settings-sha256 <preview-before-sha256>
woon knowledge obsidian-plugin disable-runnable-remote-execution --vault <vault>
woon knowledge obsidian-plugin disable-runnable-remote-execution --vault <vault> \
  --apply --expected-settings-sha256 <preview-before-sha256>
woon knowledge obsidian-plugin attest-link-calendar-runtime \
  --attested-check ribbon --attested-check month-view --attested-check event-marker \
  --attested-check daily-agenda --attested-check direct-note-link \
  --attested-check readonly-blocked --vault <vault>
woon knowledge obsidian-plugin retire --plugin notion-bases --vault <vault>
```

Runnable의 원격 실행 차단은 `disable-runnable-remote-execution`을 사용한다. 이 adapter는 기존 설정에서 `remoteExecutionEnabled: false`만 적용하며 legacy/path·다른 설정·local 실행·pairing·SecretStorage를 보존한다. preview hash, backup, 동시 변경 검사, 소유한 변경만 rollback, receipt와 디스크 재조회를 요구한다. `disk_policy_verified`와 `runtime_policy_verified`는 별개이며 이 adapter는 앱·runner·네트워크를 호출하지 않는다. 이미 실행 중인 대상 Vault에서 정책을 읽어들이고 별도 읽기 전용 조회로 확인하는 절차는 [Runnable 원격 실행 차단의 runtime 반영](references/runnable-remote-policy.md)을 따른다. companion 배포·pairing·책 코드 실행은 별도 작업이다.

`status`는 설치 manifest, version, 활성 config, 설정 파일과 `mindmap` 판정을 read-only로 반환한다. 설치는 allowlist의 공식 GitHub release API와 release asset SHA-256을 확인하고, manifest `id`가 요청 ID와 같을 때만 stage → backup → atomic replace → `community-plugins.json` 갱신 → 재조회 순서로 진행한다. receipt와 backup은 Vault의 Git 제외 `.local/woon-knowledge/obsidian-plugins/`에 남긴다.

Community Plugin 등록 전에 사용자가 소유한 plugin을 실제 Vault에서 검증해야 할 때는 임의 폴더 복사 대신 `install-local-build`만 사용한다. 현재 요청과 대화에서 대상 교체 권한이 확인됐고 [approved plugins](references/approved-plugins.md)의 development allowlist에 있는 ID에 한해, `main.js`·`manifest.json`·`styles.css`의 일반 파일 여부, manifest ID, 정확한 version과 SHA-256을 확인한다. 기존 설정 파일은 변경 없이 보존하고 stage → backup → atomic replace → 활성 config 재조회를 거친다. 실패하면 runtime·설정·활성 config를 모두 기존 상태로 복원한다. 이 경로는 로컬 개발 검증일 뿐 공식 release나 Community Plugin 승인을 대체하지 않으며 자동화에서 임의로 호출하지 않는다.

설치 전에는 먼저 `status`로 대상 ID와 기존 mindmap plugin을 확정한다. 삭제는 `remove-detected-mindmaps`만 사용해 설치 manifest가 실제 mindmap인 plugin만 backup으로 옮긴다. Obsidian 기본 Canvas, Excalidraw, 비 mindmap plugin, 그리고 이름만 비슷한 폴더는 제거하지 않는다.

Community plugin 설정상 활성화와 현재 실행 중인 Obsidian의 runtime load는 다르다. adapter는 저장하지 않은 문서를 잃을 수 있는 앱 재시작이나 UI 자동화를 하지 않는다. 설치 뒤 Obsidian을 안전하게 reload한 다음 `status` receipt와 실제 plugin 화면으로 rendered 동작을 확인한다.

`linked-graph`는 현재 Markdown의 resolved outgoing wikilink만 작성 순서로 읽고 목차와 현재 문서의 실제 1-hop force graph를 전환하는 오른쪽 사이드바다. resolved destination이나 정본 `parent`가 private·source·generated·archive 경로에 있거나 lifecycle이 archived·retired·superseded이면 route와 preview에서 제외한다. 그래프 모드는 compact header 아래 남은 leaf를 여백 없이 viewport로 사용하고, 노드 수와 viewport를 함께 반영한 제한 없는 일시적 world 좌표에서 움직인다. viewport 경계로 노드를 clamp하지 않으며 pan·zoom과 현재 node bounds 기반 fit으로 화면 밖 graph를 탐색한다. 고정 배경 키워드나 별도 group anchor를 만들지 않아 모든 제목이 node와 함께 움직인다. 현재 문서와 직접 outgoing link는 같은 연속 force simulation에서 움직이고 drag 시 simulation을 다시 가열하며, 현재 문서 클릭은 정본 `parent`로 이동한다. 직접 링크 hover·focus 동안에만 그 문서의 실제 outgoing link를 반투명 2-hop preview로 표시한다. hover source를 임시 고정하고 실측 제목 폭 collision과 다중 ring을 적용해 preview 생성·해제 반복과 겹침을 막는다. hover·focus는 채워진 card나 사각 outline 대신 node dot만 강조한다. 상위 `parent`가 없는 중심 노드는 버튼이나 tab stop으로 노출하지 않는다. 노드 색은 제목을 추측하지 않고 기존 `type`·`node_kind`·`entity_kind`·`facets` metadata만 읽으며 색은 점에만 적용하고 제목은 host text color를 유지한다. `calendar-event` 일정은 orange, 인물은 pink, 프로젝트는 blue, topic·detail 개념 하위 항목은 green으로 고정하고 책은 purple, hub·resource는 cyan, 판정 불가는 neutral을 사용한다. 모든 중심·직접·preview 노드는 Obsidian Graph와 같이 점 아래에 제목을 두고, 직접 링크는 host `--graph-line` 1px 실선, preview 링크는 같은 색의 1px 점선으로 표시한다. preview·불릿 그룹·위치·화면 상태는 저장 엔티티가 아닌 일시적 UI다. Markdown·Canvas·Map·관계·레이아웃·설정 파일을 쓰지 않는다. exact `1.6.6` local build와 receipt가 확인된 뒤에만 구형 `context-graph`를 `retire`로 backup 이동한다. 편집기의 fold 상태는 공개 API로 읽지 않고, 그룹 접기·검색·화면 전환은 세션 UI 상태로만 둔다.

일정 연동은 Google Calendar를 사용하며 Apple Calendar 수집·projection·EventKit 쓰기와 Apple profile 생성은 퇴역했다. 기존 Apple 연결을 해제할 때는 `retire-apple-calendar-source`로 먼저 읽기 전용 계획을 조회하고 그 `before_sha256`을 `--expected-settings-sha256`에 전달해 `--apply`한다. 이 adapter는 `sourceProfiles`의 `id: woon-apple-calendar`와 `googleCalendar.sourceProfileIds`의 같은 ID만 제거한다. 다른 profile·계정 설정·Google records·기존 일정 문서·원격 일정은 보존하며, backup·동시 변경 검사·실패 rollback·receipt·디스크 재조회를 수행한다. 이후 앱에서 source 해제와 기존 Google 연결 보존을 확인하는 일은 별도 검증이다. 사용자가 선택한 일반 Markdown source의 Google 동기화는 유지하고 `access: local-only`만으로 막지 않는다. 명시적 `external_sync: deny`가 있는 일정만 전송에서 제외한다. 실제 계정 연결·원격 전송은 승인된 대상과 source 범위에서 수행하고 원격 반영을 따로 확인한다.

승인된 양방향 build의 개인 설정은 `configure-google-two-way-source`로 미리 검토하고 설치·검증 담당이 preview hash를 고정해 적용한다. 이 adapter는 `woon-google-calendar` profile을 `inbox/calendar/google`에 연결하고 기본 속성 mapping·편집 허용과 `googleCalendar.incomingProfileId`, 해당 source 선택만 설정한다. 기존 다른 profile·수신 대상·겹치는 활성 폴더와 충돌하면 덮어쓰지 않는다. 계정·전용 Calendar·records·비밀·기존 문서는 보존하며, 폴더·일정 생성이나 원격 동기화를 실행하지 않는다. backup·lock·동시 변경 검사·실패 rollback·receipt·재조회를 사용한다. 설정 receipt의 `sync_verified: false`는 실제 양방향 반영과 별도이며 현재 설치본의 기능 지원도 대신 증명하지 않는다.

`link-calendar` 정본은 [approved plugins](references/approved-plugins.md)에 등록된 저장소다. 공개 plugin은 folder/tag/property mapping을 설정으로 받고 일반 Markdown 일정 조회와 Google 동기화를 유지한다. Core가 Apple 전용 속성·dashboard·source를 다시 생성하지 않는다. source의 로컬 편집 허용과 Google 전송 허용은 별도 정책이며, 원격 반영은 파일 설치나 로컬 receipt만으로 완료를 주장하지 않는다.

구형 Calendar renderer는 새 plugin의 검증된 설치·활성 config와 실제 UI 검증 뒤 `retire`로 backup 이동한다. 설치 파일 존재만으로 완료하지 않고 Obsidian reload 뒤 ribbon, 월간 화면, 일정 점, 날짜별 시간표, 정본 문서 링크, 읽기 전용 source의 편집 차단을 확인한 다음 `attest-link-calendar-runtime`으로 checklist를 기록한다. 이 operator attestation은 현재 version·asset·settings hash에 묶인다. Apple dashboard나 Apple profile은 요구하지 않는다.

현재 승인된 plugin ID와 공식 release 출처는 [approved plugins](references/approved-plugins.md)에 둔다. 새 plugin은 사용자 승인, Community Plugin 등록 확인, 공식 repository와 manifest ID 일치, release asset hash 검증 규칙을 먼저 추가한 뒤에만 allowlist에 넣는다.
