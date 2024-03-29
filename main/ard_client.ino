'''
Arduino Client : 아두이노 기기제어
작성일 : 2024.03.30
작성자 : 전자파(대한상공회의소 팀프로젝트)
'''
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Servo.h> // 서보모터 라이브러리 추가

#define DEBUG
#define IRSENSOR1_PIN 2 // 적외선 센서 핀
#define IRSENSOR2_PIN 3
#define IRSENSOR3_PIN 4
#define IRSENSOR4_PIN 5

#define MOTOR1_PIN 7
#define MOTOR2_PIN 8
#define MOTOR3_PIN 9
#define LED_BUILTIN_PIN 13

#define ARR_CNT 5
#define CMD_SIZE 60

char lcdLine1[17] = "Smart IoT By KSH";
char lcdLine2[17] = "";
char sendBuf[CMD_SIZE];
char recvId[10] = "KSH_SQL"; // SQL 저장 클라이언트 ID

bool timerIsrFlag = false;
unsigned int secCount;
SoftwareSerial BTSerial(10, 11); // RX ==>BT:TXD, TX ==> BT:RXD

int previousIrValue1 = 0;
int currentIrValue1 = 0;
int previousIrValue2 = 0;
int currentIrValue2 = 0;
int previousIrValue3 = 0;
int currentIrValue3 = 0;
int previousIrValue4 = 0;
int currentIrValue4 = 0;

int doorstate = 0;


Servo myServo1; // 서보모터 객체 생성

void setup() {
#ifdef DEBUG
  Serial.begin(115200);
  Serial.println("setup() start!");
#endif

  pinMode(LED_BUILTIN_PIN, OUTPUT); // LED_BUILTIN 핀을 출력으로 설정

  pinMode(IRSENSOR1_PIN, INPUT);
  pinMode(IRSENSOR2_PIN, INPUT);
  pinMode(IRSENSOR3_PIN, INPUT);
  pinMode(IRSENSOR4_PIN, INPUT);

  pinMode(MOTOR1_PIN, OUTPUT);
  pinMode(MOTOR2_PIN, OUTPUT);
  pinMode(MOTOR3_PIN, OUTPUT);

  digitalWrite(LED_BUILTIN_PIN, LOW);
  digitalWrite(MOTOR1_PIN, LOW);
  digitalWrite(MOTOR2_PIN, LOW);
  digitalWrite(MOTOR3_PIN, LOW);

  BTSerial.begin(9600); // 블루투스 시리얼 통신 설정

  myServo1.attach(12); // 서보모터 핀 설정
}

void loop() {
  if (BTSerial.available())
    bluetoothEvent();

  previousIrValue1 = currentIrValue1;
  previousIrValue2 = currentIrValue2;
  previousIrValue3 = currentIrValue3;
  previousIrValue4 = currentIrValue4;

  // 적외선센서 값을 읽음
  currentIrValue1 = digitalRead(IRSENSOR1_PIN);
  currentIrValue2 = digitalRead(IRSENSOR2_PIN);
  currentIrValue3 = digitalRead(IRSENSOR3_PIN);
  currentIrValue4 = digitalRead(IRSENSOR4_PIN);

  if (timerIsrFlag) {
    timerIsrFlag = false;

    // 각 적외선 센서와 해당 모터를 세트로 연결하여 물체가 감지되면 해당 모터를 멈추도록 설정
    if (digitalRead(IRSENSOR1_PIN) == LOW) {
      digitalWrite(MOTOR1_PIN, LOW);
    } else {
      digitalWrite(MOTOR1_PIN, HIGH);
    }

    if (digitalRead(IRSENSOR2_PIN) == LOW) {
      digitalWrite(MOTOR2_PIN, LOW);
    } else {
      digitalWrite(MOTOR2_PIN, HIGH);
    }

    if (digitalRead(IRSENSOR3_PIN) == LOW) {
      digitalWrite(MOTOR3_PIN, LOW);
    } else {
      digitalWrite(MOTOR3_PIN, HIGH);
    }

    if (digitalRead(IRSENSOR4_PIN) == HIGH) {
      digitalWrite(12, LOW);
    } else {
      digitalWrite(12, HIGH);
    }
  }

  // 적외선 센서의 상태 변화를 감지하여 모터를 멈추는 코드 추가
  if (previousIrValue1 == LOW && currentIrValue1 == HIGH) {
    digitalWrite(MOTOR1_PIN, LOW);
  }

  if (previousIrValue2 == LOW && currentIrValue2 == HIGH) {
    digitalWrite(MOTOR2_PIN, LOW);
  }

  if (previousIrValue3 == LOW && currentIrValue3 == HIGH) {
    digitalWrite(MOTOR3_PIN, LOW);
  }

  if (doorstate == 1 && previousIrValue4 == HIGH && currentIrValue4 == LOW) {
     delay(7000); // 10초 딜레이
     doorstate = 1; // 문 닫힘
   }

  if (doorstate == 1 && previousIrValue4 == LOW && currentIrValue4 == HIGH) {
    delay(7000); // 5초 딜레이
    doorstate = 0; // 문 닫힘
    myServo1.write(0);
  }

#ifdef DEBUG
  if (Serial.available())
    BTSerial.write(Serial.read());
#endif
}

void bluetoothEvent() {
  int i = 0;
  char *pToken;
  char *pArray[ARR_CNT] = {0};
  char recvBuf[CMD_SIZE] = {0};
  int len = BTSerial.readBytesUntil('\n', recvBuf, sizeof(recvBuf) - 1);

#ifdef DEBUG
  Serial.print("Recv : ");
  Serial.println(recvBuf);
#endif

  pToken = strtok(recvBuf, "[@]");
  while (pToken != NULL) {
    pArray[i] = pToken;
    if (++i >= ARR_CNT)
      break;
    pToken = strtok(NULL, "[@]");
  }

  if ((strlen(pArray[1]) + strlen(pArray[2])) < 16) {
    //sprintf(lcdLine2, "%s %s", pArray[1], pArray[2]);
    // lcdDisplay(0, 1, lcdLine2);
  }
  if (!strcmp(pArray[1], "LED")) {
    if (!strcmp(pArray[2], "ON")) {
      digitalWrite(LED_BUILTIN_PIN, HIGH);
    } else if (!strcmp(pArray[2], "OFF")) {
      digitalWrite(LED_BUILTIN_PIN, LOW);
    }
    sprintf(sendBuf, "[%s]%s@%s\n", pArray[0], pArray[1], pArray[2]);
  } else if (!strncmp(pArray[1], " New", 4)) { // New Connected
    return;
  } else if (!strncmp(pArray[1], " Alr", 4)) { //Already logged
    return;
  } else if (!strcmp(pArray[1], "MOTOR1")) { // 모터1 제어 명령
    if (!strcmp(pArray[2], "ON")) {
      digitalWrite(MOTOR1_PIN, HIGH);
    } else if (!strcmp(pArray[2], "OFF")) {
      digitalWrite(MOTOR1_PIN, LOW);
    }
    sprintf(sendBuf, "[%s]%s@%s\n", pArray[0], pArray[1], pArray[2]);
  } else if (!strcmp(pArray[1], "MOTOR2")) { // 모터2 제어 명령
    if (!strcmp(pArray[2], "ON")) {
      digitalWrite(MOTOR2_PIN, HIGH);
    } else if (!strcmp(pArray[2], "OFF")) {
      digitalWrite(MOTOR2_PIN, LOW);
    }
    sprintf(sendBuf, "[%s]%s@%s\n", pArray[0], pArray[1], pArray[2]);
  } else if (!strcmp(pArray[1], "MOTOR3")) { // 모터3 제어 명령
    if (!strcmp(pArray[2], "ON")) {
      digitalWrite(MOTOR3_PIN, HIGH);
    } else if (!strcmp(pArray[2], "OFF")) {
      digitalWrite(MOTOR3_PIN, LOW);
    }
    sprintf(sendBuf, "[%s]%s@%s\n", pArray[0], pArray[1], pArray[2]);
  } else if (!strcmp(pArray[1], "SERVO")) { // 서보모터 제어 명령
    if (!strcmp(pArray[2], "ON")) {
      // 두 서보모터를 같은 각도로 회전
      doorstate = 1;
      myServo1.write(110); // 예: 110도 회전
    } else if (!strcmp(pArray[2], "OFF")) {
      // 두 서보모터를 원위치로 회전
      doorstate = 0;
      myServo1.write(0); // 원위치로 회전
    }
    sprintf(sendBuf, "[%s]%s@%s\n", pArray[0], pArray[1], pArray[2]);
  }

#ifdef DEBUG
  Serial.print("Send : ");
  Serial.print(sendBuf);
#endif
  BTSerial.write(sendBuf);
}
