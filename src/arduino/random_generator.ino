/**
 * Random Number Generator - Arduino Implementation
 * 
 * 조건:
 * - 3개의 숫자(0, 1, 2)를 랜덤으로 추출
 * - 이전 숫자와 동일하지 않도록 추출
 * - 반복문(for, while) 사용 불가
 * - 논리연산자(||, &&) 사용 불가
 */

#include <Arduino.h>

// 전역 변수
int previousNumber = -1;  // 이전 숫자 저장 (-1은 초기값)
unsigned long generationCount = 0;  // 생성된 숫자 개수
unsigned long startTime = 0;  // 성능 측정용

// 함수 선언
int generateRandomNumber();
int getNextValidNumber(int candidate);
void printResult(int number);
void printStatistics();

void setup() {
    Serial.begin(115200);
    randomSeed(analogRead(0));  // 아날로그 핀의 노이즈를 시드로 사용
    
    Serial.println(F("Random Number Generator - Arduino"));
    Serial.println(F("Numbers: 0, 1, 2"));
    Serial.println(F("Constraint: No consecutive identical numbers"));
    Serial.println(F("Press any key to generate numbers..."));
    Serial.println();
    
    startTime = micros();
}

void loop() {
    // 시리얼 입력이 있거나 자동으로 생성
    static unsigned long lastGeneration = 0;
    unsigned long currentTime = millis();
    
    // 자동 생성 모드: 1초마다 숫자 생성
    if (currentTime - lastGeneration >= 1000) {
        int number = generateRandomNumber();
        printResult(number);
        lastGeneration = currentTime;
        
        // 100개 생성 후 통계 출력
        if (generationCount % 100 == 0) {
            printStatistics();
        }
    }
    
    // 시리얼 입력 처리
    if (Serial.available() > 0) {
        Serial.read();  // 입력 버퍼 클리어
        int number = generateRandomNumber();
        printResult(number);
    }
}

/**
 * 조건을 만족하는 랜덤 숫자 생성
 * 반복문과 논리연산자 사용 불가
 */
int generateRandomNumber() {
    int candidate = random(0, 3);  // 0, 1, 2 중 랜덤 선택
    
    // 이전 숫자와 같으면 다른 숫자로 변경
    candidate = getNextValidNumber(candidate);
    
    previousNumber = candidate;
    generationCount++;
    
    return candidate;
}

/**
 * 이전 숫자와 다른 유효한 숫자 반환
 * 논리연산자 사용 없이 구현
 */
int getNextValidNumber(int candidate) {
    // 경우의 수 테이블 사용 (lookup table 방식)
    // candidate와 previousNumber 조합에 따른 결과 매핑
    
    // previousNumber가 -1(초기값)인 경우
    if (previousNumber == -1) {
        return candidate;
    }
    
    // 3x3 매핑 테이블
    // [previousNumber][candidate] = result
    int lookupTable[3][3] = {
        // prev=0: cand=0->1, cand=1->1, cand=2->2
        {1, 1, 2},
        // prev=1: cand=0->0, cand=1->0, cand=2->2  
        {0, 0, 2},
        // prev=2: cand=0->0, cand=1->1, cand=2->0
        {0, 1, 0}
    };
    
    return lookupTable[previousNumber][candidate];
}

/**
 * 결과 출력
 */
void printResult(int number) {
    Serial.print(F("Generated: "));
    Serial.print(number);
    Serial.print(F(" (Previous: "));
    Serial.print(previousNumber == number ? "none" : String(previousNumber == -1 ? "none" : String(previousNumber)));
    Serial.print(F(", Count: "));
    Serial.print(generationCount);
    Serial.println(F(")"));
}

/**
 * 성능 통계 출력
 */
void printStatistics() {
    unsigned long currentTime = micros();
    unsigned long elapsedTime = currentTime - startTime;
    
    Serial.println(F("\n=== Performance Statistics ==="));
    Serial.print(F("Total generated: "));
    Serial.println(generationCount);
    Serial.print(F("Elapsed time: "));
    Serial.print(elapsedTime / 1000.0, 3);
    Serial.println(F(" ms"));
    Serial.print(F("Average time per generation: "));
    Serial.print((elapsedTime / (float)generationCount), 3);
    Serial.println(F(" microseconds"));
    Serial.print(F("Free memory: "));
    Serial.print(getFreeMemory());
    Serial.println(F(" bytes"));
    Serial.println(F("===============================\n"));
}

/**
 * 사용 가능한 메모리 계산
 */
int getFreeMemory() {
    extern int __heap_start, *__brkval;
    int v;
    return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
}