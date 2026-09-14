# Approved Obsidian plugins

제품군 표시명은 Manta다. 아래 표시명과 설치 ID를 구분하며 기존 ID·repository·release 이력은 유지한다.

| ID | Community Plugin | Official release repository | Intended role |
| --- | --- | --- | --- |
| `light-mindmap` | Light Mindmap | `ninglg/light-mindmap` | 한 Markdown 문서의 heading을 학습·리허설·발표용 mindmap으로 렌더 |
| `markdown-mindmap` | Markdown Mindmap | `kikocastro/markdown-mindmap` | frontmatter 관계를 읽어 여러 Markdown 문서를 프로젝트·키워드·질문 지도로 렌더 |
| `link-calendar` | Manta Calendar | `woonyong-choi/manta-calendar` | 날짜가 있는 Markdown을 월간 보기와 날짜별 정본 링크로 탐색한다. Google 연동과 일반 Markdown source의 편집 권한을 분리한다 |
| `linked-graph` | Manta Graph | `woonyong-choi/manta-graph` | 현재 Markdown의 공개 정본 outgoing 1-hop을 기본 그래프와 목차로 탐색하고, hover·focus 동안만 실제 outgoing 2-hop을 미리 본다. private·source·generated·archive 경로와 archived·retired·superseded destination·parent는 제외하며 지식이나 UI 상태를 저장하지 않는다 |
| `runnable-code-blocks` | Manta Code Blocks | `woonyong-choi/manta-code-blocks` | 21개 `run-<language>` fence를 browser 또는 named remote provider에서 명시적인 Run으로만 실행한다 |

## Local development allowlist

| ID | Source repository | Boundary |
| --- | --- | --- |
| `manta-diagrams` | `woonyong-choi/manta-diagrams` | Manta Diagrams의 exact `0.1.0` 개발 build를 `install-local-build`와 receipt로 격리 시험 Vault에서만 검증한다. 지원되는 일반 `mermaid` 본문도 Manta로 렌더하고, authored style·link·directive는 원문을 바꾸지 않고 bundled Mermaid로 보존한다. Manta 미지원 입력은 standard Mermaid fallback을 안내하며 유효하지 않은 입력은 원문과 오류를 표시한다. 본문·전체 viewer·browser·demo는 role palette·font·`sanitizeSvg`를 공유하고 Obsidian의 최종 `sanitizeHTMLToDom` 검사를 유지한다. `manta` fence, pan·zoom·SVG export·원문 열람·오류 시 이전 그림 제거·unload를 확인한다. 노트 쓰기·AI 호출·원격 실행은 없다. 원본의 clean HEAD와 origin을 확인하며 개인 Vault 설치·Community 등록·`0.1.0` 최종 출시 완료로 해석하지 않는다. |
| `woon-knowledge` | `woonyong-choi/manta` | Manta의 exact `0.1.0` 개발 build를 명시한 격리 시험 Vault에서만 `install-local-build`와 receipt로 검증한다. 선택한 원자료와 기존 일반 노트의 생성·독립 검토, `Vault.process` 안의 revision 검사, 상태 재조회·보류·취소·undo를 확인한다. 개인 Woon Vault·compiler 정본과 기존 세 플러그인의 설정은 변경하지 않는다. 로컬 소스의 clean HEAD와 origin은 검증하되 공개 GitHub 저장소·release·Community 심사 완료를 뜻하지 않는다. |
| `linked-graph` | `woonyong-choi/manta-graph` | exact `1.6.6` read-only current-note force graph build만 `install-local-build`와 receipt로 검증한다. edge-to-edge viewport와 unclamped ephemeral world, density-responsive spacing, bounds-based fit, pan·zoom, drag-reheated shared simulation, movable root, canonical parent navigation, private·source·generated·archive 및 archived·retired·superseded destination·parent 제외, dot-above-title-below labels, no static group captions, dot-only hover emphasis, no false root action outline, hover·focus·touch outgoing 2-hop preview, direct 120개·preview 48개 상한과 전체 Outline fallback, measured collision, metadata dot colour, neutral text, Obsidian `--graph-line` 기반 1px solid direct edges와 1px dashed preview edges를 실제 Obsidian에서 확인한다. `context-graph`는 이 설치가 검증된 뒤 backup retirement한다. |
| `link-calendar` | `woonyong-choi/manta-calendar` | CI·release asset attestation을 통과한 exact `3.2.0` source build를 `install-local-build`와 receipt로 검증한다. 신규 source read-only 기본값, 낙관적 날짜 충돌 차단, 1회 Undo, 안전한 속성명과 source별 날짜 상태를 확인한다. 구형 `context-calendar`는 이 설치가 검증된 뒤 backup retirement한다. |
| `runnable-code-blocks` | `woonyong-choi/manta-code-blocks` | exact `0.2.4` local build만 `install-local-build`와 receipt로 검증한다. 21개 `run-<language>` fence는 명시적인 Run에서만 실행하며 원격 우선·browser 우선·원격 끄기 설정과 결과 불명 시 중복 실행 차단을 확인한다. 프로젝트 소유 실행 서버·자동 실행·코드 저장·filesystem 접근·child process·runtime 자동 설치·PATH 변경은 허용하지 않고, named third-party provider로 source가 전송될 수 있음을 표시한다. DartPad는 compile API로 source를 전송하고 반환된 JavaScript는 CSS class로 숨긴 임시 sandboxed frame에서 실행한다. Obsidian reload 뒤 전체 언어 목록, 실제 provider 환경, 100 source lines + numbered trailing lines, IntelliJ Darcula syntax palette, compact 편집·Run·conditional Reset·Output을 직접 확인한다. |

두 mindmap plugin은 Markdown 원본을 읽는다. `light-mindmap`의 node 편집은 heading을 바꾸므로 source diff와 link를 재검증해야 하고, `markdown-mindmap`은 map block의 folder·`parent` relation을 다시 읽어 card를 그린다.

`link-calendar`는 여러 folder profile, optional tag filter, 날짜·시간·하루 종일·제목·분류 mapping과 Google 동기화를 지원한다. Tag만으로 Vault 전체를 색인하지 않는다. Apple 전용 source 생성과 projection 설정은 퇴역했으며 기존 source 해제는 상위 SKILL.md의 `retire-apple-calendar-source`만 사용한다. 기존 일정 문서와 Google records는 보존한다. Obsidian reload 뒤 `ribbon`, `month-view`, `event-marker`, `daily-agenda`, `direct-note-link`, 읽기 전용 source의 `readonly-blocked`를 직접 확인한 operator attestation은 현재 version·asset·settings hash에 묶인다. Apple dashboard는 요구하지 않는다. 구형 `context-calendar`, `woon-simple-calendar`, `notion-bases`, `full-calendar-remastered`는 새 설치 대상이 아니라 검증된 대체 후 migration backup 대상이다.
