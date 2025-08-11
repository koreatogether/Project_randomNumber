# Random Number Generator Project

다양한 언어로 구현한 랜덤 숫자 생성 프로젝트입니다.

## 🎯 프로젝트 목표

3개의 숫자(0, 1, 2)를 랜덤으로 추출하되, 다음 조건을 만족하는 알고리즘을 구현합니다:

### 조건
- 3개의 숫자(0, 1, 2)를 랜덤으로 추출
- **이전에 나왔던 바로 직전 숫자가 나오지 않도록 추출**
- 반복문(for, while 등) 사용 불가
- 논리 연산자(|| 또는 &&) 사용 불가

## 🔧 구현 언어
- Arduino C++
- Python
- JavaScript
- C++
- 기타 언어들

## 📊 성능 비교
각 언어별 구현의 가독성, 실행 속도, 메모리 사용량을 비교 분석합니다.

## 🚀 빠른 시작

### 개발 환경 설정
```bash
# 1. 자동 개발 환경 설정 (권장)
python tools/setup_dev_environment.py

# 2. 수동 설정
# Python 가상환경 생성
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 의존성 설치
pip install -r requirements-dev.txt

# PlatformIO 설치 및 초기화
pip install platformio
pio project init --project-dir .
```

### 빠른 검증
```bash
# 가상환경 활성화 후
python tools/quick_test.py
```

## 📁 프로젝트 구조
```
project_randomNumber/
├── src/
│   ├── arduino/          # Arduino 구현
│   ├── python/           # Python 구현  
│   ├── cpp/              # C++ 구현
│   └── javascript/       # JavaScript 구현
├── tests/                # 테스트 코드
├── docs/                 # 문서
├── tools/                # 개발 도구
└── benchmarks/           # 성능 비교 결과
```

## 🔧 개발 도구

### 코드 품질 검사
```bash
# 전체 언어 코드 품질 검사
python tools/code_quality_checker.py

# 개별 언어별 린팅, 포맷팅, 정적 분석
```

### 빌드 및 테스트
```bash
# 모든 언어 빌드 및 테스트 실행
python tools/build_and_test.py

# Arduino, Python, JavaScript, C++ 빌드/테스트
```

### 성능 분석
```bash
# 언어별 성능 비교 분석
python tools/performance_analyzer.py

# 실행 시간, 메모리 사용량, 품질 점수 측정
```

### 통합 검사
```bash
# Windows: 모든 검사 도구 실행
tools/run_all_checks.bat

# 또는 개별 실행
python tools/quick_test.py           # 빠른 기능 검증
python tools/code_quality_checker.py # 코드 품질
python tools/build_and_test.py      # 빌드/테스트
python tools/performance_analyzer.py # 성능 분석
```

## 📊 검사 결과 확인

모든 검사 결과는 `logs/` 디렉토리에 저장됩니다:

```
logs/
├── quality/          # 코드 품질 검사 결과
├── build_test/       # 빌드 및 테스트 결과  
└── performance/      # 성능 분석 결과
```

## 📈 벤치마크 결과
성능 분석 도구를 통해 언어별 비교 결과를 확인할 수 있습니다:
- 실행 시간 비교
- 메모리 사용량 분석
- 랜덤 숫자 생성 품질 검증
- 조건 만족도 측정 (이전 숫자와 다른 숫자 생성)