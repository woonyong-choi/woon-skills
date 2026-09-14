# Diagram Design 연결

공식 upstream은 [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)이다. 외부 skill 본문을 Woon의 독립 사본으로 관리하지 않는다. 설치된 upstream의 `SKILL.md`와 선택한 유형 reference만 필요한 시점에 읽는다.

## 설치와 적용

사용자가 설치를 요청한 환경에서는 현재 CLI 지원과 기존 설치를 확인한 뒤 공식 경로를 사용한다.

```sh
codex plugin marketplace add cathrynlavery/diagram-design
codex plugin add diagram-design@diagram-design
codex plugin list
```

설치 revision과 활성 상태를 재조회한다. 파일을 내려받거나 문서를 읽은 상태를 전역 설치 완료로 보고하지 않는다. 권한 때문에 설치할 수 없으면 승인된 프로젝트 안에서 확인한 upstream을 읽어 산출물을 준비할 수 있지만, 그 실행과 Codex의 자동 발견·설치 상태는 구분한다. 홈 경로·승인 정책을 우회하지 않는다.

## 역할과 산출물

- **Woon:** 공식 지식 조회의 canonical ID·revision·해당 절을 확인하고 질문, 관계, 순서, 사실·추론·미검증 구분을 지킨다. 원자료·기존 Mermaid·compiler 소유 본문과 receipt는 보존한다.
- **Diagram Design:** 의미에 맞는 서로 다른 유형, 공간 구성, 직교 연결선, 강조 1~2곳, 접근 가능한 inline SVG와 독립 HTML을 만든다. 선택한 유형의 reference와 검사를 적용한다.
- **파일:** 데모는 소유 프로젝트의 기존 Git 제외 로컬 산출물 경로 한 곳에 둔다. 출처를 연결하고 재현용 입력·유형·생략 범위를 함께 기록한다. 비공개 자료의 공개·외부 전송은 하지 않는다.
- **Wiki 반영:** 데모 제작은 정본 수정 승인이 아니다. 실제 Wiki 삽입이 요청되면 기존 담당이 `compile-knowledge`와 renderer 경계를 통해 반영한다. 전역 compiler 오류를 우회하기 위해 guard나 receipt를 바꾸지 않는다.

## Woon 표현과 검증

사용자가 제시한 시각 예제의 서체·색상·노드 비율·정보 밀도를 먼저 따른다. 예제가 없을 때 기존 Vault의 appearance·font·accent 설정을 참고한다. 원본 템플릿이 요청한 기준과 일치하면 그 템플릿을 재사용하며, 일관성을 이유로 모든 유형을 큰 상자·동일 배치로 다시 만들지 않는다. 이미 정한 스타일의 온보딩 선택은 다시 묻지 않는다. 설치된 upstream의 공유 style guide를 덮어쓰지 않고 산출물의 재현 입력에 선택한 토큰을 보존한다. 이름·설명은 한국어를 지원하는 sans, 날짜·코드 identifier는 mono로 구분한다. 사용한 폰트와 fallback을 명시하며 private 데모는 외부 폰트 호출 없이 열 수 있게 한다.

색만으로 의미를 구분하지 않는다. light/dark에서 대비·라벨 잘림·선 겹침을 실제로 확인하고, 기술 검사 통과와 예제에 대한 시각적 일치를 별도로 판단한다. 독립 HTML/SVG는 요청한 예제의 화면 비율과 자연 폭을 유지한다. 640px 본문 제약은 실제 Obsidian 삽입용 변형에만 적용하며, 독립 도해 전체를 그 폭에 맞춰 단순화하지 않는다. 좁은 화면의 가로 스크롤은 명시한다. 브라우저 확인을 실제 Obsidian Reading view 검증으로 대신 보고하지 않는다.

upstream self-check와 선택한 유형에 필요한 geometry 검사를 적용한 뒤 실제 렌더링을 확인한다. 같은 source revision·유형·renderer의 통과 근거는 재사용한다. 매 그림마다 전체 Wiki compile·공개 빌드·다른 담당의 같은 검사를 반복하지 않는다.

완료 보고는 설치, Woon 규칙 반영, 실제 데모 생성, 화면 검증을 나누고, 요청한 미리보기와 열 수 있는 파일을 제공한다. 생략한 세부사항과 실행하지 않은 검증은 짧게 밝힌다.
