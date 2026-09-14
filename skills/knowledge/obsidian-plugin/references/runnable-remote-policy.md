# Runnable 원격 실행 차단의 runtime 반영

Core의 `disable-runnable-remote-execution`은 디스크의 `remoteExecutionEnabled`만 `false`로
바꾼다. 실행 중인 plugin은 이전 settings 객체를 유지할 수 있으므로 설치·화면 담당이 아래
절차로 확인한다. pairing·companion 배포·runner 실행은 이 절차에 포함하지 않는다.

1. 이미 실행 중인 정확한 Vault를 대상으로 Core adapter의 preview와 hash-pinned apply를
   수행한다. 반환한 receipt ID·`sha256`·plugin version·asset hash를 유지한다.
2. [공식 Obsidian CLI](https://help.obsidian.md/cli)의 `eval`을 사용한다. Vault 이름 또는 ID를
   첫 매개변수로 지정한다. 앱이 닫혀 있으면 CLI가 앱을 시작하므로 닫힌 앱에서 호출하지 않는다.
3. 아래 JavaScript의 placeholder 두 개를 실제 Vault 경로와 적용 receipt의 `sha256`으로
   치환한다. `loadPolicy = true`로 한 번 실행한 뒤 **`false`로 별도 실행**해 읽기 전용으로
   재조회한다. CLI에는 `code=<JavaScript>`를 하나의 인자로 전달한다. Python subprocess를
   사용한다면 `[cli_path, "vault=" + vault_name_or_id, "eval", "code=" + code]`를 넘기며
   shell 문자열에 코드를 보간하지 않는다.

```javascript
(async () => {
  const expectedVault = "<actual-vault-absolute-path>";
  const expectedSettingsSha256 = "<applied-receipt-sha256>";
  const loadPolicy = true; // 두 번째 호출에서는 false: 읽기 전용 재조회
  if (app.vault.adapter.getBasePath() !== expectedVault) {
    throw new Error("Unexpected Vault; no policy loaded");
  }
  const plugin = app.plugins.getPlugin("runnable-code-blocks");
  if (!plugin || typeof plugin.loadSettings !== "function") {
    throw new Error("Runnable plugin is not loaded or cannot read settings");
  }
  const raw = await app.vault.adapter.read(".obsidian/plugins/runnable-code-blocks/data.json");
  const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(raw));
  const settingsSha256 = Array.from(new Uint8Array(bytes))
    .map(value => value.toString(16).padStart(2, "0")).join("");
  if (settingsSha256 !== expectedSettingsSha256 || JSON.parse(raw).remoteExecutionEnabled !== false) {
    throw new Error("Disk policy changed or remote execution is not disabled");
  }
  if (loadPolicy) await plugin.loadSettings();
  if (plugin.settings.remoteExecutionEnabled !== false) {
    throw new Error("Loaded plugin has not disabled remote execution");
  }
  return JSON.stringify({
    action: loadPolicy ? "load-runnable-remote-policy" : "read-runnable-remote-policy",
    plugin_id: plugin.manifest.id,
    version: plugin.manifest.version,
    settings_sha256: settingsSha256,
    remote_execution_enabled: plugin.settings.remoteExecutionEnabled,
    policy_loaded: loadPolicy,
    read_only: !loadPolicy
  });
})()
```

현재 Runnable의 `loadSettings()`는 `loadData()`와 `normalizeSettings()`만 호출하고,
runner registry는 `this.settings`를 동적으로 읽는다. 대상 build의 이 동작을 확인한 뒤
위 절차를 사용한다. `saveSettings()`는 다른 설정을 다시 쓰고 availability를 갱신하므로
사용하지 않는다. plugin/window reload, `Run`, runner/health 요청도 호출하지 않는다.

설치·검증 담당은 두 CLI 결과를 기존 설정 receipt ID에 연결한 별도 runtime receipt로 남긴다.
디스크 receipt를 수정하지 않고, 재조회가 성공했을 때만 `runtime_policy_verified: true`를
기록한다. 전체 settings·token·SecretStorage 값은 출력하거나 receipt에 넣지 않는다.
CLI 오류나 미응답은 runtime 확인 실패로 남기고 같은 로드를 자동 반복하지 않는다.
remote가 차단됐다는 사실은 local 실행이나 companion 연결이 준비됐다는 뜻이 아니다.
