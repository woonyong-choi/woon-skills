---
name: publish
description: private woon-knowledge의 승인된 문서를 공개 WIKI·사이트용 산출물로 선별·변환·검증해 발행할 때 사용한다. 내부 저장에는 사용하지 않는다.
---

# Publish

private source와 public output을 분리한다. `publish:true` 같은 metadata는 repository 공개 권한이 아니다.

현재 요청과 대화에서 승인된 candidate·destination·공개 범위를 확인한다. 단순 작성·정리 요청에서 공개 권한을 추론하지 않지만, 같은 산출물과 범위에 대한 구체적인 반영 승인은 재사용한다. 공개 권리와 개인정보 판단은 작업 승인과 별도로 검증한다.

1. source ID·revision, 포함·제외 claim, 개인정보·권리 판단과 미확인 사항을 정리하고 로컬 후보·검증을 완료한다. public source 반영 권한이 아직 없을 때만 검토 가능한 후보와 승격 영수증을 제시해 해당 반영 승인을 요청한다.
2. 공개할 최종 입력의 secret, 개인정보, 회사 내부 자료, 비공개 link와 source session ID를 검사한다. 승인 뒤 입력이 바뀌지 않았다면 같은 검증 근거를 재사용한다.
3. 승인된 public source만 deterministic하게 쓰고 build·rendered link·navigation을 검증한다.
4. repository visibility, target branch와 destination을 확인하되 private repository 자체를 public으로 바꾸지 않는다.
5. commit, push와 deploy는 반영 승인에 포함되지 않는다. 각각 명시적으로 요청된 범위만 수행하고 live artifact identity를 확인한다.

블로그와 포트폴리오처럼 같은 근거를 서로 다른 독자용으로 승격할 때는 `$site-promotion`이 candidate와 claim 일관성을 먼저 소유한다.

Obsidian용 private 정본을 Quartz·WIKI로 변환하거나 wikilink를 검사할 때는 `woon resolve repo://skills/standards/obsidian-compatibility.md`를 읽어 형식 호환성과 공개 경계를 함께 검증한다.
