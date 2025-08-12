/**
 * Random Number Generator - Arduino Implementation
 *
 * 조건:
 * - 3개의 숫자(0, 1, 2)를 랜덤으로 추출
 * - 이전 숫자와 동일하지 않도록 추출
 * - 반복문(for, while) 사용 불가
 * - 논리연산자(||, &&) 사용 불가
 */

// 1. 재귀 함수 사용
int prevNum1 = -1;
int getRandomNum1()
{
    int num = random(0, 3);
    if (num == prevNum1)
    {
        return getRandomNum1();
    }
    prevNum1 = num;
    return num;
}

// 2. 배열과 조건문만 사용
int prevNum2 = -1;
int getRandomNum2()
{
    int nums[3] = {0, 1, 2};
    int idx = random(0, 3);
    int num = nums[idx];
    if (num == prevNum2)
    {
        idx = (idx + 1) % 3;
        num = nums[idx];
    }
    prevNum2 = num;
    return num;
}

// 3. switch문 활용
int prevNum3 = -1;
int getRandomNum3()
{
    int num = random(0, 3);
    switch (num)
    {
    case 0:
        if (prevNum3 == 0)
            num = 1;
        break;
    case 1:
        if (prevNum3 == 1)
            num = 2;
        break;
    case 2:
        if (prevNum3 == 2)
            num = 0;
        break;
    }
    prevNum3 = num;
    return num;
}

// 4. 함수 포인터 활용
int prevNum4 = -1;
int getNum0() { return prevNum4 == 0 ? 1 : 0; }
int getNum1() { return prevNum4 == 1 ? 2 : 1; }
int getNum2() { return prevNum4 == 2 ? 0 : 2; }
int (*getNumFuncs[3])() = {getNum0, getNum1, getNum2};
int getRandomNum4()
{
    int idx = random(0, 3);
    int num = getNumFuncs[idx]();
    prevNum4 = num;
    return num;
}

// 5. 삼항 연산자와 수식 활용
int prevNum5 = -1;
int getRandomNum5()
{
    int num = random(0, 3);
    num = (num == prevNum5) ? ((num + 1) % 3) : num;
    prevNum5 = num;
    return num;
}

// 6. 중첩 함수(람다) 활용 (C++11 이상 지원)
int prevNum6 = -1;
int getRandomNum6()
{
    auto pick = [](int prev)
    {
        int n = random(0, 3);
        if (n == prev)
            n = (n + 2) % 3;
        return n;
    };
    int num = pick(prevNum6);
    prevNum6 = num;
    return num;
}

// 7. static 변수 활용
int getRandomNum7()
{
    static int prevNum7 = -1;
    int num = random(0, 3);
    if (num == prevNum7)
        num = (num + 2) % 3;
    prevNum7 = num;
    return num;
}

// 8. 조건문과 비트 연산 활용
int prevNum8 = -1;
int getRandomNum8()
{
    int num = random(0, 3);
    if ((num ^ prevNum8) == 0)
        num = (num + 1) % 3;
    prevNum8 = num;
    return num;
}

void setup()
{
    Serial.begin(9600);
    randomSeed(analogRead(0));
    Serial.println("--- 재귀 함수 사용 ---");
    Serial.println(getRandomNum1());
    Serial.println(getRandomNum1());
    Serial.println(getRandomNum1());
    Serial.println("--- 배열과 조건문만 사용 ---");
    Serial.println(getRandomNum2());
    Serial.println(getRandomNum2());
    Serial.println(getRandomNum2());
    Serial.println("--- switch문 활용 ---");
    Serial.println(getRandomNum3());
    Serial.println(getRandomNum3());
    Serial.println(getRandomNum3());
    Serial.println("--- 함수 포인터 활용 ---");
    Serial.println(getRandomNum4());
    Serial.println(getRandomNum4());
    Serial.println(getRandomNum4());
    Serial.println("--- 삼항 연산자와 수식 활용 ---");
    Serial.println(getRandomNum5());
    Serial.println(getRandomNum5());
    Serial.println(getRandomNum5());
    Serial.println("--- 중첩 함수(람다) 활용 ---");
    Serial.println(getRandomNum6());
    Serial.println(getRandomNum6());
    Serial.println(getRandomNum6());
    Serial.println("--- static 변수 활용 ---");
    Serial.println(getRandomNum7());
    Serial.println(getRandomNum7());
    Serial.println(getRandomNum7());
    Serial.println("--- 조건문과 비트 연산 활용 ---");
    Serial.println(getRandomNum8());
    Serial.println(getRandomNum8());
    Serial.println(getRandomNum8());
}

void loop()
{
    // ...existing code...
}
#include <Arduino.h>

// 코드 1

// 코드 2

// 코드 3

// 코드 4
