# vendor/ecc 로컬 변경 기록

`docs/architecture.md`와 `docs/operations.md`는 "vendor 본문을 직접 고치지 않는다"고 쓰고 있다.
실제 트리는 그 계약에서 벗어나 있다. 이 파일은 **무엇이 upstream과 다른지, 왜 그런지**를 남긴다.
출처·라이선스는 `vendor/ecc/NOTICE`에 있다.

기준: upstream `7d12022ddd708181633f50b92aafc1f6c6f05321`.

재현:

```bash
git clone --depth 1 https://github.com/Jungle-12-303/skills.git /tmp/ecc-up
diff -rq /tmp/ecc-up ~/workspace/woon/woon-skills/vendor/ecc \
  --exclude=.git --exclude=.gitignore --exclude=NOTICE --exclude=PATCHES.md
```

## 1. 가져오지 않은 것 (import 시점부터)

| 대상 | 이유 |
| --- | --- |
| `README.md` | upstream 저장소 안내문. vendor 트리에 둘 이유가 없다. |
| `commit-convention/` | Woon이 `skills/git/commit`으로 정본을 소유한다. |
| `github/` | Woon이 `skills/github/` 아래에서 정본을 소유한다. |
| `skill-syncer/` | Woon은 profile·catalog로 설치를 관리한다. |

upstream 185개 중 3개를 빼서 183개다.

## 2. description 예산 준수 재작성 — 9개 파일

커밋 `b18eac1` (2026-08-06, `fix: web profile description 예산 준수`).
`SKILL.md` frontmatter의 `description:` **한 줄만** 짧게 고쳤다. 본문·스크립트는 그대로다.

`context-budget`, `docker-mounted-workspace`, `documentation-lookup`, `frontend-design`,
`knowledge-ops`, `repo-scan`, `skill-comply`, `terminal-ops`, `three-persona-multi-agent-review`

## 3. 상태 기호를 글자로 교체 — 10개 파일

커밋 `5a808da` (2026-09-22, `chore(vendor): replace status glyphs with plain words`).
공개 저장소가 이모지를 싣지 않는다는 규칙에 따라 체크 표시(U+2713) 59건 → `OK`,
엑스 표시(U+2717) 10건 → `FAIL`로 바꿨다. 예시 출력과 `console.log` 문자열뿐이라 동작은 바뀌지 않는다.

`benchmark/SKILL.md`, `browser-qa/SKILL.md`, `canary-watch/SKILL.md`,
`ck/commands/{forget,migrate,save}.mjs`, `click-path-audit/SKILL.md`,
`django-verification/SKILL.md`, `rules-distill/SKILL.md`, `skill-stocktake/SKILL.md`

## 4. machine-specific 절대 경로 제거 — 1개 파일

커밋: 이 기록과 같은 커밋.

`github-issue-manager/SKILL.md`의 `## 빠른 사용법` 예제 5줄이 upstream 작성자의 설치 경로
`/Users/<사용자>/workspace/skills/github-issue-manager/scripts/issue_manager.py` 형태를 그대로 쓰고 있었다
(홈 경로는 이 기록에서도 commit하지 않으려고 가렸다. 원문은 upstream `7d12022` 의 같은 파일에 있다).
`README.md`의 "machine-specific 절대 경로는 commit하지 않고"와 정면으로 어긋나서 고쳤다.

- 5줄 모두 `"$WOON_ROOT"/woon-skills/vendor/ecc/github-issue-manager/scripts/issue_manager.py`로 교체.
- `$WOON_ROOT`의 뜻과 실행 위치를 설명하는 1줄을 `## 빠른 사용법` 바로 아래에 넣었다.
  `scripts/common.py:136`의 `repo_root()`가 `git rev-parse --show-toplevel`로 저장소를 찾고
  `issue_manager.py:41`이 경로를 `Path.cwd()` 기준으로 해석하므로, 명령은 **대상 프로젝트 저장소
  안에서** 실행해야 한다. 그래서 스킬 디렉터리 기준 상대경로(`python3 scripts/...`)는 쓸 수 없다.

오버레이(패치 적용 단계)로 처리하는 편이 vendor 불변 계약에 맞지만, 이 저장소에는 그런 장치가 없다.
설치는 profile이 파일을 그대로 복사하는 방식이다. 장치를 새로 만드는 것보다 vendor 파일을 고치고
여기에 기록하는 쪽을 택했다. §3에서 이미 같은 선례가 있다.

## 벗어난 계약

`docs/architecture.md:21`과 `docs/operations.md:18`의 "직접 수정하지 않습니다"는 §2 시점부터 사실이
아니었다. 문서를 트리에 맞추거나 트리를 문서에 맞추는 것은 별도 결정 사항이다. 여기서는 사실만 남긴다.
