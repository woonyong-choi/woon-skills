# 다이어그램 검사표

- Mermaid fence 바로 앞에 그림이 답할 질문을 실제 identifier가 포함된 질문형 문장으로 한 개만 명시한다.
- 관계에 맞는 Mermaid 유형을 사용하고 inheritance·runtime call·DB relation을 한 그림에 섞지 않는다.
- overview는 9 nodes 이하, node 하나는 한 동작이나 상태, label은 세 줄 이하로 둔다.
- source의 class·method·variable·value identifier를 그대로 사용한다.
- 순서가 의미라면 arrow label에 `1.`부터 번호를 붙이고 뒤의 설명도 같은 번호를 사용한다.
- 정상·오류, 값 복사·reference 공유는 text label과 line style로 구분한다.
- hard-coded fill·text color와 red/green만의 의미를 사용하지 않는다.
- 선행 조건은 의존 단계보다 먼저 나타나며 crossing line과 잘린 text가 없다.
- Markdown 안의 Mermaid source를 정본으로 유지하고 생성된 SVG·PNG를 정본으로 삼지 않는다.
- default·dark theme로 실제 render해 syntax, contrast, clipping과 label 가독성을 확인한다.
- Obsidian split pane처럼 폭이 좁은 대상은 목표 pane 폭을 정하고 SVG natural `viewBox` width와 실제 Reading view를 함께 확인한다. 학습 문서 fixture의 기준은 640 CSS px다.
- 흐름 방향과 좁은 pane의 sequence 배치는 [Diagram 정본](../SKILL.md)을 따른다. 단순 흐름의 가로 배치를 우선하되 폭에 맞는 묶음·세로 배치를 허용하며, acceptance 상한 640px와 생성 목표 620px를 혼동하지 않는다.
- repository가 고정한 Mermaid tool과 version을 우선한다. 없으면 bundled `scripts/verify-mermaid.sh`를 사용하고 unversioned package나 mutable latest를 호출하지 않는다.
- bundled verifier의 exit `2`는 renderer unavailable이다. 같은 조건의 재시도를 멈추고 미검증 범위를 보고한다. renderer 설치·수정은 현재 요청에 포함된 경우에만 진행한다.
- 두 theme의 command exit와 생성물 크기를 verifier 한 번으로 확인한다. 한 theme가 중단됐는데 다른 theme까지 검증됐다고 보고하지 않는다.
