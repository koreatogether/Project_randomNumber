# 🔧 트러블슈팅 가이드

Random Number Generator 프로젝트 개발 중 발생할 수 있는 일반적인 문제들과 해결 방법을 정리한 문서입니다.

## 📋 목차

- [Git 관련 문제](#git-관련-문제)
- [개발 환경 문제](#개발-환경-문제)
- [코드 품질 도구 문제](#코드-품질-도구-문제)
- [빌드 및 테스트 문제](#빌드-및-테스트-문제)
- [IDE 연동 문제](#ide-연동-문제)

## Git 관련 문제

### 🚨 VSCode에서 Git Push 버튼 비활성화

**증상:** VSCode의 Git 탭에서 Push, Pull, Sync 버튼이 비활성화됨

**해결 방법:**
```bash
# 1. 브랜치 추적 설정
git branch --set-upstream-to=origin/main main

# 2. 원격과 동기화
git pull --rebase origin main

# 3. 푸시 테스트
git push origin main
```

**자세한 가이드:** [docs/GIT_TROUBLESHOOTING.md](./docs/GIT_TROUBLESHOOTING.md)

### 🔄 Merge Conflict 해결

**증상:** 여러 브랜치에서 같은 파일을 수정했을 때 충돌 발생

**해결 방법:**
```bash
# 1. 충돌 파일 확인
git status

# 2. 수동으로 충돌 해결 후
git add .
git commit -m "Resolve merge conflict"

# 3. 푸시
git push origin main
```

## 개발 환경 문제

### 🐍 Python 가상환경 문제

**증상:** 패키지 설치 오류 또는 import 에러

**해결 방법:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🟨 Node.js/JavaScript 환경 문제

**증상:** ESLint 실행 안됨, 모듈 찾기 오류

**해결 방법:**
```bash
# 1. Node.js 버전 확인
node --version
npm --version

# 2. 패키지 재설치
npm install

# 3. ESLint 직접 설치
npm install -g eslint
```

### 🔵 C++/Arduino 환경 문제

**증상:** 컴파일 오류, 라이브러리 찾기 실패

**해결 방법:**
```bash
# 1. PlatformIO 환경 확인
pio --version

# 2. 라이브러리 업데이트
pio lib update

# 3. 빌드 클린
pio run -t clean
pio run
```

## 코드 품질 도구 문제

### 🔍 코드 품질 체커 실행 오류

**증상:** `python tools/code_quality_checker.py` 실행 시 오류

**해결 방법:**
```bash
# 1. 인코딩 문제 해결
set PYTHONIOENCODING=utf-8
python tools/code_quality_checker.py

# 2. 의존성 설치
pip install ruff black pytest

# 3. 도구별 개별 설치
pip install cppcheck  # Windows에서는 별도 설치 필요
npm install -g eslint
```

### 🎯 Ruff 자동 수정 실패

**증상:** Auto-fix 기능이 작동하지 않음

**해결 방법:**
```bash
# 1. 수동 실행
python -m ruff check --fix src/python/

# 2. Black 포맷팅
python -m black src/python/

# 3. 설정 파일 확인
# pyproject.toml의 [tool.ruff.lint] 섹션 확인
```

## 빌드 및 테스트 문제

### 🧪 pytest 실행 실패

**증상:** 테스트 실행 중 import 오류 또는 실패

**해결 방법:**
```bash
# 1. PYTHONPATH 설정
export PYTHONPATH="${PYTHONPATH}:./src"  # macOS/Linux
set PYTHONPATH=%PYTHONPATH%;./src        # Windows

# 2. 테스트 실행
python -m pytest tests/ -v

# 3. 특정 테스트 실행
python -m pytest tests/unit/test_random_generator.py -v
```

### 🏗️ 멀티언어 빌드 실패

**증상:** 여러 언어 동시 빌드 시 오류

**해결 방법:**
```bash
# 1. 개별 언어별 테스트
python tests/unit/test_random_generator.py    # Python
pio run                                       # C++/Arduino
node src/javascript/random_generator.js       # JavaScript

# 2. 통합 테스트 도구 사용
python tools/build_and_test.py
```

## IDE 연동 문제

### 💻 VSCode 확장 프로그램 문제

**증상:** Python, C++, JavaScript 지원 안됨

**해결 방법:**
1. 필수 확장 프로그램 설치:
   - Python
   - C/C++
   - ESLint
   - PlatformIO IDE
   - GitLens

2. 설정 확인:
   - Python 인터프리터 경로
   - ESLint 실행 경로
   - Git 경로

### 🔌 IntelliSense 작동 안함

**증상:** 자동완성, 오류 표시 안됨

**해결 방법:**
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
  "eslint.workingDirectories": ["src/javascript"],
  "C_Cpp.default.includePath": ["src/cpp"]
}
```

## 🆘 긴급 상황 대처

### 전체 환경 재설정

```bash
# 1. Git 백업
git stash
git branch backup-$(date +%Y%m%d)

# 2. 가상환경 재생성
rm -rf venv/  # 또는 rmdir /s venv (Windows)
python -m venv venv
source venv/bin/activate  # 또는 venv\Scripts\activate

# 3. 의존성 재설치
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. 노드 모듈 재설치
rm -rf node_modules/
npm install

# 5. 전체 테스트
python tools/run_all_checks.bat
```

## 📞 도움 요청

문제가 해결되지 않을 경우:

1. **로그 수집:**
   ```bash
   # 오류 로그를 파일로 저장
   python tools/code_quality_checker.py > debug.log 2>&1
   ```

2. **환경 정보 수집:**
   ```bash
   python --version
   node --version
   git --version
   pip list
   ```

3. **이슈 등록:**
   - GitHub Issues에 상세한 오류 메시지와 환경 정보 포함

## 📚 관련 문서

- [개발 프로세스 가이드](./docs/DEVELOPMENT_PROCESS.md)
- [도구 사용 가이드](./docs/TOOLS_GUIDE.md)
- [Git 상세 트러블슈팅](./docs/GIT_TROUBLESHOOTING.md)
- [테스팅 가이드](./docs/TESTING_GUIDE.md)

---

*이 문서는 실제 발생한 문제들을 기반으로 작성되었으며, 지속적으로 업데이트됩니다.*