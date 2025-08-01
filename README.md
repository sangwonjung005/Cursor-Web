# BMS 데이터 분석 대시보드

BMS 센서 데이터 전처리 및 PCA 분석 결과를 보여주는 웹 대시보드입니다.

## 📊 주요 기능

- **데이터 전처리 요약**: 267개 파일, 7,252,377행 데이터 처리
- **평균 요약**: device_no별 센서 평균값 계산
- **PCA 분석 결과**: 2D/3D PCA 그래프 시각화
- **결측치 처리**: NaN 값 처리 방법
- **결과 파일**: 생성된 분석 파일 목록

## 🚀 실행 방법

### 방법 1: 직접 HTML 파일 열기 (가장 간단)
```bash
# index.html 파일을 웹 브라우저에서 직접 열기
# 파일을 더블클릭하거나 브라우저에서 파일 열기
```

### 방법 2: Python 내장 서버 사용
```bash
# Python이 설치되어 있는 경우
python -m http.server 8000
# 웹 브라우저에서 http://localhost:8000 접속
```

### 방법 3: Node.js 서버 사용
```bash
# Node.js가 설치되어 있는 경우
node server.js
# 웹 브라우저에서 http://localhost:3000 접속
```

### 방법 4: Flask 서버 사용
```bash
# Python과 Flask가 설치되어 있는 경우
pip install -r requirements.txt
python app.py
# 웹 브라우저에서 http://localhost:5000 접속
```

## 🌐 웹사이트 링크 공유

### 로컬에서 실행하는 경우:
- **본인 접속**: `http://localhost:8000` (또는 사용한 포트)
- **다른 사람과 공유**: `http://[당신의IP주소]:8000`

### IP 주소 확인 방법:
```bash
# Windows
ipconfig

# 또는 PowerShell에서
Get-NetIPAddress -AddressFamily IPv4
```

## 📁 파일 구조

```
bms_web_app/
├── index.html          # 메인 웹페이지
├── app.py             # Flask 서버 (선택사항)
├── server.js          # Node.js 서버 (선택사항)
├── requirements.txt   # Python 패키지 목록
├── package.json       # Node.js 설정
└── README.md         # 이 파일
```

## 🎨 그래프 기능

- **2D PCA 그래프**: 메인 클러스터와 아웃라이어 구분
- **3D PCA 그래프**: device_no별 색상 구분
- **Canvas 기반 렌더링**: 모든 브라우저에서 호환
- **반응형 디자인**: 모바일/데스크톱 모두 지원

## 🔧 기술 스택

- **HTML5**: 웹페이지 구조
- **CSS3**: 스타일링 및 반응형 디자인
- **JavaScript**: Canvas 그래프 렌더링
- **Bootstrap 5**: UI 프레임워크
- **Font Awesome**: 아이콘

## 📈 데이터 분석 결과

### 통계 요약
- 처리된 파일 수: 267개
- 총 데이터 행 수: 7,252,377행
- 총 데이터 열 수: 308열
- 총 차량 수: 4대

### PCA 분석
- **2D PCA**: 주요 클러스터와 아웃라이어 포인트 구분
- **3D PCA**: device_no별 클러스터 분석
- **결과**: 차량 간 특성과 아웃라이어 명확히 확인

## 🤝 공유 방법

1. **로컬 네트워크 공유**: 같은 WiFi 네트워크에서 IP 주소로 접속
2. **GitHub Pages**: GitHub에 업로드하여 무료 호스팅
3. **Netlify/Vercel**: 무료 클라우드 호스팅 서비스 사용

## 📞 지원

문제가 있거나 추가 기능이 필요하시면 언제든지 문의해주세요! 