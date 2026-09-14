# 관리 companion 연결

이 절차는 승인된 로컬 companion 시작·pairing 담당이 사용한다. Core 구현 작업은 코드와
격리 테스트, 읽기 전용 시작 preview까지만 수행한다. `Run`과 책 코드는 호출하지 않는다.
실제 적용 권한이 이미 주어졌으면 재승인을 요구하지 않고 아래 검증을 수행한다.

## 시작

정확한 release와 artifact SHA-256, loopback port, 필요한 기존 image digest는
`repo://core/config/runnable-companion.yaml`에서 읽는다. `--companion-cli`에는 그 SHA와
일치하는 지속적인 build artifact 경로를 사용한다. 설치된 Node 22 이상과 로컬 Unix socket의
Docker engine, digest로 고정한 Kotlin image가 필요하다. 이 adapter는 설치·pull을 하지 않는다.

```bash
woon knowledge obsidian-plugin start-runnable-companion --vault /path/to/vault \
  --companion-cli /path/to/local-runner/dist/runnable-code-blocks-local-runner.mjs \
  --node-cli /path/to/node --docker-cli /path/to/docker
woon knowledge obsidian-plugin start-runnable-companion --vault /path/to/vault \
  --companion-cli /path/to/local-runner/dist/runnable-code-blocks-local-runner.mjs \
  --node-cli /path/to/node --docker-cli /path/to/docker \
  --apply --expected-state <start-preview-expected-state>
woon knowledge obsidian-plugin runnable-companion-status --vault /path/to/vault
```

preview와 apply는 같은 입력을 다시 확인한다. settings·config·managed state·정책·실행 도구가
바뀌면 새 preview가 필요하다. `remoteExecutionEnabled: false`가 디스크에 있어야 시작한다.
기존 `~/.config/runnable-code-blocks/local-runner.json`은 호환되는 owner-only 파일일 때
bytes와 token을 그대로 쓴다. 없을 때만 owner-only config와 무작위 token을 만든다.
다른 port·잘못된 config·symlink·권한 충돌은 보존하고 실패한다.

Node CLI가 Volta 등의 shim이면 `process.execPath`로 실제 실행 파일을 해석하고 그 파일의
경로·hash·version을 preview에 고정한다. 실제 파일을 직접 시작해 `Popen.pid`와 listener
PID가 일치하게 한다. shim의 종료를 실제 Node 자식의 종료로 간주하지 않는다.

정확한 artifact를 Vault의 private 관리 폴더에 보관하고 그 사본의 `start`만 실행한다.
upstream이 token을 출력하므로 stdout·stderr는 폐기한다. token을 argv·로그·receipt로
복사하지 않는다. 기존 `RCB_*` override와 `NODE_OPTIONS`는 자식에서 제외한다.
`127.0.0.1:17171`의 소유한 PID·시작 시각/명령·artifact hash를 확인한 뒤에만 인증된
`GET /v1/capabilities`를 요청한다. 다른 프로세스가 port를 사용하면 연결하거나 중단하지 않는다.

같은 관리 프로세스가 준비됐으면 재사용한다. 새 프로세스의 시작 실패는 이번 호출이 만든
자식만 종료하고 소유한 파일만 복구한다. 모든 시작 시도는 config 생성 전에 pending attempt를
남기고 spawn한 PID를 기록한다. 자식 종료와 별개로 listener 부재를 다시 확인해야 이번에
만든 config를 복구 제거할 수 있다. 남은 listener나 확인 실패가 있으면 config를 보존하고
실패 attempt에 PID와 listener를 남기며 자동으로 다시 시작하지 않는다. `17172`, 기존 gateway·터널·launchd에는
관여하지 않는다. 이 companion은 detached process이며 로그인/재부팅 자동 시작을 등록하지 않는다.

## 관리 프로세스 교체

기존 시작 receipt가 있는 프로세스는 `stop-runnable-companion`으로만 종료한다.
담당자 한 명이 stop/start를 수행하고, 화면 담당은 교체 인계까지 새 Run을 보류한다.
기존 정책의 artifact hash를 유지한 상태에서 정확한 현재 PID를 preview한다.

```bash
woon knowledge obsidian-plugin stop-runnable-companion --vault /path/to/vault \
  --pid <exact-managed-pid> --docker-cli /path/to/docker
woon knowledge obsidian-plugin stop-runnable-companion --vault /path/to/vault \
  --pid <exact-managed-pid> --docker-cli /path/to/docker \
  --apply --expected-state <stop-preview-expected-state>
```

adapter는 성공한 원래 start receipt와 state의 bytes 일치, 현재 사용자·프로세스 signature·
Vault cwd·유일한 loopback listener·원래 로컬 Docker engine을 확인한다. 자식 프로세스,
열린 TCP 연결, `rcb-` 컨테이너가 하나라도 남으면 중단하지 않는다. 이는 OS와 컨테이너의
관찰 결과이며 서버의 원자적인 drain 보장은 아니다. SIGTERM 직전에 다시 확인하고 그 PID
하나만 종료한다. 확인 실패 시 강제 종료나 다른 프로세스로 확대하지 않는다.

PID 종료와 port 해제를 확인한 뒤에만 성공 receipt를 남긴다. config·token·settings와 이전
state·artifact·start receipt는 복구 입력으로 보존한다. 성공 후에만 승인된 새 artifact SHA를
정책에 고정하고 start preview/apply를 수행한다. 새 시작이 실패하면 자동 재시도하지 않고
attempt를 확인한다. 이전 정책과 보존 artifact를 사용한 별도 start preview가 복구 경로다.
`17172` gateway와 pairing은 변경하지 않는다. 실제 책 Run 검증은 화면 담당에게 인계한다.

## 시작 실패로 남은 orphan 복구

관리 state가 없는 상태에서 `17171`을 점유한 프로세스가 남으면 등록된 복구 adapter의
preview를 사용한다. 임의 kill·process group 종료·config 재작성으로 우회하지 않는다.

```bash
woon knowledge obsidian-plugin recover-runnable-companion-orphan --vault /path/to/vault \
  --pid <exact-observed-orphan-pid>
woon knowledge obsidian-plugin recover-runnable-companion-orphan --vault /path/to/vault \
  --pid <exact-observed-orphan-pid> --apply --expected-state <recovery-preview-expected-state>
woon knowledge obsidian-plugin runnable-companion-status --vault /path/to/vault
```

복구 대상은 현재 사용자의 PPID=1인 orphan이며 유일한 loopback listener여야 한다.
관리 artifact 경로·SHA-256·프로세스 시작 시각과 명령 signature·PGID·Vault cwd·config와
settings hash가 preview에 묶인다. apply가 모두 다시 확인한 뒤 **그 PID 하나**에 `SIGTERM`을
한 번 보낸다. process group·다른 PID에는 신호를 보내지 않고 강제 종료로 확대하지 않는다.
PID 종료와 빈 port를 확인해야 성공 receipt를 남긴다. 기존 config와 settings는 그대로
보존한다. 실패에는 attempt만 남기며 자동 재시도하지 않는다. 성공 후 새 start preview를
만들어 실제 Node 경로와 새 expected_state로 진행한다. 복구에는 token·HTTP 요청이 없다.

## Pairing

설치·화면 담당이 승인된 plugin version의 로드와 정확한 Vault가 이미 열려 있음을 먼저
확인한다. [공식 Obsidian CLI](https://help.obsidian.md/cli)는 닫힌 앱을 시작할 수 있으므로
앱이 닫힌 상태에서는 pairing preview도 호출하지 않는다.

```bash
woon knowledge obsidian-plugin pair-runnable-companion --vault /path/to/vault \
  --obsidian-cli /path/to/obsidian --vault-name <running-vault-name-or-id>
woon knowledge obsidian-plugin pair-runnable-companion --vault /path/to/vault \
  --obsidian-cli /path/to/obsidian --vault-name <running-vault-name-or-id> \
  --apply --expected-state <pair-preview-expected-state>
woon knowledge obsidian-plugin runnable-companion-status --vault /path/to/vault
```

Core가 등록된 CLI `eval`을 통해 exact Vault·window·plugin version·asset와 settings hash를
확인한다. 스크립트가 검증한 config에서 token을 읽어 공개 `SecretStorage` API의
`runnable-code-blocks-local-runner-token` 하나만 처리한다. 기존 값이 같으면 재사용하고,
다르면 덮어쓰지 않는다. plugin의 `localRunnerSecretId`가 다른 ID를 선택한 경우에도
보존하고 실패한다. 이 adapter가 임의로 선택을 바꾸지 않는다. 전체 SecretStorage나 사용자
token을 출력하지 않는다.

원본 settings bytes를 backup한 뒤 local=false로 준비하고 token을 설정한다. 다음으로
local=true·endpoint=`http://127.0.0.1:17171`·remote=false를 적용하고 `loadSettings()`만
호출한다. legacy/path와 다른 설정은 보존한다. `saveSettings()`·availability refresh·reload·
코드 실행은 호출하지 않는다. 별도 읽기 전용 CLI 조회와 companion readiness 재조회가
성공해야 pairing 성공 receipt를 남긴다. Run 버튼의 화면 상태는 담당이 따로 확인한다.

후속 단계가 실패하면 소유한 설정의 local·remote를 false로 두고 다른 설정은 복구한다.
동시 편집은 덮어쓰지 않으며 그 경우 `concurrent_settings_preserved`를 기록한다. 공개
SecretStorage에는 delete API가 없으므로 새로 등록한 token은 pending으로 남을 수 있다.
raw DB를 수정하거나 빈 문자열 쓰기로 삭제를 흉내 내지 않는다. 실패 attempt의
`local_disk_disabled`·`runtime_disable_verified`·`secret_state`를 확인한다. 실패를 성공으로
표시하지 않고, 원인을 해결한 뒤 새 preview에서 같은 token을 재사용한다.

## 증거와 확인 범위

- 시작 receipt와 `.local/woon-knowledge/obsidian-plugins/companion/state.json`은 소유한
  PID·artifact·config hash·capabilities를 연결한다. token 값은 없다.
- pairing receipt는 `.local/woon-knowledge/obsidian-plugins/receipts/<id>.json`에 별도로
  남고 backup·before/after settings hash·asset hash·별도 runtime 재조회를 연결한다.
- `companion/attempts/<id>.json`은 pending/실패 상태다. `verified-awaiting-receipt`도 같은
  ID의 성공 receipt가 없으면 완료 증거가 아니다.
- `runnable-companion-status`의 `ready`는 companion 상태다. plugin의 pairing과 화면,
  실제 코드 결과를 대신 증명하지 않는다. 적용 담당이 허가된 고정 non-book smoke를 별도로
  한 번 실행하고 그 실행 receipt를 연결한다. 이 절차가 책 코드 실행을 허가하지 않는다.
