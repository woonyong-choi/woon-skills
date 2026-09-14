---
name: refactor
description: 외부 동작을 유지하며 구조, 이름, 함수·클래스 경계, 중복 또는 dependency direction을 개선하는 명시적 refactor, code review, 유지보수성 개선 요청에 사용한다.
---

# Refactor

## 시작 gate

먼저 보존할 동작, 요구사항, 현재 diff와 사용 가능한 검증 근거를 확인한다. 검증 선택·통과 근거 재사용·임시물 수명은 `repo://core/standards/code.yaml`을 따른다. 위험한 동작 변경에 필요한 기존 근거가 없을 때만 최소 재현을 만든다.

다음 중 하나면 변경을 시작하지 않고 근거와 필요한 결정을 보고한다.

- 요구 동작이나 외부 계약이 불명확하다.
- baseline test가 실패하고 원인을 현재 변경과 분리할 수 없다.
- 테스트가 없고 public API, persistence, concurrency처럼 동작 위험이 높다.
- 사용자 dirty 변경과 같은 줄 또는 같은 책임을 건드려 안전하게 분리할 수 없다.

## 판단

Code smell은 자동 판결이 아니라 조사 가설이다. 정확한 code 위치, 실제 변경 압력, 책임 경계와 냄새가 아닐 수 있는 반례를 함께 남긴다. 줄 수, parameter 수, 중복 text만으로 수정을 강제하지 않는다.

상세 smell·변환·언어별 확인표는 [review-gates.md](references/review-gates.md)를 필요한 경우에만 읽는다.

## 작은 변환 loop

1. 보존할 동작과 이번 한 단계의 목적을 고정한다.
2. rename, extract, inline, move, encapsulate 또는 dependency inversion을 함께 되돌리고 검증할 수 있는 작은 책임 단위로 수행한다.
3. 좁은 test·typecheck·compile 가운데 가장 가까운 검증을 실행한다.
4. diff에서 기능 추가, bug fix, formatting 대량 변경이 섞이지 않았는지 확인한다.
5. 다음 변환이 필요할 때만 같은 loop를 반복한다. 공유 계약 변경은 관련 통합 검사를 한 번 수행하며 작은 수정 때문에 전체 검사를 반복하지 않는다.

공개 import, API, 예외, 실행 순서, serialization, database schema와 외부 protocol은 관찰 가능한 동작으로 취급한다. 동작 변경이 필요하면 refactor와 기능 변경을 별도 단계로 분리해 사용자에게 알린다.

## 완료 보고

작업 크기에 맞춰 보존 동작·핵심 변경·검증·남은 위험을 간결하게 보고한다. 아래는 필요할 때 사용할 근거 항목이며 매번 고정 양식을 만들지 않는다.

- 보존한 동작과 baseline
- smell의 위치·근거·반례
- 적용한 작은 변환 순서
- 단계별·최종 검증 결과
- 확인하지 못한 계약과 남은 위험

시각적 일관성이나 미래 추측만으로 새 type, layer, `Manager`/`Service`를 만들지 않는다.
