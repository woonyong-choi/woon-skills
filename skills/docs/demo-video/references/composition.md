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
첫·끝을 이어 움직임과 기능 상태가 자연스럽게 연결되는지 검사한다. 모든 루프에 첫·끝
픽셀 일치를 강제하지 않으며, 실제 차이와 시각 검토를 기록한다. 역방향 재생으로 실행
취소를 꾸미지 않는다.

## 색과 캡처 준비

- 첫 프레임 전에 실제 앱 준비 신호, 사용할 timeline, `document.fonts.ready`와 이미지
  decode를 확인한다. 초기화가 끝나기 전 DOM이나 빈 caption은 완성 프레임이 아니다.
  HyperFrames 0.8.38의 virtual clock은 초기화 중 `requestAnimationFrame` 대기를 멈출
  수 있다. `--no-best-effort`로 timeout을 실패 처리하고 준비 신호를 고치거나, 원본
  composition의 준비를 기다리는 프로젝트 캡처 도구를 사용한다. 고정 지연 증가만으로
  통과하지 않는다. 재현용 clock 변경은 캡처 페이지에 한정하고 값·입력 hash를 기록한다.
- 정확한 UI 색은 PNG RGB에서 GIF를 직접 만든다. 손실 MP4를 거쳐 GIF를 만들면
  RGB/YUV 변환과 palette/dither가 겹쳐 배경이 변할 수 있다. 실행기의 UI 경로는
  [전체 histogram palette](https://ffmpeg.org/ffmpeg-filters.html#palettegen)와 dither 없는
  양자화를 사용한다. 일반 영상의 `--video` 경로를 UI 원색 보존 검증으로 재사용하지 않는다.
- PNG sequence는 `frame_000001.png`부터 시작한다. Alpha export가 root 배경을 제거했는지
  확인하고 원래 canvas를 합성한다. `--background`는 실제 단색 canvas용이며, gradient나
  이미지 배경을 임의 단색으로 바꾸는 옵션이 아니다. 크기·길이는 입력을 따른다.
- [RGB lossless MP4](https://ffmpeg.org/ffmpeg-codecs.html#libx264_002c-libx264rgb)는 편집용이다.
  색 정확성과 재생 호환성을 구분한다. 납품 GIF/MP4를 다시 디코딩해 지정한 단색 영역의
  실제 RGB, 작은 글자·선, 대표 동작과 seam을 확인한다. 중요 배경은 모든 프레임을
  검사하고, 256색 GIF의 차이를 숨기지 않는다. 알려진 모서리 raster 차이의 시각 검토를
  일반 seam 결함 허용으로 확대하지 않는다.
- 출력 receipt의 기본 재생·색·seam 검증 표시는 미확인이다. 이번 출력의 실제 확인
  근거를 더하고 이전 파일의 browser/native 통과 표시를 복사하지 않는다. 최종 파일과
  source/sequence hash를 확정한 뒤 참조와 복구 필요가 없는 중간 PNG·실패 출력만 정리한다.

[Manta의 공개 검증 예시](https://github.com/woonyong-choi/manta-diagrams/blob/64dfeb3cf59cbf66aa429e0acbc932b923ff4352/demo/README.md)는
준비 교착, 원색 복원과 경계 차이를 분리한다. 해당 제품의 해상도·6초 길이·배경색은
다른 영상의 필수값이 아니다.
