---
name: archive
description: archive MCP payload·body를 만들거나 private woon-knowledge에 저장·병합할 때 반드시 사용한다. JSON만 요청해도 frontmatter·H1 소유권, canonical 관계 ID, Obsidian 호환 계약을 지킨다.
---

# Archive

## 명시적 Inbox 접수와 완료

사용자가 정리를 요청한 선택 자료만 의미 단위별로 먼저 `woon knowledge intake register --request /path/to/request.json --vault /path/to/vault` 또는 `woon_knowledge_intake(action="register", request=...)`에 등록한다. 일상 대화·고정 여부·일일 projection을 수집 동의로 간주하지 않는다. `source_id`와 안정된 `selection`이 identity이며 content SHA-256 `revision`은 변경 감지다. title·summary·locator를 ID로 쓰지 않는다. 제목은 짧은 명사구, 요약은 해당 의미만 담고 처리 상태 접두사·규칙 설명·보고용 문단은 넣지 않는다. 같은 자료의 제목 수정·재실행은 기존 ID·card 경로·정본 목적지를 유지한다.

기존 정본의 실제 본문을 읽고 의미를 통합할 위치와 결과 bytes를 확정한 뒤 `prepare`로 현재·결과 SHA를 고정한다. 기존 writer의 revision·privacy·approval 계약으로 반영하고 대상·의존 범위 검증 뒤 `complete`에 의미를 검토한 결과 SHA를 전달한다. Python writer는 `run_intake`로 같은 처리 구간을 직렬화할 수 있다. 도구·CLI의 정확한 입력은 [Core Inbox 인터페이스](repo://core/README.md#명시적-inbox-처리)를 따른다. 기존 진행 작업은 승인된 checkpoint를 이어가며 새 Inbox로 소급 등록하지 않는다. 이미 허용된 한 요청을 항목마다 다시 승인받거나 사람이 `prepare`를 눌러야 하는 절차로 바꾸지 않는다.

완료는 대상 제목·hub 링크·옛 완료 문장이 아니라 실제 본문에 선택 자료의 의미가 보존됐는지로 판단한다. 완료 후 생성된 미수정 Inbox card는 제거하고 ID·입력 revision·정본 결과 참조만 남긴다. 중단되면 `status`를 읽어 이미 쓴 Wiki를 다시 쓰지 않고 남은 검증·정리만 이어간다. 사용자가 추가한 내용·미완료 복구 입력·보호 자료·관련성 불명 자료는 지우지 않는다. 완료 항목을 별도 History 문서·raw/clean 쌍·교정 이력으로 늘리지 않는다. Docling 추출물은 별도 변환 ID와 terminal receipt 계약이며 Inbox ID나 기존 content 승인 ID를 대신하지 않는다.

## 원자료와 정본 본문

보존하기로 한 개인 메모는 의미·말투·불확실성·생각 흐름을 유지하며 맞춤법·띄어쓰기·명백한 오타·문장부호를 교정한 본문 하나를 기본으로 한다. 이름·날짜·수치·코드·인용·모호한 의도는 추정해서 바꾸지 않는다. 음성·PDF·사진·제출 문서처럼 증거 역할을 하는 원본 bytes는 그대로 보존한다. 전사문 문장 교정은 원음 검증이나 화자 확인이 아니다. 원자료의 보존·교정과 재사용할 Wiki 의미의 통합은 역할이 다르며, 다음 정본 편집 규칙을 개인 원문 전체의 축약·재작성 권한으로 해석하지 않는다.

먼저 `$knowledge` 방식으로 2~3개 안정적인 keyword를 검색하고 후보 문서 전체와 revision을 읽는다. index missing 또는 stale generation이면 `woon_knowledge_reindex` MCP를 호출하고 동일 검색을 한 번 재시도한다. `woon knowledge index` CLI와 default vault fallback은 금지한다. 제목 유사도가 아니라 같은 질문에 답하는지로 identity를 판단한다.

대화 순서, 반복 질문, 사과, 상태 narration을 제거하고 검증된 사실·결정·예제·한계를 기존 section에 통합한다. MCP body에는 YAML frontmatter와 H1을 넣지 않는다. 이 둘은 adapter envelope의 소유다. `prerequisites`, `next_concepts`, `related`에는 검색·조회로 확인한 slash-separated canonical ID(`domain/slug`)만 넣는다. 제목·표시 이름·검색 keyword를 넣지 말고 ID를 확인하지 못한 관계는 빈 배열로 보낸다. frontmatter와 H1이 필요한 요청은 envelope에서 표현하고 body에는 반복하지 않는다. 새 문서는 `expected_revision` 없이, 기존 문서는 조회한 revision string을 변환하지 않고 넣어 `woon_knowledge_archive_conversation`을 호출한다. conflict가 나면 다시 읽고 병합하며 force overwrite하지 않는다.

호출·예시 payload를 제시할 때도 같은 계약을 적용한다. `purpose`에는 "왜 남기며 어떤 미래 질문·결정·산출물에 재사용할지"를 한 문장으로 쓴다. 전송 전에 `body` 첫 행이 `---`이거나 H1이면 제거하고, 관계 값이 검증된 `domain/slug`가 아니면 빈 배열로 교정한다. 잘못된 예시 요청은 전체를 거부만 하지 말고 알려진 값과 `<required-field>` placeholder로 계약 준수 payload를 반환한다. placeholder는 필수 `canonical_id`·`title`·`domain`·`summary`·`purpose`·`body`에만 쓰고, 미지정 `difficulty`는 `foundation`, 모든 선택 배열은 `[]`로 둔다. 실제 호출에는 placeholder를 절대 전송하지 않는다.

payload 인수는 `canonical_id`, `title`, `domain`, `summary`, `purpose`, `body`, `difficulty`, `prerequisites`, `next_concepts`, `related`, `source_session_ids`, `expected_revision`만 쓴다. `document_id`, `path`, `revision`, `tool` wrapper 같은 alias를 만들지 않는다.

Wiki는 `wiki/` 하나만 정본으로 사용하고 `woon-knowledge/docs/wiki-information-architecture.md`의 계층 계약을 따른다. 대화에서 생긴 이해·결정·프로젝트·자료는 먼저 `canonical_id`·title·aliases·keywords·중심 질문으로 기존 문서를 찾는다. 기존 정체성이면 정확한 `wiki_subject_path`로 같은 문서의 현재 이해·관련 section·시간 이력에 병합한다. 새 정본은 독립 문서 조건과 의미상 `parent`, 대표 `keywords`, `central_question`, `new_wiki_reason`을 모두 확정한 경우에만 만들며, `wiki/personal/`이나 root에 기본 낙하시키지 않는다. 부모나 정체성이 모호하면 Wiki·receipt·cursor를 쓰지 않고 Review로 보낸다. 공개 글·경력 주장·인용처럼 근거 확인이 필요한 입력만 source·accepted claim·page spec을 갱신하고 compiler가 같은 `wiki/` 아래의 근거 문서와 receipt를 만든다.

`콘텐츠` subtree와 Facet은 만들지 않는다. `content_kind: book`은 기존 책을 먼저 찾고, 새 책이면 확인된 장르 키워드 하나를 기존 `Wiki → 책 → 장르 키워드` hub와 정확히 대조한 뒤에만 그 아래 book entity를 만든다. 장르가 없거나 둘 이상이면 Review로 보내며 임시 부모에 붙이지 않는다. 책·장·reader의 화면 계층은 [책 탐색 정본](repo://skills/skills/knowledge/knowledge-navigation/SKILL.md)을 따르며 이미 승인된 목차를 재구성하지 않는다. `2주·1달·5달`, `학습 자료`, `체크포인트`, `다시 열었을 때` 같은 별도 탐색 노드를 만들지 않는다. N.M 절 page가 reader body를 소유하고 실제 N.M.K 하위 항이 있을 때만 subsection direct link를 추가한다. 기존 장 reader 형태는 full coverage replacement와 source-element relocation preflight가 통과하기 전까지 보존한다. 책이 아닌 자료의 의미는 가장 구체적인 기존 Wiki에 병합하고, 안전한 원자료 URL 또는 Vault 내부 source·asset과 기존 `resource_keyword`가 모두 확인된 경우에만 `Wiki → 리소스 → 주제 텍스트 → 들여쓴 원자료 링크` 한 줄을 추가한다. 설명형 content/resource entity는 만들지 않는다.

책 PDF·HTML 원본은 학습 본문과 섞지 않고 `Wiki → 리소스 → 책 원본`의 private source로 보존한다. archive 안의 최상위 파일·디렉터리 이름은 표지·판권·공식 판본 정보로 확인한 실제 책 제목과 판을 사용한다. downloader 접미사, 임의 hash, `압축됨`, `최종`, `사본` 같은 수집 과정 이름을 canonical archive 이름으로 승격하지 않는다. 원래 파일명과 source locator, 교정한 archive 이름, SHA-256과 권리 상태를 catalog에서 함께 보존하며 원본 bytes는 이름 교정 때문에 바꾸지 않는다. 책 학습 Wiki와 원본 리소스는 서로 링크하지만, 원본 저장만으로 학습·적용·숙달 상태를 올리지 않는다.

책 학습 대화를 아카이빙할 때는 먼저 해당 판본의 book·reader unit(N.M 절 page 또는 terminal N.M.K subsection page)과 source coverage manifest를 찾는다. migration 전 장 reader가 current라면 검증된 장 H2 owner를 사용한다. 대화는 원문 기반 설명을 다시 쓰는 입력이 아니라 학습자 보강 입력이다. 질문·오개념·예측·실행 결과·교정은 [책 독자 화면과 개인 각주 계약](repo://skills/skills/knowledge/compile-knowledge/references/book-workflow.md#독자-화면과-개인-각주)에 따라 가장 구체적인 reader unit의 각주에 provenance와 시점을 남겨 연결하고, 이미 있는 원문 주장·예제·목차·이전 보강을 삭제하거나 축약하지 않는다. 일일 대화 취합도 같은 owner page의 identity와 optimistic revision을 사용하며, 반복 질문은 하나의 오개념 설명으로 합치고 새 사실이 없으면 revision을 만들지 않는다. 원문과 대화가 충돌하면 원문·현재 공식 문서·사용자 관찰을 구분해 남기고 자동으로 어느 한쪽을 정답으로 덮어쓰지 않는다.

대화 경로는 요청한 Wiki·일일 기록·검토 후보 반영 범위의 tree·vault·검색 계약을 확인한다. 수집·중복 제거 로직을 바꿀 때는 같은 completed-turn 재실행으로 문서·timeline·색인이 늘지 않는지 검증하고, 단순 기록에는 검증된 writer와 기존 같은 입력의 근거를 재사용한다. Wiki 승격은 source를 해석하는 이 단계에서 한 번만 수행하고, 일일 기록 writer는 이미 확정된 ledger와 정본 링크만 자기 marker에 투영한다. 일일 자유 메모·할 일·Calendar projection을 다시 읽어 Wiki로 승격하지 않는다. 근거 경로는 `woon_knowledge_compile_audit`과 `woon_knowledge_audit`을 실행한다. 두 경로 모두 private 정본이며 현재 요청에서 허용한 범위 밖의 commit, push, publish는 수행하지 않는다. 일기는 사용자의 경험·감정·질문을 보존하며, 사용자가 선택한 부분만 창작 후보나 인물 기록에 연결한다. 다른 사람의 1인칭 문장이나 생성된 자기소개를 사용자의 경험·경력 사실로 채택하지 않는다. 입력 계약은 [MCP contract](references/mcp-contract.md)를 필요할 때만 읽는다. 이 스킬은 `repo://skills/skills/knowledge/archive`의 단일 원본이며 knowledge 저장소에 복사하지 않는다.

외부 폴더나 저장소의 여러 문서를 전수 처리하는 요청은 `$ingest`가 파일별 catalog·privacy·완전성을 먼저 소유하고, 실제 canonical 한 편 저장 단계에서만 이 스킬의 계약을 호출한다.

독자가 다시 읽을 학습·설명 본문을 새로 만들거나 크게 고칠 때만 아래 명령으로 quality gate, 범용 Wiki writing harness, 표본 근거를 함께 읽는다. 짧은 기록 교정·metadata·링크·Inbox 상태 처리에는 전체 harness를 다시 읽지 않는다. 주제에 맞는 route를 고르고, purpose·source·claim·page·receipt·visibility·재열람 질문을 분리한다. code·실행 근거·인과·개념·한계는 필요한 경우에만 사용하며, 대화에 없던 실행 결과·사실·의도를 만들지 않는다.

```bash
bash "$(woon resolve repo://skills/skills/writing/tech/scripts/learning-context.sh)"
```

새롭거나 크게 고친 학습 본문은 compiler 통과만으로 문체 품질이 보장되지 않는다. 해당 page의 receipt hash가 포함된 content quality review를 갱신하고 `$compile-knowledge`의 `evaluate-quality` gate가 전체 current payload를 통과하기 전까지는 "문서 품질 검증 완료"라고 말하지 않는다.

Obsidian·Quartz 표시, wikilink, callout, `.base`·`.canvas` 경계가 관련되면 `woon resolve repo://skills/standards/obsidian-compatibility.md`를 읽는다.
