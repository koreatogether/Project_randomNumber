"""
Arduino Uno R4 WiFi Random Number Generator Simulation
메인 실행 파일

사용법:
1. 빠른 테스트: python src/main.py --quick
2. 대시보드 실행: python src/main.py --dashboard
3. 벤치마크 실행: python src/main.py --benchmark
4. 테스트 실행: python src/main.py --test
"""

import argparse
import sys
import os
from pathlib import Path

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(str(Path(__file__).parent))

from arduino_simulation import (
    create_simulation, 
    SimulationRunner, 
    SimulationConfig,
    run_dashboard
)


def run_quick_test():
    """빠른 테스트 실행"""
    print("Arduino Uno R4 WiFi - Quick Test")
    print("=" * 50)
    
    # 시뮬레이션 생성
    arduino, simulator = create_simulation(seed=12345)
    
    # Arduino setup 시뮬레이션
    simulator.simulate_arduino_setup()
    
    # 20개 숫자 생성
    print("\nGenerating 20 random numbers...")
    generated_numbers = simulator.simulate_arduino_loop(20)
    
    # 간단한 분석
    print(f"\nGenerated sequence: {generated_numbers}")
    
    # 분포 분석
    counts = {0: 0, 1: 0, 2: 0}
    for num in generated_numbers:
        counts[num] += 1
    
    print(f"Distribution: {counts}")
    
    # 제약 조건 검증
    violations = 0
    for i in range(1, len(generated_numbers)):
        if generated_numbers[i] == generated_numbers[i-1]:
            violations += 1
    
    print(f"Constraint violations: {violations}")
    print(f"Constraint satisfied: {'✅' if violations == 0 else '❌'}")
    
    # 성능 통계
    stats = arduino.get_performance_stats()
    print(f"\nPerformance Stats:")
    print(f"- Instructions executed: {stats['instruction_count']:,}")
    print(f"- Function calls: {sum(stats['function_calls'].values())}")
    print(f"- SRAM usage: {stats['sram_usage_percent']:.2f}%")


def run_benchmark():
    """벤치마크 실행"""
    print("Arduino Uno R4 WiFi - Benchmark Test")
    print("=" * 50)
    
    # 벤치마크 설정
    iterations = 10000
    test_seeds = [12345, 54321, 98765, 11111, 99999]
    
    print(f"Running benchmark with {len(test_seeds)} seeds")
    print(f"Iterations per seed: {iterations:,}")
    print(f"Total iterations: {len(test_seeds) * iterations:,}")
    
    # 시뮬레이션 실행
    config = SimulationConfig(
        iterations=iterations,
        show_progress=True,
        save_results=True
    )
    
    runner = SimulationRunner(config)
    results = runner.run_multiple_simulations(test_seeds)
    
    # 결과 요약
    print(f"\n{'='*50}")
    print("BENCHMARK RESULTS")
    print(f"{'='*50}")
    
    total_time = sum(r['simulation_info']['total_time_seconds'] for r in results)
    total_iterations = sum(r['simulation_info']['total_iterations'] for r in results)
    avg_rate = total_iterations / total_time if total_time > 0 else 0
    
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Total iterations: {total_iterations:,}")
    print(f"Average rate: {avg_rate:,.0f} gen/sec")
    
    # 각 시드별 결과
    print(f"\nPer-seed results:")
    for i, result in enumerate(results):
        seed = result['seed_used']
        rate = result['simulation_info']['generation_rate_per_second']
        violations = result['constraint_verification']['consecutive_violations']
        print(f"  Seed {seed}: {rate:,.0f} gen/sec, violations: {violations}")
    
    # 분포 일관성 분석
    print(f"\nDistribution consistency:")
    for num in [0, 1, 2]:
        percentages = [r['distribution_analysis']['percentages'][num] for r in results]
        avg_pct = sum(percentages) / len(percentages)
        min_pct = min(percentages)
        max_pct = max(percentages)
        print(f"  Number {num}: {avg_pct:.1f}% (range: {min_pct:.1f}% - {max_pct:.1f}%)")


def run_tests():
    """테스트 실행"""
    print("Arduino Uno R4 WiFi - Test Suite")
    print("=" * 50)
    
    try:
        from tests.test_simulation import run_all_tests
        success = run_all_tests()
        return success
    except ImportError as e:
        print(f"Error importing test module: {e}")
        print("Make sure you're running from the project root directory")
        return False


def run_dashboard_server():
    """대시보드 서버 실행"""
    print("Arduino Uno R4 WiFi - Dashboard Server")
    print("=" * 50)
    print("Starting dashboard server...")
    print("Open your browser and go to: http://localhost:8050")
    print("Press Ctrl+C to stop the server")
    
    try:
        run_dashboard(port=8050, debug=True)
    except KeyboardInterrupt:
        print("\nDashboard server stopped")
    except Exception as e:
        print(f"Error running dashboard: {e}")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="Arduino Uno R4 WiFi Random Number Generator Simulation"
    )
    
    parser.add_argument(
        "--quick", 
        action="store_true",
        help="Run quick test (20 generations)"
    )
    
    parser.add_argument(
        "--benchmark",
        action="store_true", 
        help="Run performance benchmark"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run test suite"
    )
    
    parser.add_argument(
        "--dashboard",
        action="store_true",
        help="Start dashboard server"
    )
    
    parser.add_argument(
        "--iterations",
        type=int,
        default=10000,
        help="Number of iterations for benchmark (default: 10000)"
    )
    
    args = parser.parse_args()
    
    # 결과 디렉토리 생성
    Path("src/results").mkdir(exist_ok=True)
    
    if args.quick:
        run_quick_test()
    elif args.benchmark:
        run_benchmark()
    elif args.test:
        success = run_tests()
        sys.exit(0 if success else 1)
    elif args.dashboard:
        run_dashboard_server()
    else:
        # 기본 동작: 대화형 메뉴
        print("Arduino Uno R4 WiFi Random Number Generator Simulation")
        print("=" * 60)
        print("Select an option:")
        print("1. Quick Test (20 generations)")
        print("2. Performance Benchmark")
        print("3. Run Test Suite")
        print("4. Start Dashboard Server")
        print("5. Exit")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == "1":
                    run_quick_test()
                    break
                elif choice == "2":
                    run_benchmark()
                    break
                elif choice == "3":
                    success = run_tests()
                    sys.exit(0 if success else 1)
                elif choice == "4":
                    run_dashboard_server()
                    break
                elif choice == "5":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter 1-5.")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()