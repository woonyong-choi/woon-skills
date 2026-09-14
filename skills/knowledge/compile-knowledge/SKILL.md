---
name: compile-knowledge
description: private woon-knowledge의 LLM Wiki source·claim·page spec·receipt를 추가·수정·감사·컴파일할 때 사용한다. catalog/llm-wiki 변경이나 receipt 불일치·stale 검색 복구에 사용한다.
---

# Compile Knowledge

새로 선택한 정리 자료는 `$archive`의 명시적 Inbox 접수·원자료 정책을 먼저 적용하고, 기존 개발 Wiki 이관은 현재 writer의 checkpoint를 이어간다. 개인 메모의 허용된 교정과 immutable 증거 bytes를 구분한다. `archived/superseded` identity는 유지하되, 명시적으로 승인된 공개 생성 revision의 본문 축소는 [Core Inbox 인터페이스의 source-body-plan](repo://core/README.md#명시적-inbox-처리)으로 검토·고정한 replacement만 공유 writer가 적용한다. 이는 일반 원문 삭제 권한이 아니며 보호 자료·비공개 source·책·현재 참조·미완료 복구 입력은 보존한다. compact source의 `body_retention`은 본문 부재를 표시하고 원문 복구·근거 재검증을 주장하지 않는다.

`wiki/`는 Woon의 단일 지식 정본이며 모든 페이지가 `woon-knowledge/docs/wiki-information-architecture.md`의 `canonical_id`·`node_kind`·`parent`·`keywords`·`view_mode` 계약을 따른다. 그중 `catalog/llm-wiki/pages.yaml`이 소유한 근거 본문만 compiler 산출물이며 source, accepted claim, page spec으로 갱신하고 Markdown 출력·receipt를 직접 고치지 않는다. 대화·프로젝트 문서는 같은 Wiki 안에 있지만 conversation-to-Wiki 경로가 관리하므로 compiler page로 복제하거나 덮어쓰지 않는다. Core가 생성하는 `woon-wiki-overview`, `woon-wiki-children`, `woon-wiki-latest`, `woon-wiki-timeline` block은 같은 파일의 파생 view이며 compiler projection과 receipt 입력에서 제외한다.

사용자가 별도의 private reader 작성을 지시한 책은 기존 책 입구에서 실제 private Markdown index를 여는 단일 navigation 링크를 둘 수 있다. 이는 책 본문 편입이나 source coverage 승격이 아니며 기존 목차·identity·부모·비공개 상태를 보존한다. 단일 일반 Markdown 링크의 대상 실존과 private 경계는 Core의 공통 reader target 검증을 사용하고, 빈 책 map 본문 규칙도 이 navigation 링크를 허용한다. 연결을 위해 독립 reader를 compiler 책 본문으로 복제하거나 전권의 옛 하위 트리를 복구하지 않는다. 적용은 현재 writer가 revision·receipt가 고정된 기존 transaction과 관리 목록의 scoped refresh로 수행한다.

1. 먼저 `$knowledge`로 기존 canonical 문서와 관계 ID를 확인한다. 대화 한 건을 정본에 저장하는 일은 `$archive`, 외부 corpus 전수 수집은 `$ingest`에 넘긴다.
2. source body 또는 claim Markdown을 새로 쓰거나 고쳐 독자가 읽을 설명을 바꿀 때는 먼저 아래 명령으로 `$tech`의 learning harness를 읽는다. hash·receipt·관계만 고치는 변경에는 이 단계를 적용하지 않는다.

```bash
bash "$(woon resolve repo://skills/skills/writing/tech/scripts/learning-context.sh)"
```

3. 변경할 `catalog/llm-wiki/sources.yaml`, `claims.yaml`, `pages.yaml`을 읽고 [compiler contract](references/compiler-contract.md)의 필수 필드와 privacy 규칙을 적용한다. 원본은 덮어쓰지 않으며 locator에 머신 절대 경로·secret·private 원문을 넣지 않는다.

책 source·번역·coverage·reader tree를 처리할 때만 [책 편입 계약](references/book-workflow.md)을 읽는다. 판본·권리·원문 보존·단일 writer와 검증된 phase의 증분 적용을 유지한다.

4. 새 source에는 원문 hash, 보존 본문, 그리고 "왜 보존하는가 / 어떤 미래 질문·결정·산출물에 쓸 것인가"를 한 문장으로 쓴 nonempty `purpose`를 둔다. legacy-wiki 이관본은 당시 목적을 추정해 덧쓰지 않는다. 대신 `curation.yaml`의 `current_use`에 지금 이 문서를 학습·설명·검색에 쓰는 이유를 적고, 그 근거(`basis`)와 확정 여부(`status`)를 남긴다. `current_use`는 현재 운영 판단이지 과거 source intent가 아니다. claim은 해당 source ID와 채택 근거, page spec은 한 output path와 현재 source/claim 집합을 가진다. 같은 conversation 문서를 갱신하면 기존 원문·claim을 지우거나 다시 렌더하지 말고 `archived/superseded`와 후속 ID로 이력을 남긴다. public page에는 public provenance만 연결한다. 미확인 주장·충돌은 `review-queue.yaml`에 남기고 accepted claim으로 만들지 않는다.
5. `woon_knowledge_compile`을 호출한다. 직접 Markdown 변경 또는 receipt 오류가 있으면 source/claim/page spec을 고친 뒤 다시 컴파일한다. `--force`는 compiler 변경 또는 receipt 전체 재생성이 필요한 경우에만 쓴다.

기존 compiler catalog에 `curation.yaml`이 아직 없으면, 첫 전환에서만 아래 명령으로 빈 historical purpose를 건드리지 않고 모든 page spec의 provisional current-use record를 만든다. 이 명령은 기존 curation을 덮어쓰지 않는다.

```bash
woon knowledge initialize-curation --vault <vault>
```

자동 문구의 생성 규칙을 고쳤거나 기존 페이지에 새 curated·archive source를 연결했을 때는 `legacy-page-metadata`와 `provisional`인 record만 아래 명령으로 갱신한다. 이 명령은 direct source가 전부 legacy인지 다시 확인해, `curated-wiki`가 있으면 `manual-review/confirmed`, legacy가 없는 새 source만 있으면 `archive-request/confirmed`로 바로잡는다. 이미 `manual-review` 또는 `confirmed`인 record는 이 명령이 바꾸지 않는다.

```bash
woon knowledge refresh-provisional-curation --vault <vault>
```

과거 archive 구현이나 중단된 작업 때문에 현재 page spec에 속하지 않는 conversation source·claim이 남았고, 같은 locator의 현재 successor가 하나로 확인되면 아래 명령으로 비파괴 이력으로 정규화한다. 서로 다른 locator이거나 successor가 여럿이면 자동으로 고르지 않고 audit 오류로 남긴다.

```bash
woon knowledge reconcile-superseded-revisions --vault <vault>
```
6. compile 뒤 변경 대상과 의존 범위의 Core Wiki view·receipt·검색을 확인한다. 공유 catalog는 현재 revision을 고정한 단일 writer transaction으로 반영하며 지원되는 scoped audit을 사용한다. 전체 공개·정본 전환에는 전체 `woon_knowledge_compile_audit`과 `woon_knowledge_audit`을 유지한다. 범위 검증이 지원되지 않는 경로에서는 우회해 성공 receipt를 만들지 않는다. receipt의 `compiler_projection_sha256`은 source·claim·page spec이 소유하는 compiler 본문을 검증하고, `output_sha256`은 해당 compile 시점의 전체 파일을 추적한다. Core 관리 block이 정상 갱신돼 전체 파일 hash가 달라져도 compiler projection이 재현되면 stale이 아니다. marker 밖의 compiler 본문 변경은 계속 오류다. source 변경 뒤 search가 stale이면 compile, Wiki view refresh, reindex 순서로 실행한다. 반영 대상과 의존 범위의 compiler 입력·출력·tree view·index가 current인지 확인한 범위만 완료로 보고한다.
7. 독자가 읽는 학습 본문을 새로 쓰거나 고쳤다면, 현재 receipt `output_sha256`와 writing harness hash를 함께 담은 quality review payload를 갱신하고 아래 gate를 실행한다. 한 페이지라도 누락·보류·stale이면 compiler 정합성은 통과해도 문서 품질은 미검증으로 보고한다.

```bash
woon knowledge evaluate-quality \
  --vault <vault> \
  --reviews <content-quality-reviews.json> \
  --standard "$(woon resolve repo://skills/standards/learning-writing-harness.md)" \
  --prompt "$(woon resolve repo://skills/standards/learning-quality-review-prompt.md)"
```

전체 corpus 품질 평가나 기존 결과를 재사용할 때만 [품질 평가 실행](references/quality-review-workflow.md)을 읽는다. immutable plan과 현재 receipt를 대조하고 바뀐 batch만 다시 평가한다.

컴파일 실패 시 output 파일을 수동 복구하지 않는다. Git diff로 source catalog 변경을 검토하고 필요한 입력만 되돌린 후 재컴파일한다. 자동 commit, push, publish는 하지 않는다.
