# Arduino Uno R4 WiFi Random Number Generator Simulation

Arduino Uno R4 WiFi에서 실행되는 Random Number Generator의 정확한 Python 시뮬레이션입니다.

## 🎯 프로젝트 개요

이 프로젝트는 Arduino Uno R4 WiFi의 하드웨어 특성을 정확히 반영하여 Random Number Generator 알고리즘을 시뮬레이션합니다.

### 주요 특징
- **정확한 하드웨어 시뮬레이션**: Renesas RA4M1 (48MHz, 32KB SRAM) 사양 반영
- **제약 조건 준수**: 반복문/논리연산자 사용 금지, 연속 동일 숫자 방지
- **룩업 테이블 알고리즘**: 원본 Arduino 코드와 동일한 로직
- **실시간 대시보드**: Dash를 사용한 시각화 및 모니터링
- **성능 벤치마킹**: 10,000회 시뮬레이션 및 통계 분석

## 🏗️ 프로젝트 구조

```
src/
├── arduino_simulation/
│   ├── arduino_mock.py          # Arduino Uno R4 WiFi 하드웨어 모킹
│   ├── random_generator_sim.py  # Random Number Generator 시뮬레이션
│   ├── simulation_runner.py     # 대량 시뮬레이션 실행 엔진
│   └── dashboard.py             # 실시간 모니터링 대시보드
├── tests/
│   └── test_simulation.py       # 테스트 스위트
├── results/                     # 시뮬레이션 결과 저장
└── main.py                      # 메인 실행 파일
```

## 🚀 빠른 시작

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 빠른 테스트 실행
```bash
python src/main.py --quick
```

### 3. 대시보드 실행
```bash
python src/main.py --dashboard
```
브라우저에서 http://localhost:8050 접속

### 4. 성능 벤치마크
```bash
python src/main.py --benchmark
```

### 5. 테스트 스위트 실행
```bash
python src/main.py --test
```

## 📊 Arduino Uno R4 WiFi 하드웨어 사양

| 항목 | 사양 |
|------|------|
| MCU | Renesas RA4M1 (ARM Cortex-M4) |
| 클럭 속도 | 48MHz |
| 플래시 메모리 | 256KB |
| SRAM | 32KB |
| EEPROM | 8KB (에뮬레이션) |
| 디지털 핀 | 14개 (PWM 6개) |
| 아날로그 입력 | 6개 (12-bit ADC) |
| 동작 전압 | 5V |

## 🔧 시뮬레이션 기능

### Arduino Mock 클래스
```python
from arduino_simulation import create_arduino_mock

# Arduino Uno R4 WiFi 모킹
arduino = create_arduino_mock(seed=12345)

# 기본 함수들
arduino.millis()                    # 밀리초 타이머
arduino.micros()                    # 마이크로초 타이머  
arduino.random_range(0, 3)          # 랜덤 숫자 생성
arduino.Serial_println("Hello")     # Serial 출력
arduino.digitalWrite(13, 1)         # 디지털 출력
arduino.analogRead(0)               # 아날로그 입력 (노이즈 포함)
```

### Random Number Generator 시뮬레이션
```python
from arduino_simulation import create_simulation

# 시뮬레이션 환경 생성
arduino, simulator = create_simulation(seed=12345)

# Arduino setup/loop 시뮬레이션
simulator.simulate_arduino_setup()
numbers = simulator.simulate_arduino_loop(20)

# 대량 시뮬레이션 (10,000회)
results = simulator.run_batch_simulation(10000)
```

### 시뮬레이션 러너
```python
from arduino_simulation import SimulationRunner, SimulationConfig

# 설정
config = SimulationConfig(
    iterations=10000,
    seed=12345,
    show_progress=True,
    save_results=True
)

# 실행
runner = SimulationRunner(config)
results = runner.run_single_simulation()

# 다중 시드 테스트
seeds = [11111, 22222, 33333]
multi_results = runner.run_multiple_simulations(seeds)
```

## 📈 대시보드 기능

### 실시간 모니터링
- 시뮬레이션 진행률 및 속도
- 실시간 분포 분석
- 제약 조건 위반 모니터링
- Arduino 하드웨어 상태

### 시각화 차트
- 숫자 분포 히스토그램
- 생성 시퀀스 라인 차트
- 상태 전이 분석
- 성능 메트릭 테이블

### KPI 카드
- 총 생성 횟수
- 초당 생성 속도
- 제약 조건 만족 여부
- SRAM 사용률

## 🧪 테스트 및 검증

### 테스트 항목
1. **Arduino Mock 기능 테스트**
   - 하드웨어 사양 검증
   - 시간 함수 정확성
   - I/O 기능 테스트

2. **Random Generator 시뮬레이션 테스트**
   - 룩업 테이블 로직 검증
   - 제약 조건 만족 테스트
   - 분포 공정성 검증

3. **성능 벤치마크 테스트**
   - 생성 속도 측정
   - 메모리 사용량 모니터링
   - 다중 시드 일관성 검증

### 테스트 실행
```bash
# 전체 테스트 스위트
python src/main.py --test

# 개별 테스트 모듈
python -m pytest src/tests/test_simulation.py -v
```

## 📊 예상 성능 지표

| 메트릭 | 목표값 | 실제 측정값 |
|--------|--------|-------------|
| 생성 속도 | > 10,000 gen/sec | 측정 필요 |
| SRAM 사용률 | < 50% | 측정 필요 |
| 제약 조건 만족률 | 100% | 측정 필요 |
| 분포 균등성 | 30-35% 각 숫자 | 측정 필요 |

## 🔍 알고리즘 상세

### 룩업 테이블 방식
```
이전숫자 \ 후보숫자  │  0  │  1  │  2  │
─────────────────────┼─────┼─────┼─────┤
        0            │  1  │  1  │  2  │
        1            │  0  │  0  │  2  │
        2            │  0  │  1  │  0  │
```

### 동작 원리
1. `candidate = random(0, 3)` - 후보 숫자 생성
2. `result = lookupTable[previous][candidate]` - 테이블 조회
3. `previous = result` - 상태 업데이트
4. 통계 수집 및 분석

## 📁 결과 파일

시뮬레이션 결과는 `src/results/` 디렉토리에 JSON 형식으로 저장됩니다:

```json
{
  "simulation_info": {
    "total_iterations": 10000,
    "generation_rate_per_second": 15000,
    "arduino_board": "Uno R4 WiFi"
  },
  "distribution_analysis": {
    "counts": {"0": 3333, "1": 3334, "2": 3333},
    "percentages": {"0": 33.33, "1": 33.34, "2": 33.33}
  },
  "constraint_verification": {
    "consecutive_violations": 0,
    "constraint_satisfied": true
  }
}
```

## 🛠️ 개발 및 확장

### 새로운 Arduino 보드 추가
1. `HardwareSpecs` 클래스에 새 보드 사양 추가
2. 보드별 특화 기능 구현
3. 테스트 케이스 추가

### 새로운 알고리즘 추가
1. `RandomNumberGeneratorSim` 클래스 확장
2. 룩업 테이블 수정
3. 검증 테스트 추가

### 대시보드 커스터마이징
1. `dashboard.py`에서 레이아웃 수정
2. 새로운 차트 컴포넌트 추가
3. 콜백 함수 확장

## 📚 참고 자료

- [Arduino Uno R4 WiFi 공식 문서](https://docs.arduino.cc/hardware/uno-r4-wifi)
- [Renesas RA4M1 데이터시트](https://www.renesas.com/us/en/products/microcontrollers-microprocessors/ra-cortex-m-mcus/ra4m1-32-bit-microcontrollers-48mhz-arm-cortex-m4-and-lcd-controller-and-cap-touch-hmi)
- [Dash 프레임워크 문서](https://dash.plotly.com/)
- [프로젝트 설계 문서](../docs/architecture/SIMPLIFIED_SIMULATION_DESIGN.md)

## 🤝 기여하기

1. 이슈 리포트 또는 기능 제안
2. 포크 및 브랜치 생성
3. 테스트 추가 및 실행
4. 풀 리퀘스트 제출

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.