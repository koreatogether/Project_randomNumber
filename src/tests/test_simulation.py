"""
Arduino Simulation Test Suite
Arduino Uno R4 WiFi 시뮬레이션의 정확성 및 성능 테스트

테스트 항목:
1. Arduino Mock 기본 기능 테스트
2. Random Number Generator 시뮬레이션 정확성 테스트
3. 제약 조건 검증 테스트
4. 성능 벤치마크 테스트
5. 하드웨어 시뮬레이션 정확성 테스트
"""

import unittest
import time
import sys
import os
from typing import List, Dict, Any

# 상위 디렉토리의 모듈 import를 위한 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from arduino_simulation.arduino_mock import ArduinoUnoR4WiFiMock, create_arduino_mock
from arduino_simulation.random_generator_sim import RandomNumberGeneratorSim, create_simulation
from arduino_simulation.simulation_runner import SimulationRunner, SimulationConfig


class TestArduinoMock(unittest.TestCase):
    """Arduino Mock 기본 기능 테스트"""
    
    def setUp(self):
        """테스트 설정"""
        self.arduino = create_arduino_mock(seed=12345)
    
    def test_hardware_specs(self):
        """하드웨어 사양 테스트"""
        hw_info = self.arduino.get_hardware_info()
        
        # Arduino Uno R4 WiFi 사양 검증
        self.assertEqual(hw_info['board_name'], 'Arduino Uno R4 WiFi')
        self.assertEqual(hw_info['mcu'], 'Renesas RA4M1')
        self.assertEqual(hw_info['clock_speed_mhz'], 48.0)
        self.assertEqual(hw_info['sram_kb'], 32)
        self.assertEqual(hw_info['flash_memory_kb'], 256)
        self.assertEqual(hw_info['digital_pins'], 14)
        self.assertEqual(hw_info['analog_pins'], 6)
        self.assertEqual(hw_info['adc_resolution'], 12)
    
    def test_timing_functions(self):
        """시간 관련 함수 테스트"""
        # millis() 테스트
        start_millis = self.arduino.millis()
        time.sleep(0.1)  # 100ms 대기
        end_millis = self.arduino.millis()
        
        # 약 100ms 차이가 나야 함 (오차 허용)
        self.assertGreaterEqual(end_millis - start_millis, 90)
        self.assertLessEqual(end_millis - start_millis, 110)
        
        # micros() 테스트
        start_micros = self.arduino.micros()
        time.sleep(0.001)  # 1ms 대기
        end_micros = self.arduino.micros()
        
        # 약 1000μs 차이가 나야 함
        self.assertGreaterEqual(end_micros - start_micros, 900)
        self.assertLessEqual(end_micros - start_micros, 1100)
    
    def test_random_functions(self):
        """랜덤 함수 테스트"""
        # 시드 설정 테스트
        self.arduino.randomSeed(54321)
        
        # random_range 테스트
        for _ in range(100):
            num = self.arduino.random_range(0, 3)
            self.assertIn(num, [0, 1, 2])
        
        # random_max 테스트
        for _ in range(100):
            num = self.arduino.random_max(10)
            self.assertGreaterEqual(num, 0)
            self.assertLess(num, 10)
    
    def test_digital_io(self):
        """디지털 I/O 테스트"""
        from arduino_simulation.arduino_mock import PinMode
        
        # pinMode 테스트
        self.arduino.pinMode(13, PinMode.OUTPUT)
        self.assertEqual(self.arduino.digital_pins_mode[13], PinMode.OUTPUT)
        
        # digitalWrite 테스트
        self.arduino.digitalWrite(13, 1)
        self.assertEqual(self.arduino.digital_pins_value[13], 1)
        
        self.arduino.digitalWrite(13, 0)
        self.assertEqual(self.arduino.digital_pins_value[13], 0)
    
    def test_analog_io(self):
        """아날로그 I/O 테스트"""
        # analogRead 테스트 (노이즈 포함)
        for _ in range(10):
            value = self.arduino.analogRead(0)
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 4095)  # 12-bit ADC
        
        # analogWrite (PWM) 테스트
        self.arduino.analogWrite(9, 128)  # 50% duty cycle
        self.assertEqual(self.arduino.pwm_values[9], 128)
    
    def test_serial_communication(self):
        """Serial 통신 테스트"""
        self.arduino.Serial_begin(9600)
        self.assertEqual(self.arduino.serial_baud_rate, 9600)
        
        # Serial 출력 테스트
        self.arduino.Serial_println("Test message")
        self.assertIn("Test message\n", self.arduino.serial_output)
    
    def test_performance_counters(self):
        """성능 카운터 테스트"""
        # 초기 상태
        initial_stats = self.arduino.get_performance_stats()
        initial_instructions = initial_stats['instruction_count']
        
        # 몇 가지 함수 호출
        self.arduino.millis()
        self.arduino.random_range(0, 3)
        self.arduino.digitalWrite(13, 1)
        
        # 성능 카운터 증가 확인
        final_stats = self.arduino.get_performance_stats()
        self.assertGreater(final_stats['instruction_count'], initial_instructions)
        self.assertGreater(len(final_stats['function_calls']), 0)


class TestRandomGeneratorSimulation(unittest.TestCase):
    """Random Number Generator 시뮬레이션 테스트"""
    
    def setUp(self):
        """테스트 설정"""
        self.arduino, self.simulator = create_simulation(seed=12345)
    
    def test_lookup_table_logic(self):
        """룩업 테이블 로직 테스트"""
        # 룩업 테이블 검증
        expected_table = [
            [1, 1, 2],  # 이전이 0일 때
            [0, 0, 2],  # 이전이 1일 때
            [0, 1, 0]   # 이전이 2일 때
        ]
        
        self.assertEqual(self.simulator.lookup_table, expected_table)
    
    def test_constraint_satisfaction(self):
        """제약 조건 만족 테스트"""
        # 100개 숫자 생성
        generated_numbers = []
        for _ in range(100):
            num = self.simulator.generate_random_number()
            generated_numbers.append(num)
        
        # 연속된 동일한 숫자가 없는지 확인
        consecutive_violations = 0
        for i in range(1, len(generated_numbers)):
            if generated_numbers[i] == generated_numbers[i-1]:
                consecutive_violations += 1
        
        self.assertEqual(consecutive_violations, 0, 
                        "Consecutive identical numbers found!")
    
    def test_number_range(self):
        """숫자 범위 테스트"""
        # 1000개 숫자 생성
        for _ in range(1000):
            num = self.simulator.generate_random_number()
            self.assertIn(num, [0, 1, 2], f"Invalid number generated: {num}")
    
    def test_distribution_fairness(self):
        """분포 공정성 테스트 (통계적)"""
        # 대량 생성 (10,000개)
        generated_numbers = []
        for _ in range(10000):
            num = self.simulator.generate_random_number()
            generated_numbers.append(num)
        
        # 각 숫자의 빈도 계산
        counts = {0: 0, 1: 0, 2: 0}
        for num in generated_numbers:
            counts[num] += 1
        
        # 각 숫자가 최소 20% 이상 나와야 함 (너무 편향되지 않음)
        total = len(generated_numbers)
        for num in [0, 1, 2]:
            percentage = (counts[num] / total) * 100
            self.assertGreaterEqual(percentage, 20.0, 
                                  f"Number {num} appears too rarely: {percentage:.1f}%")
            self.assertLessEqual(percentage, 50.0, 
                               f"Number {num} appears too frequently: {percentage:.1f}%")
    
    def test_transition_completeness(self):
        """전이 완전성 테스트"""
        # 충분한 수의 숫자 생성
        generated_numbers = []
        for _ in range(5000):
            num = self.simulator.generate_random_number()
            generated_numbers.append(num)
        
        # 전이 행렬 계산
        transitions = set()
        for i in range(1, len(generated_numbers)):
            prev_num = generated_numbers[i-1]
            curr_num = generated_numbers[i]
            transitions.add(f"{prev_num}->{curr_num}")
        
        # 가능한 모든 전이가 발생했는지 확인 (대각선 제외)
        expected_transitions = {
            "0->1", "0->2", "1->0", "1->2", "2->0", "2->1"
        }
        
        self.assertTrue(expected_transitions.issubset(transitions),
                       f"Missing transitions: {expected_transitions - transitions}")
    
    def test_arduino_setup_simulation(self):
        """Arduino setup 시뮬레이션 테스트"""
        # setup 실행
        self.simulator.simulate_arduino_setup()
        
        # Serial이 초기화되었는지 확인
        self.assertEqual(self.arduino.serial_baud_rate, 9600)
        self.assertGreater(len(self.arduino.serial_output), 0)
    
    def test_arduino_loop_simulation(self):
        """Arduino loop 시뮬레이션 테스트"""
        # loop 실행 (20회)
        generated_numbers = self.simulator.simulate_arduino_loop(20)
        
        # 정확한 개수 생성 확인
        self.assertEqual(len(generated_numbers), 20)
        
        # 모든 숫자가 유효한 범위인지 확인
        for num in generated_numbers:
            self.assertIn(num, [0, 1, 2])


class TestSimulationRunner(unittest.TestCase):
    """Simulation Runner 테스트"""
    
    def test_single_simulation(self):
        """단일 시뮬레이션 테스트"""
        config = SimulationConfig(
            iterations=1000,
            seed=12345,
            show_progress=False,
            save_results=False
        )
        
        runner = SimulationRunner(config)
        results = runner.run_single_simulation()
        
        # 결과 구조 검증
        self.assertIn('simulation_info', results)
        self.assertIn('distribution_analysis', results)
        self.assertIn('constraint_verification', results)
        self.assertIn('performance_metrics', results)
        
        # 기본 값 검증
        self.assertEqual(results['simulation_info']['total_iterations'], 1000)
        self.assertTrue(results['constraint_verification']['constraint_satisfied'])
    
    def test_multiple_simulations(self):
        """다중 시뮬레이션 테스트"""
        config = SimulationConfig(
            iterations=500,
            show_progress=False,
            save_results=False
        )
        
        runner = SimulationRunner(config)
        seeds = [11111, 22222, 33333]
        results = runner.run_multiple_simulations(seeds)
        
        # 결과 개수 확인
        self.assertEqual(len(results), len(seeds))
        
        # 각 결과의 시드 확인
        for i, result in enumerate(results):
            self.assertEqual(result['seed_used'], seeds[i])


class TestPerformanceBenchmark(unittest.TestCase):
    """성능 벤치마크 테스트"""
    
    def test_generation_speed(self):
        """생성 속도 테스트"""
        arduino, simulator = create_simulation(seed=12345)
        
        # 1000개 생성 시간 측정
        start_time = time.time()
        for _ in range(1000):
            simulator.generate_random_number()
        end_time = time.time()
        
        total_time = end_time - start_time
        generation_rate = 1000 / total_time
        
        # 최소 성능 기준 (1000 gen/sec 이상)
        self.assertGreater(generation_rate, 1000, 
                          f"Generation rate too slow: {generation_rate:.0f} gen/sec")
        
        print(f"Generation rate: {generation_rate:,.0f} gen/sec")
    
    def test_memory_usage(self):
        """메모리 사용량 테스트"""
        arduino, simulator = create_simulation(seed=12345)
        
        # 초기 메모리 사용량
        initial_stats = arduino.get_performance_stats()
        initial_sram = initial_stats['sram_usage_percent']
        
        # 대량 생성
        for _ in range(5000):
            simulator.generate_random_number()
        
        # 최종 메모리 사용량
        final_stats = arduino.get_performance_stats()
        final_sram = final_stats['sram_usage_percent']
        
        # SRAM 사용량이 50%를 넘지 않아야 함
        self.assertLess(final_sram, 50.0, 
                       f"SRAM usage too high: {final_sram:.2f}%")
        
        print(f"SRAM usage: {final_sram:.2f}%")


# ==================== 테스트 실행 ====================

def run_all_tests():
    """모든 테스트 실행"""
    print("Arduino Uno R4 WiFi Simulation Test Suite")
    print("=" * 60)
    
    # 테스트 스위트 생성
    test_suite = unittest.TestSuite()
    
    # 테스트 클래스 추가
    test_classes = [
        TestArduinoMock,
        TestRandomGeneratorSimulation,
        TestSimulationRunner,
        TestPerformanceBenchmark
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)