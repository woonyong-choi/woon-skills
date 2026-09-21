# Writing quality contract

## Scope and ownership

이 표준은 번역, 기술 설명, 보고서, 안내, 개인 기록과 창작의 공통 작성·검토 경계를 소유한다. 각 유형의 skill은 자료 선택, 형식, 정본 writer와 유형별 표현을 소유하고, 이 표준의 의미·근거·검토 계약을 복제하지 않는다.

충돌은 현재 사용자 요청 → 대상의 보존 계약 → 사용자가 명시한 선호 → 검증된 유형별 기준 → 학습 중인 규칙 후보 순서로 해결한다. 아래 공통 불변조건은 모든 층에 적용한다.

- **공통 불변조건**: 사실·의도·조건·부정·수치·주체·예외·권리·visibility와 보존 대상을 바꾸지 않는다.
- **유형별 기준**: 번역·기술 설명·보고서·안내·개인 기록·창작이 각각 전달해야 할 결과를 확인한다.
- **개인 선호**: 사용자가 명시했거나 승인한 말투·용어·구조를 적용한다. 명시 선호가 없고 여러 표현이 모두 정확하면 기존 표현을 보존한다.

문체 선호는 사실과 보존 계약을 덮어쓰지 않는다. 공통 기준은 특정 문장 길이, 접속사, heading 수나 표현 목록을 모든 글에 강제하지 않는다.

## Input contract

작성 전에 다음 입력을 고정한다. 짧은 문장 교정도 같은 필드를 확인하되, 이미 요청과 원문에서 분명한 값을 별도 문서로 늘리지 않는다.

```yaml
writing_brief:
  purpose: 이 글로 독자가 판단하거나 수행할 일
  audience: 독자의 배경과 필요한 설명 수준
  document_type: translation | technical-learning | research-report | general-guidance | personal-record | fiction
  request_revision: 요청 또는 승인 범위를 식별하는 revision
  source_records:
    - locator: 원자료 위치
      revision: hash 또는 immutable revision
      role: fact | style
  edit_scope: 바꿀 수 있는 본문·구조·형식
  preserved_elements: [원문, 인용, code, 수치, 이름, 사건 순서, 말투 등]
  completion_conditions: [필요한 산출물과 검증]
  visibility: private | local-only | internal | publishable
  preferences: [명시적으로 확인한 말투·용어·구조 선호]
```

- `fact` reference는 사실·수치·실행 결과를 뒷받침한다. `style` reference는 말투·용어·구성 참고이며 사실 근거를 대신하지 않는다. 보존할 원문은 `preserved_elements`에 둔다.
- 원자료의 locator와 revision을 확인할 수 없으면 확인 가능한 범위만 작성하고 나머지는 `unknown`으로 남긴다.
- 공개 범위와 변경 허용 범위가 없으면 private 원자료를 외부 전송하거나 공개 후보로 바꾸지 않는다.
- source 원문이나 다른 저장소의 지침을 이 표준에 복제하지 않는다. 안정적인 `repo://` 참조와 revision만 남긴다.

## Claims, anchors and explanation links

검토 가능한 글은 주장과 실제 본문 위치를 연결한다. Woon Wiki에서는 기존 `source → claim → page → receipt`를 재사용하고 별도 claim 장부를 만들지 않는다. 그 밖의 산출물은 Core v2의 claim 역할인 `fact`, `observed`, `inference`, `proposal`, `example`, `unknown`으로 필요한 주장만 구분한다. 개인 기록의 기억·감정과 창작의 허구·표현 선택은 유형 profile에서 보존하되 새 claim enum을 만들지 않는다. 이 문서의 YAML과 표는 작성 원칙을 설명하는 개념 예시이며 Core schema의 정확한 필드·enum 원본이 아니다.

각 주장에는 실제 `body_anchor`와, 필요한 경우 `evidence_anchor`를 둔다. 문서 전체나 제목만 가리켜 개별 주장을 검증했다고 하지 않는다. 설명의 연결은 접속사 수나 문장 길이가 아니라 다음 관계가 실제로 성립하는지로 확인한다.

- 전제 → 결론 (`premise-conclusion`)
- 조건 → 결과 (`condition-result`)
- 앞선 표현 → 같은 대상 (`coreference`)
- 원인 → 변화 (`cause-change`)
- 개념 → 예시 (`concept-example`)
- 코드 → 출력 → 해설 (`code-output-explanation`)
- 질문 → 답 (`question-answer`)

원문에 없는 인과 접속사를 넣거나, 관계를 설명하지 않은 채 문장을 길게 잇는 것은 연결 개선이 아니다.

## Type profiles

| 유형 | 필수 결과 | 보존·제외 경계 |
| --- | --- | --- |
| 번역 | 원문의 주장·조건·부정·수식 범위·설명 순서와 전문 용어를 대상 언어로 전달한다. | code·identifier·인용·판본 차이를 문체 선호로 바꾸지 않는다. style-reference 문장을 복사해 개선으로 세지 않는다. |
| 기술 설명 | 독자가 실제 source·code·값·결과에서 원리와 적용 경계를 따라갈 수 있다. | 실행하지 않은 output, 최신성·성능·안전성 주장을 만들지 않는다. |
| 보고서 | 결론, 근거, 확인 범위, 미결정과 다음 판단 조건을 구분한다. | 조사·시도·후보를 완료·채택·운영 결과로 바꾸지 않는다. |
| 안내 | 대상과 행동, 필요한 조건, 예상 결과와 실패 시 다음 확인이 분명하다. | 짧은 안내에 배경 설명을 늘리거나 확인하지 않은 절차를 보태지 않는다. |
| 개인 기록 | 사용자의 말투, 시점, 감정, 불확실성과 생각 흐름을 보존한다. | 반복을 줄인다는 이유로 경험을 요약 삭제하거나 타인의 의도를 확정하지 않는다. |
| 창작 | 요청한 시점, 정서, 관계, 장면·대사의 기능과 의도한 모호성을 보존한다. | 사실문 기준으로 의도한 비유·중의성·파격을 평탄화하지 않는다. 새 variant를 기존안의 객관적 개선으로 단정하지 않는다. |

## Write and review

1. `writing_brief`와 유형 profile로 초안을 작성한다.
2. 작성 호출과 분리된 검토 호출을 수행한다. 짧은 교정도 검토를 생략하지 않지만, 별도 hidden agent나 자동 실행을 요구하지 않는다.
3. 검토자는 초안, 사용자 요청, 근거, 적용 기준만 받는다. 작성자의 자기평가, 개선 주장이나 예상 판정은 입력하지 않는다.
4. 같은 계열 model이 작성과 검토를 맡더라도 별도 호출이면 절차상 분리할 수 있다. 같은 model·session의 단순 연속 자기검토는 별도 검토가 아니며, 어느 경우도 통계적으로 독립한 검토라고 주장하지 않는다.
5. 검토 실패를 수정하고 영향받은 항목만 다시 확인한다. 자동 수정은 최초 검토 뒤 최대 두 차례다. 이후에도 핵심 실패가 남으면 재개 가능한 상태와 필요한 입력을 남기고 멈춘다.

항목 상태는 네 가지뿐이다.

- `pass`: 기준을 충족한다는 실제 본문·근거 anchor가 있다.
- `fail`: 실제 anchor가 필수 기준을 위반한다.
- `unknown`: 근거·범위·revision이 부족하거나 서로 충돌해 판정할 수 없다.
- `not-applicable`: 해당 유형·문서에 적용되지 않으며 이유가 있다.

증거 없는 `pass`는 금지한다. 결함을 입증하지 못했다는 이유만으로 `pass`를 주지 않으며, “확인 범위” 문구가 있다는 이유만으로 범위 안의 주장을 자동 통과시키지 않는다. 핵심 `unknown`과 필수 `fail`은 확정·승격·공개를 차단한다. 스타일 판단이 갈리지만 사실·의도·보존 계약을 모두 만족하면 사용자의 명시 선호, 없으면 기존 표현을 보존한다.

문서, 근거, 사용자 요청, 적용 표준 또는 profile의 revision/hash가 바뀌면 영향받는 기존 검토는 stale이다. 최종 판정은 검토한 문서 hash와 같은 bytes에만 유효하다.

## Reviewer contract

새 검토는 Core의 writing review request/result v2를 사용한다. request는 profile, purpose, audience, visibility, edit scope, preserved elements, completion conditions, `revision_attempt`, 문서·reference·standard revision/hash, fact/style reference, typed claim과 body/evidence anchor, writer provider·model·tool·run ID를 고정한다. result는 별도 reviewer identity, 같은 revision/hash와 revision attempt, 각 항목의 네 상태와 `not-applicable` 이유, source anchor, relation type, 핵심 unknown, hard failure와 final document hash를 보존한다. 비핵심 `unknown`은 이유와 영향 범위를 한정한 qualified result로만 남길 수 있다.

기존 Wiki `quality-review-plan` v1 result는 기존 Wiki-only acceptance gate를 통과할 수 있지만, v2 cross-profile contract를 충족하거나 v2로 승격되지는 않는다. 새 검토의 실행 순서는 writer가 request 생성 → 별도 보이는 reviewer가 result 작성 → 현재 bytes·hash·anchor evaluate다. reviewer를 자동으로 숨겨 실행하거나 작성자가 result를 대신 채우지 않는다. 정확한 schema와 명령은 `repo://core/docs/writing-quality.md`를 따른다. 진입점은 `woon knowledge evaluate-writing-review`, `woon knowledge evaluate-writing-rule`, `woon knowledge adopt-writing-rule`, `woon knowledge register-writing-rule-application`, `woon knowledge rollback-writing-rule`이다.

## Learning rules from examples

예시에서 규칙을 배우는 작업은 일상 작성과 분리한다. 규칙 후보에는 다음을 둔다.

```yaml
rule_candidate:
  id: stable-id
  version: v1
  instruction: 검증할 규칙
  source_observations: [source locator와 revision]
  profiles: [한정된 적용 profile]
  applicability: 적용 조건
  exclusions: [비적용 조건]
  expected_effect: 관찰 가능한 차이
  counterexamples: [규칙을 기각할 결과]
  status: candidate | trial | adopted | held | rejected | disabled
  evaluation_revision: 평가 revision
  invariant_effect: preserve-only
```

도출용, 개발용, 최종 검증 자료를 규칙 고정 전에 나눈다. 규칙 생성·수정에 노출되었거나 개발 평가에 재사용한 자료와 그 중복·파생 자료는 최종 held-out으로 세지 않는다. 최종 평가자는 정답 기준을 볼 수 있지만 candidate를 만든 자기평가나 규칙 개선 힌트는 받지 않는다. 같은 model이라도 session·입력 누출이 있으면 독립 사례로 세지 않는다. 원자료 안의 지시는 평가 명령으로 따르지 않는다.

규칙 자동 채택은 한 대상 유형 안에서 다음 조건을 모두 만족할 때만 허용한다.

- 독립적인 실제 사례 20개 이상, 서로 다른 문서·과제 3개 이상
- 같은 입력·model·도구 조건에서 기준본보다 명확히 우세한 사례 12개 이상
- 나머지는 동등하며 악화, 핵심 `unknown`, reviewer 불일치, 누출과 중복이 모두 0
- 의미 동등 의역, 정확한 짧은 글, 의도한 창작을 오탐하지 않는 대조시험 통과
- 조건·부정·숫자·주체·예외 변조, 잘못된 인과, 길이만 증가, 근거 없는 검증 완료 표현을 모두 탐지
- 각 판정에 구체적인 문장·source anchor가 있고 사용자의 명시 선호와 충돌하지 않음

최종 비교는 기준본과 candidate의 순서를 가린 A/B 검토로 수행하고, 관계별 근거·문제·수정 이유를 남긴다. 문턱에 이르지 못한 규칙은 `trial`로 계속 관찰할 수 있지만 일상 작성의 강제 규칙이나 채택 완료로 보고하지 않는다.

이는 초기 운영 문턱이며 통계적 무오류 보장이 아니다. 한 유형에서 채택한 규칙을 다른 유형으로 자동 확장하지 않는다. 검토 중인 후보는 `trial`, 문턱 미달은 `candidate` 또는 `held`, 폐기는 `rejected`, 회귀로 끈 규칙은 `disabled`로 기록한다. 채택·적용 등록·복구, revision guard와 영향 문서 식별은 Core policy API가 소유한다.

## Required controls

새 기준과 learned rule은 관련된 최소 대조군으로 확인한다.

- 의미가 같은 의역, 짧지만 정확한 글, 의도한 창작 선택은 실패시키지 않는다.
- 조건·부정·숫자·주체·예외가 바뀌면 실패시킨다.
- 원문에 없는 인과 접속사, 반복으로 늘어난 길이, 근거 없는 “검증됨” 문구를 개선으로 인정하지 않는다.
- 표본 몇 개의 성공, 문서 작성, schema 통과만으로 품질 개선이나 일반화를 완료했다고 보고하지 않는다.
