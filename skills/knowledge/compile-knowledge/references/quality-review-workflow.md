# 품질 평가 실행

650개처럼 전체 corpus를 검토할 때는 payload를 추정해 채우지 않는다. 먼저 `quality-review-plan`으로 현재 page·receipt·writing harness·review prompt가 묶인 immutable batch를 만들고, LLM 또는 사람이 각 batch의 `*.result.json`만 작성한다. `assemble-quality-reviews`가 plan과 현재 receipt를 다시 대조해 하나의 payload로 조립한 뒤에만 위 gate를 실행한다. plan 생성 뒤 문서나 표준이 바뀌면 이전 판정은 stale이며 새 plan부터 다시 시작한다.

```bash
woon knowledge quality-review-plan \
  --vault <vault> \
  --standard "$(woon resolve repo://skills/standards/learning-writing-harness.md)" \
  --prompt "$(woon resolve repo://skills/standards/learning-quality-review-prompt.md)" \
  --output <new-empty-plan-directory> \
  --batch-size 2 \
  --max-batch-chars 24000
```

로컬 Ollama가 있고 Vault를 외부에 보내지 않아도 되는 경우에는 아래 명령으로 아직 없는 batch 결과만 만든다. 기본 batch는 최대 2페이지이면서 Markdown 합계가 `24,000`자를 넘지 않으므로, 큰 페이지는 혼자 검토하고 작은 페이지들만 함께 검토한다. `--max-batch-chars`는 이 상한을 바꾸며, 한 페이지가 상한보다 큰 경우에는 그 페이지를 쪼개지 않고 단독 batch로 남긴다. `OLLAMA_HOST`가 loopback이 아니면 실행을 거부하며, 생성 온도는 0으로 고정한다. review는 기준마다 현재 문서의 서로 다른 anchor를 남긴다. model JSON이 page ID·receipt hash·rubric·근거 계약을 어기면 오류를 넣어 같은 batch를 최대 세 번 다시 요청하고, 끝내 맞지 않으면 결과 파일을 쓰지 않는다. `--max-attempts 1..5`로 한계를 바꿀 수 있다. 전체 corpus에서는 `--continue-on-error true`로 실패 batch의 ID와 오류를 report에 남기면서 다음 batch를 계속 검토한다. 기존 result는 덮어쓰지 않으므로 중단 뒤 같은 명령으로 재개할 수 있다. 결과는 quality evaluator receipt일 뿐 source·claim·page 정본이나 검색 색인이 아니므로, reviewer의 해석을 새 지식으로 편입하지 않는다.

```bash
woon knowledge review-quality-ollama \
  --plan <new-empty-plan-directory>/manifest.json \
  --results <quality-review-results-directory> \
  --model <available-local-model> \
  --batch quality-001
```

plan 생성 뒤 일부 페이지의 receipt만 바뀌었다면 이전 plan이나 result를 직접 고치거나 복사하지 않는다. 아래 명령은 새 immutable plan과 새 results directory를 만들고, writing harness·review prompt·Markdown hash가 모두 같은 **완전한 batch**만 검증해 재사용한다. 변경된 페이지가 있는 batch와 기존에 실패·누락된 batch는 새 results directory에 쓰지 않으므로, 같은 `review-quality-ollama` 명령이 그 batch만 다시 검토한다.

```bash
woon knowledge rebase-quality-review-plan \
  --vault <vault> \
  --prior-plan <old-plan-directory>/manifest.json \
  --prior-results <old-results-directory> \
  --standard "$(woon resolve repo://skills/standards/learning-writing-harness.md)" \
  --prompt "$(woon resolve repo://skills/standards/learning-quality-review-prompt.md)" \
  --output <new-plan-directory> \
  --results <new-results-directory> \
  --batch-size 2 \
  --max-batch-chars 24000
```
