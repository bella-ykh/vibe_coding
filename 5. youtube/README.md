# YouTube Downloader

유튜브 동영상을 쉽고 빠르게 다운로드할 수 있는 웹 애플리케이션입니다.

## 기능

- 🎥 유튜브 동영상 정보 조회
- 📱 반응형 웹 디자인
- 🎨 모던하고 직관적인 UI
- 📊 다양한 품질 옵션 선택
- ⚡ 실시간 다운로드 진행 상황 표시
- 🔍 URL 유효성 검사

## 설치 및 실행

### 1. 가상환경 활성화
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행
```bash
python main.py
```

### 4. 웹 브라우저에서 접속
```
http://localhost:5000
```

## 사용 방법

1. 웹 브라우저에서 `http://localhost:5000`에 접속
2. 유튜브 동영상 URL을 입력창에 붙여넣기
3. "동영상 정보 가져오기" 버튼 클릭
4. 원하는 품질 선택
5. "다운로드 시작" 버튼 클릭

## 지원하는 URL 형식

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- 기타 유튜브 URL 형식

## 기술 스택

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **동영상 다운로드**: yt-dlp
- **UI Framework**: Font Awesome (아이콘)

## 주의사항

- 이 도구는 개인적인 용도로만 사용해주세요
- 저작권이 있는 콘텐츠의 다운로드는 해당 저작권 정책을 준수해주세요
- 대용량 동영상의 경우 다운로드 시간이 오래 걸릴 수 있습니다

## 문제 해결

### yt-dlp 설치 오류
```bash
pip install --upgrade pip
pip install yt-dlp
```

### 포트 충돌 오류
`main.py` 파일에서 포트 번호를 변경할 수 있습니다:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 포트 5001로 변경
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
