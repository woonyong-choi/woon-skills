---
name: people
description: 확인된 인물 신상·역할과 Vault 자료를 기존 인물 정본에 출처와 함께 정리하고 사람 기준으로 다시 찾을 때 사용한다. 이름만으로 빈 카드를 만들거나 Novel·민감 인물을 일반 지도에 넣지 않는다.
---

# People

`config/person-schema.json`과 [인물과 자료 연결 규칙](repo://knowledge/docs/person-knowledge-schema.md)을 먼저 읽는다. 이 skill은 확인된 인물 정보와 관련 문서·역할을 기존 인물 정본에서 다시 찾을 수 있게 정리하는 절차다. 사용자가 제공했거나 자료에 명시된 생일·신상·역할은 사실의 출처와 확인 시점을 함께 기록하며, 추정한 연락처·신상·관계·민감 특성은 채우지 않는다.

사용자의 “인물이 등장하면 인물 신상정보가 있다면 연결등록하고 인물에 정리해” 지시는 확인된 인물의 명시적 정보 기록과 자료 연결에 대한 사전 승인이다. 이 범위는 매번 다시 승인받지 않는다. 새 자료 수집·전역 대화 자동수집·메일 수집의 재활성화나 외부 전송까지 허용하는 뜻은 아니다.

## 작업 순서

1. `woon_people_find`로 같은 인물 카드를 먼저 찾는다. 이름이 비슷하다는 사실만으로 카드를 합치지 않는다.
2. 문서의 `record_owner`와 원자료의 `author`, `source-provider`, `speaker`, 회의의 `participant`, `organizer`를 분리한다. 별도 지시가 없는 Vault 기록의 소유자는 최우녕이다.
3. 이미 확인된 카드가 있으면 `woon_people_link_document`에 문서 상대 경로, 역할, 문서 안에서 확인한 근거를 함께 보낸다. 호출 뒤 `woon_people_documents`로 같은 문서가 정확히 한 번 연결됐는지 재조회한다.
   신상 사실은 해당 카드의 기존 정본 소유 경로로 반영하고 사실·출처·확인 시점을 구분한다. compiler 소유 정본은 `$compile-knowledge`를 따르며, 역할 연결 MCP에 없는 신상 필드를 임의로 전달하지 않는다. 같은 사실·출처의 재처리는 중복 카드·항목을 만들지 않는다.
4. 사용자가 "이 표기는 이 사람"이라고 직접 확인한 경우에만 `woon_people_set_identity_identifiers`로 `value`, 필요한 `context_terms`, 한 줄 근거를 기록한다. 새 general 한국어 실명 카드는 전체 이름과 성 제외 이름을 기본 식별자로 기록한다. 일반 `aliases`나 이름 유사도는 식별자로 쓰지 않는다.
5. 카드가 없으면 명시 요청 또는 서로 다른 자료에서 확인된 반복 관계가 있는지 확인한다. 위 사전 승인 아래 신상·역할의 명시 근거와 인물 정체성이 확인됐다면 명시 요청으로 처리한다. 단순 이름만 있거나 동명이인·정체성이 불분명하면 `attributions` 또는 확인 필요로 남기고 빈 카드를 만들거나 임의로 합치지 않는다.
6. 카드 생성이 정당하면 `woon_people_upsert_card`에 `explicit-request` 또는 `repeated-evidence`를 명시한다. 목적은 "왜 이 사람 기준으로 문서를 다시 찾아야 하는가"로 한 문장만 쓴다.

기존 비공개 native Wiki의 본문·metadata는 `KnowledgeService.apply_native_wiki_transaction`에 검토한 `ManualWikiWrite`를 전달해 변경한다. 각 항목은 동일한 기존 경로, 읽은 bytes의 SHA-256, 반영할 전체 bytes와 SHA-256을 고정한다. adapter는 canonical ID와 `access: local-only`·`publish: false`를 보존하고 compiler 소유를 제외하며, 대상 tree·index 재조회와 backup·receipt·실패 rollback을 수행한다. 공개 page의 dummy upsert나 전체 compiler 실행을 끼우지 않는다. 새 카드는 위 PersonService 생성 계약으로 먼저 만들고, 기존 카드에 추가된 신상·출처·본문은 upsert 재실행으로 덮어쓰지 않는다. 실제 반영은 현재 Wiki 단일 writer가 담당한다.

## 문서별 선택

- 일반 source·회의·일일 기록·brain 후보: 이 skill의 local MCP로 역할 연결이 가능하다.
- compiler가 소유한 `wiki/`: 생성 Markdown을 직접 고치지 않는다. `$compile-knowledge`로 source·claim·page spec을 갱신하고 compiler receipt까지 확인한다.
- 이름은 있으나 카드 생성 근거가 없는 자료: `attributions`만 사용한다.
- Novel 원문, `private/**`, 실제 인물의 창작·민감 자료: 일반 인물 지도·검색으로 옮기지 않는다. 명시된 신상 사실도 해당 인물의 기존 비공개 정본에 기록하고 원문은 기존 보관 위치에 보존한다. 확인된 작품·인물 관계만 기존 `wiki/private/**` 정본 아래에 연결한다. 기존 삭제 금지 지시는 요약·중복 정리·퇴역에도 우선한다.
- 자동 수집 메일·대화 후보: 사람 이름이나 관계를 추정해 카드·링크를 만들지 않는다. 후보 검토 뒤 명시된 사실만 이 skill으로 연결할 수 있다.
- Calendar 제목: Core가 `identifiers`의 정확한 표기만 local-only 일정 노트에 연결한다. `Woon 일정`에서 직접 만든 일정은 최우녕을 `organizer`로 연결한다. 같은 식별자가 여러 카드에 있으면 `inbox/review/calendar-person-identity-review.md`에 후보만 남기고 자동 연결하지 않으며, 사용자가 지정한 뒤에만 맥락 단어를 포함한 식별자를 갱신한다.
- Novel private history: 원문을 읽어 이름을 추정하지 않는다. `private/novel/work/work-catalog.yaml`과 `private/novel/work/people/person-link-ledger.yaml`은 source 입력 장부이며, 검증된 작품→인물·인물→작품 관계의 정본은 기존 `wiki/private/**` 작품·사람 subtree에 한 번만 기록한다. `inbox/private-person-history/**`나 source dashboard를 만들지 않는다. 원문 전체는 복사하지 않고 source locator·hash·확인 근거만 둔다. `review_candidates`가 있을 때만 Review를 만들고 승인 전에는 관계를 승격하지 않는다.

## 완료 기준

- 모든 인물은 [공통 구조와 정렬](repo://knowledge/docs/person-knowledge-schema.md#인물-페이지의-공통-구조와-정렬)에 따라 `H1 사람 이름 → 짧은 확인된 신상·현재 설명 → 내용이 있는 카테고리`로 읽는다. 같은 종류에는 같은 카테고리명·날짜 표기·링크 깊이를 사용하고 빈 카테고리·카드·wrapper·날짜 문서를 만들지 않는다.
- 카테고리의 대표 키워드는 최근 의미 있는 갱신순, 그 안의 사건·녹음·문서는 실제 발생 시기의 과거→최근순으로 둔다. 같은 canonical 키워드의 내용 추가·사실 수정·근거 보강은 기존 항목에 흡수하고 갱신일과 본문 위치를 함께 갱신한다. 기존 `updated`는 의미 변경 근거가 확인될 때만 사용하며 compile·reindex·배포·서식·mtime으로 순서를 올리지 않는다. 이번 작업에서 실제로 의미 있게 갱신한 키워드는 저장 날짜가 같은 날이어도 확인된 갱신 순서에 따라 카테고리 맨 위로 이동한다. 과거 항목끼리 같은 갱신일이고 시각·갱신 선후도 확인할 수 없을 때만 기존 본문·navigation 순서를 유지한다. 새 timestamp 속성이나 추정 시각은 만들지 않는다. 갱신일 미확인과 발생일 미상은 구분해 각 목록 마지막에 둔다.
- 대표 항목 하나 아래 세부 기록을 연결하고 같은 내용을 주제 목록과 별도 이력에 반복하지 않는다. 같은 시기라는 이유로 독립 사건 본문을 합치지 않는다. Base·DQL·생성 연표는 같은 정본 metadata와 명시 관계를 읽는 보조 조회이며 수동 목록·자동 표를 독립 원본으로 관리하지 않는다.
- 기본 `woon_people_documents`와 인물 Base는 명시적 `people` 연결만 조회한다. `record_owner`는 참여 관계가 아니며 소유 문서 조회는 Core의 `include_owned=True`를 명시할 때만 사용한다.
- 실제 관찰·사건·화자의 감정·당시와 현재의 해석은 `wiki/private/people/<person-id>/` 아래에서 읽고, 창작 코어·행동·관계·각색은 기존 작품 subtree가 소유한다. 민감 기록은 일반 인물 Base·검색·Global Graph에 펼치지 않는다.
- 사건의 기존 ID와 경로를 보존하고 `event_people`에는 확인된 기록 관련 인물 ID만 둔다. 이 값은 참석자 목록이 아니다. `event_period`는 발생 시기와 불확실성, `sequence`는 확인된 사건 순서다. 관계 페이지의 `history_person_id`를 읽어 Core가 `woon-person-history` 연표를 생성한다. 수정일을 사건 날짜로 사용하지 않는다.
- 인물 기록으로 지정한 대화는 기존 사건·근거·감정·해석을 구분해 병합한다. 일기 원문은 일기에 보존하고, 창작 후보 연결은 사용자가 해당 부분을 선택한 경우에만 수행한다. 이전 해석·기각 이유·variant를 삭제하거나 새 요약 문서로 복제하지 않는다.

- 사람 카드에는 근거가 확인된 신상·역할과 필요한 자료 연결만 있으며, 추정한 신상·관계 설명은 없다. 기존 사실과 새 근거가 충돌하면 조용히 덮어쓰지 않고 근거와 확인 필요 상태를 함께 남긴다.
- 연결 문서에는 `people`과 `person_roles`가 함께 있으며 role과 evidence가 빠지지 않는다.
- 사람 기준 재조회 결과에는 의도적으로 연결한 문서만 나온다.
- 기본 `people-index`와 전역 Graph에 Novel·민감 인물 카드가 나타나지 않는다.
- `novel-local-only` 카드의 직접 확인된 식별자는 local-only Calendar 노트에만 쓸 수 있고, 이 예외가 일반 지도·검색으로 번지지 않는다.
- private history 검증은 작품 catalog와 explicit relation ledger를 반복 실행해도 새 dashboard·링크·이력을 만들지 않으며, Novel 원문이나 전역 Graph를 바꾸지 않는다. 사람용 관계 갱신은 Wiki projection 한 경로만 소유한다.
- Calendar는 Novel 작품·관계·원문을 event나 task로 가져오지 않고, 사용자 확인 식별자의 local-only 사람 연결만 허용한다.

## 비공개 기록 연결과 재생성

- 실제 내용·독립된 사건이나 경험·현재 쓰는 목차가 있을 때만 새 문서를 만든다. 기록 표를 채우기 위한 빈 wrapper, 원문 사본, 별도 운영 보고서는 만들지 않는다. 승인된 개발 키워드 목차를 이 규칙으로 일괄 삭제하지 않는다.
- 선택한 기록의 속성과 API는 [인물과 자료 연결 규칙](repo://knowledge/docs/person-knowledge-schema.md#비공개-관련-기록-조회)을 따른다. `record_kind`를 사람·프로젝트·개념에 일괄 부여하지 않는다. 기존 날짜·ID·`event_people`·`history_person_id` 소유권을 보존한다.
- source renderer는 Core `people.records.resolve_record_metadata(existing, proposed, confirmed_relations=...)`로 기존 frontmatter를 병합하고 선택 batch의 `validate_record_collection`을 쓰기 전에 통과시킨다. native 갱신은 같은 resolver로 만든 전체 bytes를 기존 transaction에 전달한다. 기록 metadata를 표현하지 못하는 일반 archive로 재생성하지 않는다.
- 사용자 연결 `related-record`와 화자·참석자 확인을 구분한다. 후보 person ID는 plain text 목록에 남기며, 같은 사람의 related-record 연결이 화자 후보를 자동 확정하지 않는다. 실제 화자 대응과 상세 근거는 기존 장부를 재사용한다.
- 비공개 host의 보조 조회는 Core의 `inbox/private-linked-records.base`를 사용한다. native Bases가 제외하는 녹음 reader는 위 연결 규칙의 등록 DQL producer로 승인 host 안에 읽기 전용 표를 생성한다. 일반 검색·Graph·인물 Base의 private 제외를 풀거나 DataviewJS를 활성화하지 않는다. 관계·날짜·상태는 Core에서 생성하고 후보·날짜 미상은 별도 조회로 유지한다. 원문·관계를 표에서 이중 관리하지 않으며 파일 검증·실제 화면·본문 교정 완료를 구분한다.

이 skill은 `repo://skills/skills/knowledge/people`의 단일 원본이며, Vault에는 사용 문서만 둔다.
