---
name: knowledge-navigation
description: Woon Wiki의 단일 계층형 키워드 트리, 하위 문서 색인, 엔티티별 성장 구조와 Obsidian Graph·Canvas 파생 화면을 설계·검증할 때 사용한다. 고아 문서, 중복 키워드, 별도 Map, 모호한 부모를 진단하는 요청에 적용한다.
---

# Knowledge Navigation

`$knowledge-navigation`은 `woon-knowledge/docs/wiki-information-architecture.md`를 실행하는 절차다. 사람이 읽고 AI가 검색하는 지식·질문·탐색 순서의 정본은 `wiki/**/*.md`뿐이다. 먼저 `$knowledge`로 기존 정체성을 찾고, 실제 기록은 `$archive` 또는 `$compile-knowledge`로 반영한다.

## 단일 트리 계약

새 정리 요청은 `$archive`의 명시적 Inbox 접수에서 시작한다. Inbox에는 미처리 의미 단위를 짧은 제목과 요약으로 보여 주고, 검증된 통합 뒤에는 정본으로 이동해 읽는다. 별도 완료 History·처리 규칙 문단·상태 접두사를 탐색 체계에 추가하지 않는다. title은 표시, canonical ID와 검증된 parent는 정체성이므로 화면 이름을 다듬는 작업으로 ID·URL·파일 경로를 일괄 변경하지 않는다.

1. `wiki/README.md`만 root다. 모든 활성 Wiki 문서는 root에서 `parent` 하나를 따라 도달해야 한다.
2. 부모는 폴더가 아니라 의미로 선택한다. `parent_topics`, `parent_moc`, `map_role`, `mindmap_role`로 병렬 계층을 만들지 않는다.
3. `canonical_id`, title, aliases, keywords, 중심 질문을 함께 대조한다. 같은 질문이면 기존 문서의 section을 갱신하고, 독립된 중심 질문·고유 근거 또는 이력·둘 이상의 재사용 맥락 중 하나가 있을 때만 새 child를 만든다.
4. 새 child는 `parent`, 대표 `keywords`, `central_question`, 생성 이유를 확정할 수 있을 때만 만든다. 부모가 모호하면 root에 임시로 붙이지 않고 Review로 보낸다.
5. 기본 Map은 `# 페이지 제목 → ## 주제 키워드 → - [[직접 하위 링크]]`로 보여 준다. 주제 키워드를 일반 불릿이나 wrapper link로 만들지 않고 H2로 둔다. 같은 화면에는 직접 하위 링크만 평평한 불릿으로 표시하며 손자 이하를 펼치지 않는다. 아래 인물 초성 인덱스는 H2 대신 일반 불릿 묶음을 쓰는 표시 예외이며, 인물 entity 본문은 아래의 대표 키워드·사건 불릿 형식을 따른다. `navigation_groups`가 H2 주제와 direct child 순서를 소유한다. 한 페이지에서는 장르·목적·관계·진행 단계 중 하나의 분류 축만 사용하고, 포함 관계가 겹치는 label은 대표 label 하나로 합친다. 모든 direct child는 정확히 한 그룹에 있어야 하고 그룹당 링크가 20개를 넘으면 안 된다. 전체 subtree·최신 목록·summary·상태·개수는 펼치지 않는다.
   책은 사용자가 승인한 독서 흐름을 따르며 첫 목차에서 실제 본문을 원문 순서로 연다. 장·절 자체에 실제 개요·서문 본문이 있으면 상위 제목 자체를 그 본문 링크로 표시하고, 별도 `도입`이나 동명 첫 하위 항목을 만들지 않는다. 자체 본문이 없는 상위 항목은 링크 없는 키워드와 하위 목록만 표시하며, 하위 항목 없는 실제 본문은 링크 한 줄로 둔다. 책마다 다른 예외나 고정된 3단계 깊이를 강제하지 않는다. 본문 유무는 원문·source element·실제 내용으로 확인하며 길이, 단순 절 안내문이나 제목 OCR 잔재로 추정하지 않는다. 실제 개요·서문·본문·코드·그림과 source coverage를 보존하고, 표지·판권·목록뿐인 wrapper를 다시 생성하지 않는다. 검증된 inbound·이전/다음 링크를 실제 본문이나 책 목차의 해당 anchor로 바꾸고 필요한 source coverage owner를 exact-once 옮긴 뒤 무내용 wrapper를 퇴역한다. 같은 목차 형태에는 Wiki와 private reader가 같은 Core renderer를 사용한다. 번호·순서·개인 각주와 공개 경계를 보존하고 요청 밖의 책 구조나 본문을 바꾸지 않는다. 언어는 작품의 최초 출판 언어가 아니라 사용자가 제공한 source 판본의 언어로 판정한다. 제공 판본이 한국어인 책은 원문을 최대한 그대로 보존하며 `humanize`나 문체 재작성의 대상이 아니다. 원문과 대조해 확인한 OCR 오류와 사용자가 요청한 목차·링크·그림만 수정한다. 문장 자연화는 승인된 번역문에만 적용하며, 현재 교정 범위는 사용자가 제공한 Kotlin in Action 영문에서 만든 한국어 번역문이다. LLM·DL1의 제공 PDF는 한국어이므로 원문 보존 대상이다. 다른 책으로 교정 범위를 확대하지 않는다. 번역문도 인용·기술 내용의 원뜻과 출처를 보존하며, 제공된 한국어판을 AI가 만든 번역문으로 오분류하거나 작품의 최초 출판 언어를 이유로 다시 교정하지 않는다.
6. `aliases`는 같은 정체성의 다른 이름, `related_to`는 비교·원인·사례·사용 같은 횡단 관계다. 둘 다 기본 부모를 대신하지 않는다. 공개 검색에 필요한 이전 표기와 관련 검색어는 `public_search_terms`에 명시하며, 검색어가 같다는 이유로 다른 개념을 동의어로 합치지 않는다.
7. 순서는 탐색 의미다. root의 순서는 실제 `wiki/README.md`의 승인된 `navigation_groups`가 소유하고, 기술 개념은 가까운 선수·응용 주제를 붙인다. 그룹 안에서는 선수 개념·작업 흐름·가나다순·날짜순 중 하나를 일관되게 적용한다. `navigation_groups`가 있으면 group과 `children` 배열이 사람 화면과 AI 문맥의 순서를 함께 소유하고, `sequence`는 명시적 인덱스 예외와 단일 child의 fallback만 소유한다. 아래 인물 이름순 인덱스는 실제 title을 사용한다. 파일명 자동 정렬에 맡기지 않는다.

개발 분야의 경계와 이름은 [공개 Wiki의 키워드와 문서](repo://knowledge/docs/wiki-information-architecture.md#3-공개-wiki의-키워드와-문서)를 따른다. 분류·표시명을 바꾸면 안정된 canonical ID·URL·원문·기존 날짜를 보존하면서 `parent`, `public_parent_id`, `identity_scope`, 경로를 포함한 `central_question`, Home 안내와 `public_taxonomy`를 같은 반영 구간에서 맞춘다. 공개 문서를 통합할 때는 옛 URL이 대표 정본으로 연결되는 발행 경로까지 확인한다.

## 페이지와 엔티티

- 탐색 페이지는 기본적으로 `H1 제목 → H2 주제 키워드 → direct child 링크 불릿`으로 읽으며 인물 초성 인덱스는 아래 표시 예외를 따른다. `navigation_groups`는 표시 순서일 뿐 새 정체성이나 두 번째 parent를 만들지 않는다. 실제 하위 항을 가진 책 절 page는 자기 H1 아래에 subsection direct link를 두는 source-depth 예외이며 자기 제목의 H2를 반복하지 않는다. 인물 entity는 아래의 공통 인물 형식을 사용한다. 그 밖 entity 첫 화면은 같은 Map 형식과 필요한 날짜별 이력을 함께 보여 주며, 설명과 판단 근거는 명확한 내부 section 또는 도착한 상세 topic·detail에서 읽는다.
- 책은 `책` 페이지에서 `- 장르 텍스트` 아래의 한국 번역판 책 제목 wikilink를 바로 연다. 영문 원제는 alias와 source metadata에 남긴다. 정본 parent tree는 `Wiki → 책 → 장르 키워드 → 책 제목`을 유지한다. 책 root는 승인된 목차에서 실제 학습 본문으로 연결하고 부·장·절의 원문 순서를 보존한다. 검증된 장·절 anchor는 중간 목차를 대체할 수 있으며, 임의의 요약 계층이나 소개용 자식을 만들지 않는다.
- 별도 장·절 page는 위 공통 목차 계약에 따라 실제 본문을 소유할 때 유지한다. 표지·판권 등 비학습 앞부분은 원본 PDF·자산·판본 식별 정보와 source inventory로 보존한다. 의미 있는 개요·서문·학습 설명과 개인 각주는 삭제하지 않는다.
- 책 계층에는 `2주·1달·5달` 중요도 색인을 두지 않는다. 1·2차 book reader unit은 원문의 설명·도판·code만 소유하고 선형 이동은 Map과 관계 metadata가 소유한다. 실제 대화에서 확인된 오개념·실행·결과·인출·전이는 4차 `understanding-enriched`에서만 [책 독자 화면과 개인 각주 계약](repo://skills/skills/knowledge/compile-knowledge/references/book-workflow.md#독자-화면과-개인-각주)에 따라 연결하며 반복 workflow section을 만들지 않는다. 재사용 가능한 일반 개념은 개념 Wiki에 병합하되 책 절을 대체하거나 같은 본문을 복제하지 않는다.
- 책 절의 원문 기반 설명은 대화 보강보다 먼저 존재하는 기준층이다. 이후 학습 대화에서 드러난 오개념·질문·실행 결과는 해당 절의 개인 각주에 출처와 시점을 남겨 연결하되, 기준층의 주장·예제·목차를 삭제하거나 대화 내용으로 바꾸지 않는다. 서로 충돌하면 원문, 현재 공식 문서, 사용자 관찰을 분리하고 어느 하나를 조용히 덮어쓰지 않는다.
- book reader unit과 일반 개념은 별도 identity를 유지한다. 책 밖의 질문·새 근거·현재 버전은 개념 문서를 성장시키고, 책의 특정 판본 설명은 해당 reader unit에 남는다. 둘은 검증된 본문 wikilink와 relation으로 연결하되 같은 설명을 복제하지 않는다.
- 책 tree의 판본·목차·번역·실행 예제 안착을 먼저 완료하고, 개념 tree 연결 확장은 별도 hash 기반 증분 실행으로 처리한다. 개념 연결을 위해 책 장을 다시 생성하거나 전체 개념 corpus를 매 장마다 재검색하지 않으며, 개념 연결 미실행은 source-covered 책 장의 완료를 막지 않는다.
- `콘텐츠` subtree와 Facet은 만들지 않는다. 강의·글·영상에서 얻은 의미는 기존 주제 Wiki에 흡수하고, 외부 원자료와 PDF·이미지·전사는 `Wiki → 리소스 → 분야 텍스트 → 원자료 링크`로만 색인한다. 같은 출처·대상·용도라는 이유로 중간 bundle 문서를 만들지 않는다.
- 책이 아닌 외부 자료의 의미 부모나 `resource_keyword`를 확정할 수 없으면 중간 콘텐츠 카드를 만들지 않고 Review로 보낸다. Novel·민감 자료는 일반 리소스 Graph에 중복 노출하지 않는다.
- 프로젝트 entity는 목표·완료 조건, 요구사항, 설계, 결정, 구현, 검증, 결과, 남은 문제를 subtree와 본문으로 관리한다.
- 인물 hub의 직접 child는 사람 이름의 person entity뿐이다. root 직속 인물 hub(`canonical_id: people/README`)는 `navigation_order: title`을 유지하고 H1 아래에 `- ㄱ` 같은 초성 일반 불릿과 그 아래 들여쓴 사람 wikilink를 표시한다. 빈 초성은 생략하고, NFC 정규화한 이름의 초성순·묶음 안 가나다순을 사용한다. 한글이 아닌 이름은 첫 글자로 묶는다. 초성은 표시 묶음뿐이므로 새 페이지·parent·H2를 만들지 않으며 기존 인물 identity·실제 parent·개인정보 scope를 보존한다. 이 인덱스는 자식 sequence를 요구하지 않고 `navigation_groups`를 함께 선언하지 않는다. native 본문과 AI context의 인물 링크 순서는 같아야 하며 context에도 가짜 초성 문서를 만들지 않는다. [Manta Graph](../obsidian-plugin/references/approved-plugins.md)는 생성된 본문 링크 순서를 읽으므로 metadata만 바꾸고 본문을 남기지 않는다. 다른 hub의 그룹·sequence 규칙은 유지한다. 인물 entity는 아래 카테고리별 흐름에 관계·프로젝트·결정·대화·자료를 통합하며 주제 링크와 별도 이력에 같은 내용을 반복하지 않는다. 날짜만을 위한 별도 히스토리 문서를 만들지 않는다. 사람 이름과 특정 분석 제목을 별도 인물처럼 병렬로 두지 않는다. 이름 한 번의 언급으로 entity를 만들지 않는다.
- 모든 인물의 본문은 `H1 사람 이름 → 짧은 확인된 신상·현재 설명 → 내용이 있는 카테고리`를 따른다. 카테고리의 대표 키워드는 최근 의미 있는 갱신일 내림차순이며, 같은 canonical 키워드를 갱신하면 날짜와 본문 위치를 함께 바꾼다. 그 안의 세부 사건·녹음·문서는 발생 시기의 과거→최근순이다. 이번 작업에서 실제로 의미 있게 갱신한 키워드는 저장 날짜가 같은 날이어도 확인된 갱신 순서에 따라 카테고리 맨 위로 이동하며 본문과 해당 navigation 순서를 함께 맞춘다. 과거 항목끼리 같은 갱신일이고 시각·갱신 선후도 확인할 수 없을 때만 기존 순서를 유지한다. 이를 위해 새 timestamp 속성이나 추정 시각을 만들지 않는다. 발생 시기와 키워드 갱신일을 구분하고 compile·reindex·배포·서식·mtime을 갱신 근거로 삼지 않는다. 모든 인물의 카테고리명·날짜 표기·불명 날짜·대표 항목과 세부 링크 깊이는 [인물 공통 계약](repo://knowledge/docs/person-knowledge-schema.md#인물-페이지의-공통-구조와-정렬)을 따른다. 빈 카테고리·wrapper를 만들지 않으며 인물·캐릭터에 별도 최신 문서 목록을 만들지 않는다.
- 민감한 사건·감정·해석은 기존 비공개 관계 기록에서 읽는다. 같은 시기라는 이유로 독립 사건의 ID·본문을 합치지 않으며 실제 사건의 단일 parent와 창작의 횡단 참조를 보존한다. `history_person_id`, 확인된 `event_people`·`event_period`·`sequence`로 파생한 연표와 Base·DQL은 보조 조회다. 정본 metadata·명시 관계를 공유하고 표·수동 흐름의 요지와 날짜를 원본 사건과 별개로 편집하지 않는다.
- 질문과 답변은 관련 키워드 본문에 둔다. 질문 자체가 계속 갱신되는 독립 정체성일 때만 detail child로 분리한다.

## 파생 화면 경계

- `maps/`에는 `.canvas`와 plugin profile 같은 화면 상태만 둘 수 있다. Markdown Map, 별도 키워드 목록, 독립 시작 노트를 만들지 않는다.
- Global Graph는 `graph/overview` tag가 있는 root·hub·entity만 보여 준다. leaf는 현재 페이지의 subtree, Local Graph, Manta Graph에서 연다.
- `.base`, Canvas, Manta Graph는 Wiki metadata와 실존 wikilink를 읽는다. 화면에만 존재하는 제목·답변·관계·순서를 만들지 않는다.
- 한 문서의 code·실행·상태 관계를 설명하는 canonical 시각화는 `$diagram`의 Markdown Mermaid다.

### Graph 색상 계약

사용자가 지정한 분야색은 일반 entity 색보다 우선한다. 정본 판정과 palette producer는 `repo://core/src/woon_core/knowledge/graph_colors.py`다. 분류표를 복제하거나 해시 파일명 prefix·본문 단어로 분야를 추정하지 않는다.

1. `wiki/README.md`의 승인된 `navigation_groups.children`과 실제 `parent`에서 최상위 의미 분류를 읽는다. 해당 root 아래 `public_taxonomy.roots`가 선언된 경계는 그 이름과 일치하는 직접 child를 분야 입구로 사용한다. 개발 분야의 순서와 정체성도 여기서 파생한다.
2. `entity_kind: book`, `content_kind: book`, `facets: [책]`과 실제 `parent`로 확정한 책 색인·한국어 reader는 비공개여도 기존 책 자주색 `#8B6F82`를 적용한다. 책 entity가 연결한 목차와 확정된 한국어 reader 관계를 따른다. 영어 원문 Markdown·PDF는 정본 담당이 명시 등록한 책별 리소스 archive로 구분하고 기존 리소스 cyan을 적용한다. 같은 폴더의 미연결 파일이나 이름에 책이 언급된 문서를 추정 분류하지 않으며 원문 writer의 작업이 끝나고 정확한 소유권 인계가 되기 전에는 이동·재생성하지 않는다. 그 밖에는 문서 자신의 `access: local-only|private`, `publication_state: private` 또는 private 경로가 **빨강**을 우선한다. 비공개 경계 부모의 접근 상태를 공개 자손에게 상속하지 않는다. 색은 access·publication_state·publish나 공개 범위를 바꾸지 않는다.
3. 공개 리소스는 별도의 cyan, 나머지는 실제 parent를 따라 해당 분야색을 적용한다. 새 개발 parent tree에 편입된 `planned` 키워드는 본문 없음·생각 중이라는 이유로 legacy가 되지 않는다.
4. 현재 `domain: concepts`인 옛 개념 입구 아래의 미편입 개발 문서, 승인된 root 밖의 문서와 해결되지 않은 parent는 회색이다. 새 정본 parent로 이동하면 파생색도 바뀐다. 아직 색인하지 않은 노드는 host의 기본 회색·흰색을 유지한다.
5. Graph query는 현재 parent 분류와 확인된 reader·책별 리소스 등록의 정확한 경로를 파생한다. 빨강 query에서는 승인된 책·책별 리소스 경로만 제외하고 해당 색 query는 private 여부로 제외하지 않는다. 나머지 색 query에는 private 제외 조건을 유지하여 색상 그룹이 중첩되지 않게 한다. 검색 필터·overview 범위·줌·forces는 색과 별개이며 색 변경만으로 수정하지 않는다.

Native Graph 색상 설정은 아래 등록 adapter로 적용한다. Local Graph와 Manta Graph도 분야색을 구현할 때 같은 정본 판정을 따라야 하지만 각각의 설치·화면 반영은 담당 구현과 실제 화면에서 따로 확인한다. 색은 node dot에 적용하고 제목은 host text color를 유지한다. 검색 query는 [Obsidian 공식 Search 문법](https://help.obsidian.md/plugins/search)을 따른다.

책 원문 등록은 `repo://knowledge/config/obsidian-navigation.json`의 `graph.book_source_registry`가 가리키는 기존 책 담당 registry 하나를 읽는다. 참조는 Vault 상대 경로이며 별도의 Graph 파일 목록을 만들지 않는다. 책 record의 `resource_archive`는 `role: book-source-archive`, `source_language: en`, 정확한 archive `root`와 `files[].path`, `kind`, `sha256`를 소유한다. producer는 `private/knowledge/local-only/resources/books` 안의 실존 파일과 hash를 확인하고 등록된 원문 Markdown·PDF·asset만 색에 반영한다. 등록이 미완료이거나 hash·경로·중복·symlink 검사가 실패하면 색 설정과 성공 receipt를 변경하지 않는다. 이 registry 참조를 Obsidian의 `graph.json` 설정 키로 복사하지 않는다.

## Canvas 계약

1. `.canvas`에는 기존 Wiki Markdown을 가리키는 `file` node와 node 사이 edge만 둔다. `text`, `link`, `group` node와 edge label은 지식 정본으로 사용하지 않는다.
2. node `file`은 vault 안의 실존 `.md`다. `subpath`는 실제 heading 또는 block이어야 한다.
3. Canvas edge는 실제 `parent`, `related_to`, 본문 wikilink 중 하나를 투영한다. 좌표·색·edge가 Markdown 관계를 대신하지 않는다.
4. `auto-` ID만 AI가 재생성한다. `manual-` ID와 그 node에 닿는 edge, 접두어 없는 기존 배치는 사용자 소유로 보존한다.
5. 대량 변경 전후에 대상 Markdown, Canvas, 자동 생성 범위, 보존할 수동 범위를 비교한다.

```bash
python3 "$(woon resolve repo://skills/skills/knowledge/knowledge-navigation/scripts/validate_canvas.py)" \
  --vault <vault> \
  --canvas <vault-relative-map.canvas>
```

## 완료 기준

개별 수정은 변경한 node·의존 경로·파생 화면을, 전체 tree 전환은 전체 구조를 확인한다. 아래 기준을 요청 범위에 적용하고 같은 입력·설정의 통과 근거는 재사용한다.

1. root에서 모든 활성 Wiki가 `parent`로 도달하고 cycle·고아 문서가 없다.
2. title·aliases·keywords·중심 질문 기준의 의미상 중복과 병렬 Markdown Map이 없다.
3. root의 직접 child 링크, hub의 직접 링크·작은 분류·명시적 `navigation_groups`의 H2와 direct child 불릿, topic·entity의 child·latest 링크가 실제 metadata와 일치하며 hub에 최신 subtree를 펼치거나 설명·날짜·개수를 반복하지 않는다. 명시적 평탄 인덱스 예외를 제외한 모든 다중 child 페이지는 한 축의 `navigation_groups`를 가진다.
4. `콘텐츠` 분류가 없고 책 화면은 장르 텍스트→한국 번역판 책 링크에서 승인된 실제 본문으로 이어진다. 평탄화한 책은 첫 목차의 장·절 키워드와 본문 링크만으로 탐색하고 퇴역한 wrapper가 파일·링크·이전/다음 이동에 남지 않는다. coverage의 exact-once 본문 소유권·원문 순서·공개 경계를 보존한다. 리소스는 분야 텍스트→원자료 링크이고 프로젝트·인물 entity는 각각 project·topic-timeline 계약을 충족한다.
5. Canvas target과 edge가 실존 Wiki 관계와 일치하고 수동 배치를 보존한다.
6. 화면 반영을 요청한 경우 변경된 root·entity·latest·Global Graph·Local Graph를 실제로 확인한다. UI 확인 전에는 정적 검증 완료로만 보고한다.

## Obsidian 탐색 설정 적용

일반 Graph·검색의 선언된 정책은 `repo://knowledge/config/obsidian-navigation.json`을 읽는다. `woon knowledge configure-navigation --vault <vault>`로 차이를 검토하고 현재 요청이 설정 변경을 포함하면 `--apply`로 반영한다. 기본 모드는 Graph의 search와 Omnisearch의 명시된 필드만 병합한다. 색상만 검토할 때는 `woon knowledge configure-navigation --vault <vault> --graph-colors`를 사용하고, 설정 적용이 배정된 담당은 같은 명령에 `--apply`를 붙인다. 색상 모드의 허용 키는 Graph의 `colorGroups` 하나이며 search·줌·forces·사용자 작업 영역·다른 plugin 설정을 보존한다. 원본 hash가 바뀌면 다시 계획하고, backup → atomic write → disk 재조회 후 local receipt를 기록한다.

실행 중인 Vault에 반영하려면 화면 담당이 같은 adapter의 `--runtime-reload --obsidian-cli <absolute-path> --vault-name <name>` 모드로 먼저 준비 조회한다. 이미 열린 대상 Vault에서 편집이 멈춘 상태로 수행하며, 실제 reload는 준비 결과의 `--expected-state <digest>`와 `--apply`를 명시한 별도 호출이다. 공개 CLI/API로 정확한 Vault·저장된 편집 내용·탭·활성 문서·기존 설정 receipt를 확인하고, 데이터 손실 가능성이 확인되거나 상태가 바뀌면 차단한다. 설정 적용과 reload를 한 호출에 섞지 않는다. machine reload/requery 기록과 실제 Graph 색상 관측을 구분한다. 공개 view state에 색상이 없어도 다른 보존 조건이 충족되면 reload할 수 있지만, 결과는 `pending-visual-verification`이며 담당의 실제 화면 확인 전에는 색상 반영 완료가 아니다. 구체적인 호출과 실패 경계는 `repo://core/README.md`를 따른다.

파일 적용은 실제 화면 검증과 다르다. `ui_verified: false`를 유지하고, 실행 중인 Obsidian이 설정을 다시 저장했다면 반복 덮어쓰지 않는다. 색상 판정은 위 계약과 현재 canonical parent에서 파생하며, 민감 자료 표시를 요청한 사용자의 명시 범위와 일반 탐색 기본값은 담당 작업이 구분한다. 화면을 노출하지 말라는 지시가 있으면 Obsidian을 열거나 재시작해 우회하지 않는다.

Runtime 계약 v3는 공개 `isDeferred`와 view state에서 읽기 모드·파일이 확인되고 디스크 내용이 안정적인 지연 로딩 Markdown만 허용한다. 편집 버퍼를 확인할 수 없는 source 모드와 미저장 내용은 계속 차단하며 탭을 강제 로딩하지 않는다. `navigation-runtime-attempt.json`의 최신 시도 단계와 전후 window epoch를 보고 reload 요청 전 실패·요청 결과 불명·새 창의 postcheck 실패를 구분한다. 실패 시 이전 `navigation-runtime.json` 성공 기록을 이번 실행의 완료로 재사용하지 않는다. 두 기록 모두 실제 Graph 색상 관측을 대신하지 않는다.

reload 이후 재연결 확인만 실패했다면 실패 attempt의 hash를 확인하고 `--runtime-reconnect --expected-attempt <sha256>`로 공개 상태 조회만 이어간다. 이 모드는 reload·layout 저장·설정·receipt 쓰기를 하지 않으며, 명령과 제한은 `repo://core/README.md`를 따른다. reload 전 baseline이 없는 과거 시도는 현재 창 관찰만 반환하며 당시 탭·문서 보존 성공으로 승격하지 않는다. 재연결 중 비완료 eval JSON은 정해진 조회 횟수 안에서만 재시도하고 원래 reload를 반복하지 않는다.
