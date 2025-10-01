# VibeTube (Flask)

유튜브와 비슷한 레이아웃의 간단한 데모 웹앱입니다. 홈 그리드, 검색, 시청 페이지, 추천 목록을 제공합니다.

## 실행 방법 (Windows)
1) 프로젝트 내 가상환경 파이썬을 사용해 의존성 설치 및 실행:

```
venv\Scripts\python -m pip install -r requirements.txt
venv\Scripts\python main.py
```

브라우저에서 `http://127.0.0.1:5000` 로 접속합니다.

## 폴더 구조
- `main.py`: Flask 앱, 라우트, 샘플 데이터
- `templates/`: `base.html`, `index.html`, `watch.html`
- `static/`: `styles.css`, `app.js`

## 참고
- 썸네일은 `picsum.photos`, 비디오는 `samplelib.com` 미리보기 URL을 사용합니다.
- 학습용 데모로, 업로드/DB 연동은 없습니다.
