# Arduino Multi-Implementation Comparison System

여러 Arduino 랜덤 숫자 생성기 구현을 동시에 비교하고 분석하는 시스템입니다.

## 🚀 주요 기능

### 1. 다중 구현 시뮬레이터
- **최대 20개**의 다양한 Arduino 구현 방식 지원
- **YAML 설정 파일**로 쉬운 구현 정의
- **자동 성능 벤치마킹**
- **실시간 비교 분석**

### 2. 비교 대시보드
- **인터랙티브 웹 대시보드** (http://localhost:8051)
- **실시간 성능 차트**
- **구현별 상세 분석**
- **최적 구현 추천 시스템**

### 3. 지원하는 구현 방식
1. **Lookup Table v1** - 기본 3x3 룩업 테이블
2. **Optimized Lookup Table** - 개선된 룩업 테이블
3. **If-Else Chain** - 조건문 체인 방식
4. **Switch-Case Style** - 딕셔너리 기반 스위치
5. **Mathematical Formula** - 수학 공식 기반
6. **Bitwise Operations** - 비트 연산 활용
7. **Retry Method** - 재시도 방식
8. **Weighted Selection** - 가중치 기반 선택
9. **Circular Pattern** - 순환 패턴
10. **Hybrid Approach** - 하이브리드 방식

## 📁 파일 구조

```
arduino_implementations.yaml    # 구현 정의 설정 파일
src/arduino_simulation/
├── multi_implementation_sim.py # 다중 구현 시뮬레이터
├── multi_dashboard.py         # 비교 대시보드
├── arduino_mock.py           # Arduino 하드웨어 시뮬레이션
└── random_generator_sim.py   # 기본 시뮬레이터
```

## 🛠️ 사용법

### 1. 구현 정의 (arduino_implementations.yaml)

```yaml
implementations:
  - id: "my_custom_impl"
    name: "My Custom Implementation"
    description: "사용자 정의 구현"
    type: "lookup_table"
    enabled: true
    lookup_table:
      - [1, 2, 0]  # 이전이 0일 때
      - [2, 0, 1]  # 이전이 1일 때
      - [0, 1, 2]  # 이전이 2일 때
    expected_performance: "high"
    memory_usage: "low"
```

### 2. 명령줄에서 실행

```bash
# 다중 구현 테스트
python src/arduino_simulation/multi_implementation_sim.py

# 비교 대시보드 실행
python src/arduino_simulation/multi_dashboard.py
```

### 3. 프로그래밍 방식 사용

```python
from src.arduino_simulation.multi_implementation_sim import run_multi_implementation_test

# 모든 구현 비교 실행
report = run_multi_implementation_test(
    iterations=10000,
    seed=12345
)

print(f"추천 구현: {report.recommended_implementation}")
print(f"최고 성능: {report.best_performance}")
```

## 📊 성능 결과 (5,000회 테스트)

| 구현 방식 | 속도 (gen/sec) | 제약 위반 | 상태 |
|-----------|----------------|-----------|------|
| **Optimized Lookup Table** | **2,293,975** | 0 | ✅ 추천 |
| Lookup Table v1 | 2,110,660 | 0 | ✅ |
| Mathematical Formula | 2,029,960 | 1,657 | ⚠️ |
| Bitwise Operations | 1,917,484 | 0 | ✅ |
| Circular Pattern | 1,748,938 | 0 | ✅ |
| Switch-Case Style | 1,612,450 | 0 | ✅ |
| If-Else Chain | 1,581,682 | 0 | ✅ |
| Weighted Selection | 939,753 | 0 | ✅ |
| Hybrid Approach | 776,148 | 175 | ⚠️ |
| Retry Method | 627,326 | 0 | ✅ |

## 🎯 추천 시스템

시스템은 다음 기준으로 최적 구현을 추천합니다:

- **성능** (30%): 생성 속도
- **메모리 효율성** (20%): SRAM 사용량
- **코드 단순성** (20%): 구현 복잡도
- **신뢰성** (20%): 제약 조건 준수
- **유지보수성** (10%): 코드 가독성

## 🔧 커스터마이징

### 새로운 구현 추가

1. `arduino_implementations.yaml`에 새 구현 정의
2. 필요시 `ImplementationGenerator` 클래스에 새 메서드 추가
3. 대시보드에서 자동으로 인식 및 테스트

### 테스트 설정 변경

```yaml
test_config:
  default_iterations: 20000      # 기본 반복 횟수
  default_seed: 54321           # 기본 시드
  performance_benchmark_iterations: 100000
```

## 🌐 대시보드 기능

### 실시간 모니터링
- 구현별 실행 진행률
- 성능 메트릭 실시간 업데이트
- 오류 발생 시 즉시 알림

### 비교 차트
- **속도 비교**: 생성 속도 막대 차트
- **메모리 사용량**: 메모리 효율성 비교
- **분포 품질**: 균등 분포 달성도
- **제약 준수**: 연속 숫자 위반 횟수

### 상세 분석
- 구현별 상세 결과 테이블
- 분포 히스토그램
- 성능 트렌드 분석
- 추천 이유 설명

## 🚀 빠른 시작

```bash
# 1. 의존성 설치
pip install pyyaml dash plotly pandas

# 2. 기본 테스트 실행
python src/arduino_simulation/multi_implementation_sim.py

# 3. 대시보드 실행
python src/arduino_simulation/multi_dashboard.py

# 4. 브라우저에서 확인
# http://localhost:8051
```

## 📈 확장 가능성

- **더 많은 구현 방식** 추가 가능 (최대 20개)
- **커스텀 메트릭** 정의 가능
- **다양한 제약 조건** 테스트 가능
- **성능 프로파일링** 상세 분석
- **Arduino 보드별** 최적화 비교

---

**🎉 이제 여러분만의 Arduino 구현을 추가하고 최적의 성능을 찾아보세요!**