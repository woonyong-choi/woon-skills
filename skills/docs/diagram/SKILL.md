---
name: diagram
description: Mermaid·Obsidian Canvas와 diagram-design HTML/SVG로 구조·순서·상태·관계·Wiki 기록을 시각화하고 출처·정본·light/dark 경계를 검증할 때 사용한다.
---

# Diagram

사용자가 `diagram-design`, 편집용 HTML/SVG 또는 Wiki 기록의 시각화 데모를 요청하면 [Diagram Design 연결](references/diagram-design.md)을 함께 적용한다. Woon은 출처·관계·정본·공개 범위를, upstream `diagram-design`은 유형별 시각 구성과 HTML/SVG 출력을 소유한다. 아래 Mermaid 규칙은 Mermaid 산출물에 적용하며 HTML/SVG를 만들기 위해 기존 Wiki Mermaid를 삭제하거나 compiler 본문을 직접 바꾸지 않는다.

그림이 답할 질문을 한 문장으로 먼저 정하고 유형 하나를 고른다: 흐름 `flowchart`, 호출 순서 `sequenceDiagram`, 상태 `stateDiagram-v2`, 타입 `classDiagram`, cardinality `erDiagram`. 산출물에서는 Mermaid fence 직전의 비어 있지 않은 문장을 실제 identifier가 포함되고 `?` 또는 `하는가.`로 끝나는 질문으로 쓰며, fence 뒤에는 같은 번호를 사용하는 관찰 2~5개를 둔다.

overview는 9 nodes 이내, node는 한 동작·상태, sibling label은 같은 문법으로 유지한다. source identifier를 정확히 쓰고 inheritance, runtime call, DB relation을 한 그림에 섞지 않는다. 색을 hard-code하지 말고 위치·선·label로 의미를 전달한다.

AI가 작성·재구성하는 Wiki의 단순 흐름이 세로로 길어지면 `flowchart LR`을 우선한다. node label은 짧게 쓰고 설명은 인접 본문에 두어 본문 폭 안에서 읽게 한다. 폭과 높이가 모두 큰 그림은 단계별로 묶거나 세로 흐름을 허용한다. 모든 그림에 LR을 강제하거나 맞추기 위해 글자를 작게 축소하지 않는다. 책 원본 image payload는 이 선호 때문에 바꾸지 않는다.

Obsidian의 640px split pane에 3개 participant를 놓는 `sequenceDiagram`은 자연 폭을 620px 이하로 설계해 20px 여유를 남긴다. 첫 줄에 `%%{init: {"sequence": {"actorMargin": 24, "width": 112}}}%%`를 사용하고 participant에는 class·variable identifier만 쓴다. type·signature는 prose로 옮기며 arrow label은 번호를 포함해 한글 16자 이내로 줄인다. 4개 이상이면 한 그림을 억지로 축소하지 말고 질문별로 나눈다. 가로 flowchart가 목표 폭을 넘으면 짧은 label·단계 묶음을 먼저 검토하고, 여전히 읽기 어려우면 세로 배치를 사용한다. 최종 acceptance는 640px 이하이며 620px는 생성 안전 목표다.

독립 diagram 작성·검토는 [diagram checklist](references/diagram-checklist.md)에서 대상 source·renderer·표시 환경에 필요한 기준을 적용한다. 같은 diagram과 renderer 환경에서 이미 통과한 source 대조·light/dark render·clipping 근거는 재사용한다. 학습 문서에서는 아래 learning-content 표준이 같은 gate를 소유하므로 checklist를 중복해서 읽지 않는다. 다른 저장소는 이 스킬을 복사하지 말고 `repo://skills/skills/docs/diagram`을 참조한다.

repository에 고정된 Mermaid CLI를 우선하고 없으면 이 skill의 `scripts/verify-mermaid.sh <source.mmd> <output-dir>`를 사용한다. 이미 확인한 경로와 사용 가능한 renderer를 재사용한다. verifier는 설치된 `mmdc` 또는 npm cache의 고정 version으로 default·dark SVG를 만든다. exit `2`는 renderer unavailable이므로 해당 render를 미검증으로 보고하고 같은 조건의 재시도는 하지 않는다. renderer 설치·수정은 현재 요청에 포함될 때만 진행한다.

학습용 code·memory·exception 흐름에서는 AI raster image를 만들지 않는다. `woon resolve repo://skills/standards/learning-content-quality.md`의 diagram gate를 적용해 실제 identifier, 의미 있는 공간 구획, 번호가 붙은 arrow, diagram 뒤의 관찰 설명으로 같은 정보 품질을 만든다. 단, PDF·웹·문서에 실제 UI·측정 chart·강의 도판 같은 설명력 높은 source figure가 있으면 Mermaid로 다시 그려 버리지 않는다. 원본 asset의 보존·권리·privacy·본문 매핑은 `repo://skills/skills/knowledge/ingest/references/source-assets.md`를 따른다.

Obsidian `.canvas`를 요청해도 검증된 Markdown Mermaid를 삭제하거나 색만으로 필수 의미를 표현하지 않는다. Canvas는 같은 identifier·단계를 유지하고 Obsidian·공개 renderer를 별도 검증한 보조물로만 둔다. 세부 계약은 `woon resolve repo://skills/standards/obsidian-compatibility.md`를 읽는다.
