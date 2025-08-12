"""
Arduino Uno R4 WiFi Simulation Package
정확한 하드웨어 사양을 반영한 Arduino 시뮬레이션 패키지

주요 모듈:
- arduino_mock: Arduino 하드웨어 모킹
- random_generator_sim: Random Number Generator 시뮬레이션
- simulation_runner: 대량 시뮬레이션 실행
- dashboard: 실시간 모니터링 대시보드
"""

from .arduino_mock import ArduinoUnoR4WiFiMock, create_arduino_mock
from .random_generator_sim import RandomNumberGeneratorSim, create_simulation
from .simulation_runner import SimulationRunner, SimulationConfig
from .dashboard import ArduinoSimulationDashboard, run_dashboard

__version__ = "1.0.0"
__author__ = "Arduino Simulation Team"

__all__ = [
    "ArduinoUnoR4WiFiMock",
    "create_arduino_mock", 
    "RandomNumberGeneratorSim",
    "create_simulation",
    "SimulationRunner",
    "SimulationConfig",
    "ArduinoSimulationDashboard",
    "run_dashboard"
]