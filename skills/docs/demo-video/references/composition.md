# 재현 가능한 HTML 장면

원본: [HyperFrames core](https://github.com/heygen-com/hyperframes/blob/f6041d7597c8c53d381d4c27feb86b305b3317a4/skills/hyperframes-core/SKILL.md),
[CLI](https://github.com/heygen-com/hyperframes/blob/f6041d7597c8c53d381d4c27feb86b305b3317a4/skills/hyperframes-cli/SKILL.md).
Apache-2.0 프로젝트의 공개 구성 계약을 참고했다. Woon은 실제 제품 출처·로컬 렌더·최소
설치·원본 보존을 소유하며 vendor의 자동 설치·telemetry·feedback 절차를 가져오지 않는다.

- `index.html`의 body 바로 아래 크기를 가진 root를 둔다. `data-composition-id`,
  `data-width`, `data-height`, `data-duration`을 선언하고 CSS 크기는 `100%`로 둔다.
- 같은 ID로 `window.__timelines[id]`에 paused GSAP timeline 하나를 등록한다.
  GSAP·폰트·이미지를 로컬에 두고 자산을 모두 읽은 뒤 렌더한다.
- 시간 구간에는 `data-start`, `data-duration`을 사용한다. clip 자체의 visibility,
  display, autoAlpha를 애니메이션하지 않는다. 내부 요소의 opacity·transform을 움직인다.
- CSS 초기 transform과 GSAP transform을 같은 요소에서 경쟁시키지 않는다.
  `fromTo`로 시작과 끝을 명시하고 양방향 seek에서 같은 화면이 나오게 한다.
- 실제 시각·무작위값·네트워크 응답·마우스 상태로 프레임을 만들지 않는다.
- 짧은 제품 소개는 단일 composition을 우선한다. 영상에 나온 중첩 장면의 빈 화면
  문제를 회피한다고 기능을 감추지 말고, 각 장면에서 실제 픽셀이 있는지 확인한다.
- 제품 화면을 확대하는 편집은 가능하나 작동하지 않는 버튼·저장·성공 알림을 합성하지 않는다.
  과거 버전 화면을 재사용했다면 촬영 버전과 현재 버전의 차이를 공개 설명에 남긴다.

```sh
DO_NOT_TRACK=1 npm exec --yes --package=hyperframes@0.8.38 -- hyperframes check ./demo/intro --snapshots
DO_NOT_TRACK=1 npm exec --yes --package=hyperframes@0.8.38 -- hyperframes snapshot ./demo/intro --at 0.5,3,6
```

README·Community의 기본 매체는 `![행동과 결과 설명](intro.gif)`다. GIF에 무한 반복
메타데이터를 넣어 재생 버튼 없이 표시한다. MP4 링크나 플레이어로 대체하지 않는다.
웹 video가 별도로 요청됐다면 `autoplay muted loop playsinline`을 사용하고
`prefers-reduced-motion`에서는 정지한다. 영상 제작용 HTML은 새 소개 사이트가 아니다.
입력·선택·탐색은 빠르게, 결과는 약 0.6~1초 보여준다. 촬영 커서와 클릭 표시를 숨기고
첫·끝 픽셀 및 기능 상태가 일치하는지 검사한다. 역방향 재생으로 실행 취소를 꾸미지 않는다.
