---
name: site-promotion
description: private Woon 정본을 블로그·포트폴리오 공개 후보로 변환하거나 portfolio 노출 항목을 직접 선택하며 claim·개인정보·승인을 관리할 때 사용한다.
---

# Site Promotion

`woon-knowledge`의 깊은 정본을 공개 투영 폴더에 직접 복사하지 않고, 검증된 claim ledger에서 목적별 public candidate를 만든다. 일반 기술 글, 이력서 문구, private 저장, UI 구현에는 각각 `$tech`, `$career`, `$archive`, `$react`를 쓴다.

1. `$knowledge`로 source를 검색·조회하고 `canonical_id`·revision·source type·현재 재검증 여부를 고정한다.
2. claim마다 사실, 수치 조건, 개인·팀·사후 확장 소유권, 공개 권리와 근거를 분리한다. 입력에 없는 ownership·rights는 각각 `unresolved`·`unknown`이며 요청 문장이나 인접 claim에서 가져오지 않는다. rights 때문에 본문을 보류해도 private 값만 제외한 claim ledger와 metric context는 생략하지 않는다.
3. destination이 blog이면 [블로그 계약](references/blog-contract.md), portfolio이면 [포트폴리오 계약](references/portfolio-contract.md)을 읽는다. 둘 다 요청되면 하나의 ledger에서 별도로 쓰고 문장을 재사용하지 않는다.
4. 요청한 destination의 candidate와 [승격 계약](references/promotion-contract.md)의 영수증을 검토 가능한 형태로 완성한다. private 값은 제외 유형과 건수만 적고 원문을 다시 쓰지 않는다. 로컬 후보·검증 파일 작성은 요청 범위에서 진행하되 정본 반영·공개 상태와 구분한다.
5. 현재 요청과 대화에서 해당 candidate·destination·포함 범위의 반영 권한이 확인되면 Vault의 해당 source·claim·page spec을 갱신하고 승인된 공개 projection을 생성한다. 권한이 부족할 때만 완성한 후보를 제시해 필요한 반영 승인을 요청한다. commit·push·deploy는 각각 현재 요청에 포함된 범위에서만 수행한다.
6. 변경한 콘텐츠와 대상 저장소 계약에 필요한 schema·claims·images·build·rendered route를 검증하고 확인한 계층과 미검증 계층을 분리한다. 같은 입력의 통과 근거는 재사용한다.

승인 표현의 단어만으로 권한을 인정하거나 배제하지 않는다. 바로 앞의 검토 가능한 후보와 명확한 destination·포함 범위를 승인한 응답은 그 범위에 재사용한다. 포괄적인 작성 요청은 공개 권리나 대상 선택 권한이 아니며, unsupported claim 보강과 승인 범위 밖 변경을 금지한다.
