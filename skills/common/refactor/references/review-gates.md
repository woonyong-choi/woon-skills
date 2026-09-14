# Refactor review gates

이 reference는 Martin Fowler의 《Refactoring: Improving the Design of Existing Code, Second Edition》에서 다루는 행동 보존, code smell, 작은 변환, 테스트 재검증 원칙을 작업용 계약으로 재구성한 독자적 요약이다. 원문 문장이나 예제의 복제본이 아니다.

공식 도서 안내: https://martinfowler.com/books/refactoring.html

## Smell에서 조사로

| 신호 | 확인할 근거 | 주로 검토할 변환 | 반례 |
| --- | --- | --- | --- |
| Mysterious Name | 역할·단위·범위가 이름에서 읽히는가 | Rename | 짧고 문맥이 명백한 local |
| Duplicated Code | 같은 지식이 같은 이유로 함께 변하는가 | Extract, Move | text만 같고 domain 규칙이 다름 |
| Long Function | 책임과 추상화 수준이 여러 번 바뀌는가 | Extract Function, Split Phase | 분리하면 data 흐름이 더 어려워지는 선형 algorithm |
| Long Parameter List | 함께 이동하는 값, query 가능한 값, flag가 있는가 | Parameter Object, API refactor | dependency를 명시하는 경계 함수 |
| Mutable 또는 Global Data | 쓰기 주체, 순서, lifecycle을 추적할 수 있는가 | Encapsulate, immutable value | 격리된 성능 buffer |
| Divergent Change | 한 module이 독립된 여러 이유로 바뀌는가 | Extract Class, Split Phase | 작고 안정적인 module |
| Shotgun Surgery | 한 변경이 여러 위치의 같은 수정으로 퍼지는가 | Move, Combine | 독립 adapter가 protocol상 함께 갱신됨 |
| Feature Envy | behavior가 다른 객체의 data에 더 의존하는가 | Move Function | 여러 객체 조정이 본래 책임인 orchestrator |
| Repeated Switches | 같은 type 분기가 여러 위치에 반복되는가 | Polymorphism, Strategy | 한 번뿐인 단순 분기 |
| Message Chains | caller가 내부 object graph를 과도하게 아는가 | Hide Delegate | 의도된 fluent API |

## 변환 전 확인

- 현재 branch와 dirty diff에서 사용자 소유 변경을 식별한다.
- 반환값, 예외, side effect, 저장 상태, 정렬, 시간·순서, 외부 호출을 포함해 보존 동작을 적는다.
- public API, import, reflection, annotation, JSON key, database schema, protocol consumer를 검색한다.
- baseline 명령과 결과를 기록한다. flaky 또는 기존 실패는 성공으로 취급하지 않는다.

## 언어별 확인

- Python: dynamic import, monkey patch, string lookup, mutable default, module global, raw dict와 얕은 copy를 확인한다.
- Java: binary/source compatibility, overload resolution, reflection, annotation processor, record/value semantics와 defensive copy를 확인한다.
- Kotlin: Java interop, nullability, default/named argument, extension import, sealed hierarchy, `data class.copy`의 얕은 copy와 read-only collection을 확인한다.

## 완료 판정

완료는 새 code가 더 좋아 보인다는 주장으로 정하지 않는다. 보존 계약이 테스트되고, 각 변환이 review 가능한 크기이며, 최종 diff에 별도 기능 변경이 섞이지 않고, 변경된 계약에 필요한 검증이 통과해야 한다. 검증하지 못한 항목은 `unverified`로 남긴다.
