/**
 * Random Number Generator - JavaScript Implementation
 * 
 * 조건:
 * - 3개의 숫자(0, 1, 2)를 랜덤으로 추출
 * - 이전 숫자와 동일하지 않도록 추출
 * - 반복문(for, while) 사용 불가
 * - 논리연산자(||, &&) 사용 불가
 */

class RandomNumberGenerator {
    constructor() {
        this.previousNumber = null;
        this.stats = {
            totalCount: 0,
            startTime: performance.now(),
            numberFrequency: { 0: 0, 1: 0, 2: 0 },
            transitionMatrix: {}
        };
        
        // 룩업 테이블: [이전숫자][후보숫자] = 결과숫자
        this.lookupTable = {
            0: { 0: 1, 1: 1, 2: 2 },  // 이전이 0일 때
            1: { 0: 0, 1: 0, 2: 2 },  // 이전이 1일 때
            2: { 0: 0, 1: 1, 2: 0 }   // 이전이 2일 때
        };
    }
    
    /**
     * 조건을 만족하는 랜덤 숫자 생성
     * 반복문과 논리연산자 사용 불가
     */
    generateNumber() {
        const candidate = Math.floor(Math.random() * 3);  // 0, 1, 2 중 랜덤 선택
        
        let result;
        // 이전 숫자가 없으면 바로 반환 (삼항 연산자 사용)
        result = (this.previousNumber === null) ? candidate : this.lookupTable[this.previousNumber][candidate];
        
        this._updateStats(result);
        this.previousNumber = result;
        
        return result;
    }
    
    /**
     * 통계 정보 업데이트
     */
    _updateStats(number) {
        this.stats.totalCount++;
        this.stats.numberFrequency[number]++;
        
        // 전이 행렬 업데이트 (이전 -> 현재)
        if (this.previousNumber !== null) {
            const transition = `${this.previousNumber}->${number}`;
            this.stats.transitionMatrix[transition] = (this.stats.transitionMatrix[transition] || 0) + 1;
        }
    }
    
    /**
     * 성능 및 분포 통계 반환
     */
    getStatistics() {
        const elapsedTime = (performance.now() - this.stats.startTime) / 1000; // 초 단위
        
        // 빈도 분석
        const frequencyAnalysis = {};
        [0, 1, 2].forEach(num => {
            const count = this.stats.numberFrequency[num];
            frequencyAnalysis[num] = {
                count: count,
                percentage: this.stats.totalCount > 0 ? (count / this.stats.totalCount) * 100 : 0
            };
        });
        
        return {
            totalGenerated: this.stats.totalCount,
            elapsedTimeSeconds: elapsedTime,
            generationRate: elapsedTime > 0 ? this.stats.totalCount / elapsedTime : 0,
            averageTimePerGeneration: this.stats.totalCount > 0 ? elapsedTime / this.stats.totalCount : 0,
            frequencyAnalysis: frequencyAnalysis,
            transitionAnalysis: this.stats.transitionMatrix,
            currentNumber: this.previousNumber
        };
    }
    
    /**
     * 생성기 상태 초기화
     */
    reset() {
        this.previousNumber = null;
        this.stats = {
            totalCount: 0,
            startTime: performance.now(),
            numberFrequency: { 0: 0, 1: 0, 2: 0 },
            transitionMatrix: {}
        };
    }
}

/**
 * 생성기 데모 함수 (재귀 사용으로 반복문 대체)
 */
function demonstrateGenerator(count = 20) {
    console.log("Random Number Generator - JavaScript Implementation");
    console.log("Numbers: 0, 1, 2");
    console.log("Constraint: No consecutive identical numbers");
    console.log("-".repeat(50));
    
    const generator = new RandomNumberGenerator();
    const generatedNumbers = [];
    
    // 재귀 함수를 사용해서 반복문 없이 구현
    function generateRecursive(remaining) {
        if (remaining <= 0) {
            return;
        }
        
        const number = generator.generateNumber();
        generatedNumbers.push(number);
        
        const prevDisplay = generatedNumbers.length > 1 ? 
            generatedNumbers[generatedNumbers.length - 2] : 'none';
        console.log(`Generated: ${number} (Previous: ${prevDisplay})`);
        
        // 재귀 호출로 반복문 대체
        generateRecursive(remaining - 1);
    }
    
    generateRecursive(count);
    
    // 통계 출력
    const stats = generator.getStatistics();
    console.log("\n" + "=".repeat(50));
    console.log("PERFORMANCE STATISTICS");
    console.log("=".repeat(50));
    console.log(`Total generated: ${stats.totalGenerated}`);
    console.log(`Elapsed time: ${stats.elapsedTimeSeconds.toFixed(6)} seconds`);
    console.log(`Generation rate: ${stats.generationRate.toFixed(2)} numbers/second`);
    console.log(`Average time per generation: ${(stats.averageTimePerGeneration * 1000).toFixed(3)} milliseconds`);
    
    console.log("\nFREQUENCY ANALYSIS:");
    Object.entries(stats.frequencyAnalysis).forEach(([num, data]) => {
        console.log(`  Number ${num}: ${data.count} times (${data.percentage.toFixed(1)}%)`);
    });
    
    console.log("\nTRANSITION ANALYSIS:");
    Object.entries(stats.transitionAnalysis).forEach(([transition, count]) => {
        console.log(`  ${transition}: ${count} times`);
    });
    
    console.log(`\nGenerated sequence: [${generatedNumbers.join(', ')}]`);
}

/**
 * 성능 벤치마크 클래스
 */
class PerformanceBenchmark {
    static runBenchmark(iterations = 10000) {
        const generator = new RandomNumberGenerator();
        
        const startTime = performance.now();
        
        // 재귀로 벤치마크 실행
        function benchmarkRecursive(remaining) {
            if (remaining <= 0) {
                return;
            }
            generator.generateNumber();
            benchmarkRecursive(remaining - 1);
        }
        
        benchmarkRecursive(iterations);
        
        const endTime = performance.now();
        const totalTime = (endTime - startTime) / 1000; // 초 단위
        
        return {
            iterations: iterations,
            totalTime: totalTime,
            timePerIteration: totalTime / iterations,
            iterationsPerSecond: iterations / totalTime
        };
    }
}

// Node.js 환경에서 실행
if (typeof require !== 'undefined' && require.main === module) {
    // 데모 실행
    demonstrateGenerator(20);
    
    // 성능 벤치마크
    console.log("\n" + "=".repeat(50));
    console.log("PERFORMANCE BENCHMARK");
    console.log("=".repeat(50));
    
    const benchmarkResults = PerformanceBenchmark.runBenchmark(10000);
    console.log(`Iterations: ${benchmarkResults.iterations.toLocaleString()}`);
    console.log(`Total time: ${benchmarkResults.totalTime.toFixed(6)} seconds`);
    console.log(`Time per iteration: ${(benchmarkResults.timePerIteration * 1000000).toFixed(2)} microseconds`);
    console.log(`Iterations per second: ${Math.round(benchmarkResults.iterationsPerSecond).toLocaleString()}`);
}

// 브라우저 및 Node.js 모두에서 사용 가능하도록 내보내기
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { RandomNumberGenerator, PerformanceBenchmark, demonstrateGenerator };
}