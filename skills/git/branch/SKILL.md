---
name: branch
description: Git 브랜치를 만들고 이름을 정하거나 GitHub Flow, trunk-based, GitFlow, merge와 rebase 전략을 판단할 때 사용한다.
---

# Branch

저장소의 protected branch, CI, release 방식, feature flag, 협업자를 먼저 확인한다.

- 기본은 `main`에서 짧은 `feat/<slug>` 또는 `fix/<slug>` 브랜치를 만든다.
- 사용자의 플러그인 저장소는 `main`을 정본으로 유지하고, 기능 개발과 긴급 수정 동안만 `feature/<slug>` 또는 `hotfix/<slug>`를 쓴다. 개발 완료 후 관련 검증을 통과한 변경을 `main`에 병합·push하고 remote SHA를 확인한 뒤, 병합 완료가 확인된 local·remote 작업 브랜치만 삭제한다. 다른 담당이 작업 중인 브랜치와 worktree는 보존하며 이 규칙을 다른 Woon 저장소의 일괄 브랜치 삭제 권한으로 확대하지 않는다.
- 공유·push된 branch는 rebase로 history를 바꾸지 않는다.
- merge 방식은 저장소 정책을 따르며, 확실하지 않으면 PR의 허용 방식부터 확인한다.
- 여러 버전 유지와 release train이 실제로 없으면 GitFlow를 도입하지 않는다.
- branch 생성·전환 전 dirty state와 base SHA를 기록한다.

branch 삭제나 강제 갱신은 `$safety`를 함께 적용한다.
