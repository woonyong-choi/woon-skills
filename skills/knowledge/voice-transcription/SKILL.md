---
name: voice-transcription
description: 사용자가 제공한 녹음을 승인한 OpenAI STT로 전사하고 화자·시간·원본 날짜를 보존하며 비공개 아카이빙할 때 사용한다. 기존 텍스트만 다듬는 요청에는 적용하지 않는다.
---

# Voice Transcription

원본 녹음과 새 전사 응답의 소유자는 비공개 intake다. Wiki 반영은 `$archive`와 기존 compiler 소유 절차에 맡긴다. 외부 음성 전송에는 `$safety`를 함께 적용하고, 사용자가 이미 지정한 서비스·대상·비용과 실행 승인을 재사용한다.

- Apple 등 기존 저품질 전사는 사용자가 정한 식별 범위에만 쓰며 새 STT의 프롬프트나 최종 정본으로 전용하지 않는다.
- 원본 ID·hash·실제 녹음 시작 시각을 보존한다. 일기 날짜는 사용자가 지정한 녹음 날짜이며 복사일·전사일과 분리한다. 동일 음성의 결과는 재사용하되 원본이나 사본은 삭제하지 않는다.
- 등록 adapter는 `repo://core/src/woon_core/voice_transcription.py`다. 실행 환경에 core가 연결된 상태에서 `python -m woon_core.voice_transcription --help`로 CLI를 확인한다. `--check`는 키와 모델 접근만 확인하며, `--run`만 입력 manifest의 선택 음성을 OpenAI에 전송한다.
- API 키는 사용자가 제공·지정한 credential 입력에서만 읽고 출력·receipt·Wiki·Git에 넣지 않는다. 계정 생성이나 새 token 발급은 전사 실행과 별개다.
- manifest에는 음원별 입력 구간, 원본 날짜, SHA-256과 상대 시각 offset을 둔다. 큰 파일은 원본을 보존한 채 API 크기에 맞춰 준비한다. 압축 음성 stream copy를 사용했다면 구간 경계를 검토한다. 업로드 크기뿐 아니라 모델 출력 한도를 함께 고려한다. `gpt-4o-transcribe`의 한국어 대화는 2분 안팎으로 준비하고 경계 문맥을 보존한다. 한도 도달·비정상 반복이 있는 응답은 완성 전사로 쓰지 않으며 adapter가 후속 요청을 중단한다.
- 첫 구간을 읽어 화자 구분·한국어 내용·타임스탬프를 확인한 뒤 계속한다. 빈 전사와 언어 오인식이 반복되면 전체 실행 전에 원인을 진단하며 품질 통과로 간주하지 않는다. 직접 청취를 지원하지 않는 실행 환경에서는 그 한계를 밝히고 정확도 검증을 가장하지 않는다. 녹음·구간이 바뀐 화자 A/B를 동일 인물로 자동 연결하지 않는다. 실명 연결은 확인한 발화나 사용자의 대응 정보에 근거한다.
- 화자 분리보다 전사 정확도를 우선하라는 사용자의 지시가 있으면 일반 전사 모델을 비교할 수 있다. 현재 adapter는 `gpt-4o-transcribe-diarize`, `gpt-transcribe`, `gpt-4o-transcribe`를 지원하며 원응답 폴더를 분리한다. 모델 변경 사유와 새 요금을 기록하고, 일반 전사 결과에 없는 화자·문장별 시각을 만들어 넣지 않는다.
- adapter는 네트워크 호출 전 요청을 journal에 기록한다. 완료 응답을 로컬에 저장·재조회한 구간만 완료 처리하고 재실행 때 건너뛴다. 결과가 불명확하거나 HTTP 실패가 나면 자동 재전송하지 않는다. 성공한 응답을 잃은 재처리 비용은 별도 승인 범위에서 판단한다.
- 모델 원응답, 시간·화자를 보존한 전사, 읽기용 정리를 구분한다. 들리지 않는 내용은 추측해 채우지 않고 표시한다. 이전 잘못된 정본은 채택 대상에서 제외하며 원문 보존 지시를 지킨다.

요금은 [OpenAI pricing](https://developers.openai.com/api/docs/pricing), 입력·diarization 형식은 [file transcription](https://developers.openai.com/api/docs/guides/speech-to-text)에서 확인한다. 분당 비용은 추정치이며 실제 결제와 구분한다. 앱 제목 변경은 별도의 등록된 직접 adapter와 재조회가 마련된 경우에만 수행한다.
