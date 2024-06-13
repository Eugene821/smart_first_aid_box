### 2024.03.30 디바이스마트 공모전 출품작
##### Team_ 이유진, 권유진, 신혜원, 이수빈

> #### 개발 목표
> - 구급상자를 재설계하여 AI를 결합해 사용자에게 다양한 의료 지원을 제공하고 사람들의 건강과 안전을 효과적으로 보호하는 방안을 마련
> - 실시간 영상 처리 및 음성 인식 기술을 활용한 AI 구급상자 구현
> - 상처의 종류를 영상처리로 인식, 사용자의 음성 지시를 통한 모듈 제어


|구분||
|---|---|
|사용 언어|python, C++, C|
|사용 부품|Raspberry pi4 (server), Raspberry pi4 (client) - 음성인식, Jetson Nano (client) - 영상처리, Arduino UNO (client) - 기기 제어, XPT2046 Touch Screen Controller, Motor * 3, Servo Motor * 2, PLEOMAX 300K PIXELS Camera, USB SPEAKER, SF-555B MICROPHONE, Mouse, IR Sensor : HAM4311 * 4|
|사용 기술|OpenCV, Roboflow, Git, YOLOv8|

<hr/>

#### 주요 동작 및 특징

1) 상처 인식 AI 컴퓨터 비전 영상처리  AI 컴퓨터 비전 영상처리 기술을 활용해 실시간으로 상처를 인식하고, 그에 적합한 의료용품을 제공한다.

2) 음성 인식 및 대처 방법 출력
  음성 인식을 통해 사용자가 원하는 증상에 맞는 대처 방법과 구급상자가 제공할 수 있는 의료용품을 안내한다. 또한, 필요한 약품이나 소모품이 구급상자 내에 구비되어 있지 않을 경우에도 음성 인식 기술을 통해 치료 권장 사항을 제공받을 수 있다.
3) 컴퓨터 비전과 음성 인식 기술을 활용한 응급 처치 및 시간 단축
  컴퓨터 비전과 음성 인식 기술을 통해 필요한 구급약품을 신속히 제공함으로써, 약품을 찾는 데 소요 되는 시간을 줄이고, 응급 처치에 필요한 시간을 단축할 수 있다.
4) 특정 명령을 통한 약품함 개폐 시스템 
  사용자의 특정 명령으로 약품함을 개폐할 수 있게 함으로써, 아동의 손이 닿지 않도록 주의가 필요한 약품을 안전하게 보관할 수 있다.

<hr/>

#### 전체 개발 환경
||Server (Main)|Device|Application1|Application2|
|---|---|---|---|---|
|Board|Raspberry Pi 4 Model B|Arduino UNO|Jetson Nano|Raspberry Pi 4 Model B|
|Language|C|C++|Python|Python|
|OS|Raspbian GNU / Ubuntu 24.04|Windows 11|JetPack 4.6.0|Raspbian GNU / Ubuntu 24.04|
|Library|stdio.h, stdlib.h, unistd.h, string.h, arpa/inet.h, sys/types.h, sys/socket.h, netinet/in.h, pthread.h, sys/stat.h, fcntl.h, dirent.h, sys/time.h, time.h, errno.h|SoftwareSerial.h, Wire.h, Servo.h|cv2, tkinter, socket, threading, sys, time, re, yolov5|speech_recognition, socket, threading, sys, time, re, pygame|
|System|VSCode|Arduino IDE|Google Colab, VSCode|VSCode|

<hr/>

#### 회로도

|[Client] Jetson Nano 회로도|
|-|
|![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/0ae853e2-4564-4d7f-8a67-66d105ec60c4)|

|[Slave] Arduino 회로도|
|-|
|![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/b8fd4a7c-c6e6-4a1a-8b1b-c1ee8af0fec1)|

|[Client] Raspberry Pi 회로도|
|-|
|![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/5c5c64f4-039d-489a-9e03-00429c783cc4)|


<hr/>

#### 전체 시스템 구성
|![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/1a99cc5e-6179-4479-9f95-b264177b694f)|
|-|

<hr/>

#### 세부 시스템 구성
##### 1. Raspberry Pi (Server, Master)
|![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/b36c638e-d884-4294-a57a-0068f7fee8f4)|
|-|
|클라이언트 간의 데이터 송수신을 위해 서버 소켓을 생성한다. 클라이언트가 접속하기 전까지 대기 상태를 유지하다가 클라이언트로부터 연결 요청이 들어오면 서버는 연결을 수락한다. 이 부분에서 보안을 위해 idpasswd.txt 파일을 만들어 인증된 클라이언트만 접속할 수 있도록 하였다. 인증된 클라이언트는 메시지를 서버에 전송할 수 있으므로 클라이언트 간의 송수신을 통해 다양한 접속기기로 Arduino를 제어하도록 했다.|

##### 2. Jetson Nano (Client)
|![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/cf84c220-534b-4afb-a87d-d60c5b625e8e)|
|-|
|Jetson Nano는 머신 러닝을 이용해 객체를 감지하는 역할을 담당한다. 웹캠으로 객체를 인식하고 인식된 결과를 문자열로 값을 바꾸어 Raspberry Pi Server와의 소켓 통신을 통해 문자열 값을 Arduino에 송신한다. 송신된 결괏값을 받으면 Arduino 제어가 가능하게 했다.|

##### 3. Raspberry Pi (Client)
|![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/c5a17abb-a757-4bbd-926e-a09efdaf0641)|
|-|
|Raspberry Pi에 마이크와 스피커를 연결하여 핫 워드를 인식시키면 Raspberry Pi Server와의 소켓 통신을 통해 문자열 값을 Arduino에 송신한다. 송신된 결괏값을 받으면 Arduino 제어가 가능하게 했다.|

##### 4. Arduino (Slave)
|![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/ba4365b6-788f-4a65-97f5-5242497ae83d)|
|-|
|Raspberry Pi Server와의 소켓 통신을 통해 Arduino에 데이터를 송신하면 Arduino에 수신된 값에 따라 설정된 제어시스템이 활성화된다. 만약 수신된 정보가 문 열림을 필요로 한다면 시스템은 먼저 적외선 센서로 약품의 존재 여부를 감지한다. 감지 되는 경우 서보모터가 작동하여 문을 열고 약품을 꺼낸 후 다시 넣으면 센서가 이를 감지하고 7초 뒤에 문을 자동으로 닫는다. 만약 수신된 데이터가 레일 작업을 요구한다면, 해당 작업은 레일 모터 시스템으로 전달된다. 이때, 레일 모터는 특정 조합에 따라 작동하여 물체를 이동시킨다. 만약 레일이 작동하여 물체가 아래로 떨어져 적외선센서에 물체가 인식되지 않으면 레일이 정지하게 된다.|

<hr/>

#### 개발 과정 및 기능

##### 1. Raspberry Pi Server
  Raspberry Pi Server는 음성을 인식하는 Raspberry Pi 모듈과 영상을 인식하는 Jetson Nano 모듈로부터 클라이언트 연결을 받아들여 명령어를 수신하는 중추적 역할을 한다. 이와 동시에, Arduino와의 통신에서는 마스터-슬레이브 관계를 형성하여 스마트 구급상자의 모터 제어를 담당한다. Arduino는 블루투스를 통해 Raspberry Pi로부터 명령어를 수신한다.

##### 2. Ai modeling
  스마트 구급상자에 쓰인 ai 모델은 주변에서 흔히 볼 수 있는 상처를 인식하도록 생성했다. 모델은 Roboflow를 이용하여 약 7300장의 상처 이미지 데이터를 수집하고 라벨링을 시행했다. 모델 유형은 실시간 상처 인식을 위해 객체 감지 유형으로 선택했다. 구현한 모델은 베임, 화상, 벌레 물림 상처를 구분하여 인식한다. 본 프로젝트에서는 Ultralytics YOLOv8을 이용하여 모델링을 진행하였다. YOLOv8 모델은 빠르고 정확하고 사용하기 쉽다는 점에서 사용했다. 데이터 클래스는 bites, burns, cuts 세 개의 클래스로 구성했다. 데이터 셋 버전을 생성한 뒤 트레이닝을 위해 데이터 셋 형식을 다운 받아 코랩에서 학습 시켰다. 학습의 정확도를 높이기 위해 Epoch는 100으로 지정하고 batch 사이즈는 일반적으로 많이 사용하는 16으로 지정하였다.

![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/028c9f83-891e-4db5-82b8-f1f3339e3621)

Training Graphs를 보면 50에서 100 사이의 Loss 값이 안정되는 것을 볼 수 있다.

![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/e6a067cc-8046-42c0-80aa-1f5fbcf146c1)
![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/96c73f1c-253c-42c1-99f8-dd75b53bb57c)

 머신러닝은 batch=16의 크기만큼 데이터를 활용해 모델의 예측값과 실제 정답 간의 오차를 계산하여 파라미터를 업데이트한다. 학습 후 생성된 best.pt 파일로 모델을 생성했다.
 
##### 3. Jetson Nano 영상처리
  스마트 구급상자는 실시간 상처 인식 기능을 통해 상처에 적합한 약품을 자동으로 제공한다. 이를 위해 NVIDIA에서 개발한 Jetson Nano 단일 보드 AI 키트를 사용했다. 상처 인식 과정에서는 카메라와 마우스가 입력 장치로 사용된다. 카메라는 사용자의 상처를 실시간으로 캡처하여 LCD 화면을 통해 GUI와 함께 보여준다. 사용자는 마우스를 사용하여 LCD의 GUI 버튼을 조작할 수 있다.
  
![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/7bec9032-ac0b-4f7f-be06-f3f53411ba8d)

  상처 인식을 원할 때는 ‘Resume’ 버튼을 누르면 된다. 상처가 인식되고 '진단' 버튼을 누르면, GUI에는 해당 상처의 종류와 필요한 약품 정보가 표시된다. 예를 들어, 화상 상처의 경우 연고와 밴드를, 벌레 물린 상처에는 전용 약품을, 베인 상처에는 밴드를 제공하도록 설정하였다.
  진단 버튼을 누르면 Jetson Nano는 연결된 Raspberry Pi 서버로 모터 구동 명령어를 전송한다. 이 명령어는 Raspberry Pi를 통해 Arduino에 연결되며, Arduino는 명령에 따라 모터를 구동하여 적절한 약품을 스마트 구급상자에서 출력하도록 한다. 이 과정을 통해 사용자는 자신의 상처에 가장 적합한 치료를 신속하게 받을 수 있다.

![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/69042792-f8ce-4472-8bde-5e1e96ed77c3)
![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/41a2abfa-f40e-4482-b52d-c5ef831f3206)
![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/112f5dd0-371a-4d22-b30b-4b0c51eb4c23)

##### 4. Raspberry Pi 음성 인식 처리
  음성 인식용 Raspberry Pi 보드는 사용자의 증상에 따른 해결책과 약품 제공을 위해 음성 인식 기술을 활용한다. 사용자가 ‘아파’라는 핫워드를 통해 증상을 말하면, 모듈은 증상을 인식하고 해당 정보를 바탕으로 Arduino에 명령어를 전송한다. 이 명령에 따라, 스피커는 증상에 맞는 해결책을 포함한 음성 파일을 재생하며, 스마트 구급상자는 필요한 약품을 제공한다.
  
![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/fcdff09a-8f97-4afc-8e2c-66030b28b10b)

또한, 음성 인식 기능은 구글 API로 구현되어 있어 한국어가 아닌 해외 다른 외국어를 등록시켜 사용할 수 있어 언어의 장벽 또한 없앨 수 있다. 이를 통해 다양한 사용자가 손쉽고 빠르게 적절한 해결책과 약품을 얻을 수 있도록 했다.

##### 5. Arduino 모듈 제어
  영상처리 결과에 맞는 명령어를 Arduino 보드에서 블루투스 모듈로 받고, 이 명령어로 선택된 모터가 구동되고, IR 센서를 통해 감지된 물체의 상태 변화를 통해 모터 구동 제어를 하는 것을 Arduino 개발의 시나리오로 설정했다. 
  우선 블루투스 모듈을 통해 MOTOR1@ON, MOTOR2@ON, MOTOR3@ON, SERVO@ON 명령어를 받고, 그에 맞는 모터를 구동하는 기능을 bluetoothEvent 함수로 구현하였다. 레일과 연결된 서보형 DC모터는 디지털 출력을 HIGH로 설정해 위에 올려진 물건을 나오는 방향으로 옮기도록 하였고, 여닫이문에 연결된 일반 서보모터는 110°만큼 회전해 문이 열리도록 설정했다.

![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/a21804f2-af78-4fd3-8f18-e876f0ac9649)
![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/29e373cd-6595-47c4-aabe-d4739fcc14da)

  이후의 모터 구동은 레일과 여닫이문 두 가지 경우로 나누어 IR 센서의 출력값을 통해 제어한다. 레일의 이동 방향 끝에 달린 IR 센서의 출력값이 0->1->0으로 변하면 서보형 DC모터가 구동을 멈춘다. 레일 위에는 여러 개의 약품이 간격을 둔 상태로 올려져 있으며, 한 개의 약품만을 떨어뜨릴 것이다. 이를 위해 약품이 감지되기 전(0, 약품이 아직 센서에 닿지 않음) -> 감지 된 상태(1, 약품이 센서를 지나 밖으로 떨어지는 중) -> 다시 감지되지 않음(0, 약품 떨어지고 그다음 약품은 일정 간격 뒤에 위치하는 상태)으로 시나리오를 설정했다. 
  선택된 레일의 모터가 구동되면 IR 센서값이 0->1로 변하므로, 물체가 통과하는 과정(값이 1인 순간)엔 계속 모터가 돌고, 값이 0인 순간엔 모터가 정지하는 것을 기본상태로 설정했고, 모터가 구동하다가 falling edge를 감지하면 모터 구동이 멈추도록 코드를 구성했다.

![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/e5176b21-3a53-4363-a0fc-b0597f287acb)
![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/674615bf-1e47-43eb-b5d4-6c38d339dc06)

  여닫이문은 레일과는 반대로 수납공간에 위치한 IR 센서의 출력값이 1->0->1로 변하면 110° 회전(명령어를 받고 문이 열려있는 상태)해 있던 서보모터가 다시 원위치(문이 닫혀있는 상태)로 돌아오도록 구성하였다. 약품이 수납공간에 보관되어 있는 상태(1, 초기 상태) -> 문이 열린 후 약품을 밖으로 꺼내 사용(0, 수납공간 안에 물체가 없는 상태) -> 사용한 약품을 다시 수납(1)으로 이러한 상태 변화가 일어나면 문이 닫힌다. 
  여닫이문의 기본값은 IR 센서값이 1이면 서보모터가 원위치에 있고, 0인 순간에는 서보모터가 110°에 위치한 상태를 기본으로 설정했다. 문이 닫혀있는 상태에는 안의 물건을 꺼낼 수 없고, 문이 열려있는 상태에서만 물건을 빼고 다시 수납하는 것이 가능했기에 문의 상태변수 doorstate를 추가했고, 문이 열려있는 경우에 currnetIRvalue의 rising edge를 감지하면 여닫이문을 닫을 수 있도록 했다. 또한 약품을 다시 수납하고 바로 문이 닫히지 않도록(손 끼임 방지) 7초의 delay를 추가했다.

<hr/>

##### ■ 작품외관
![image](https://github.com/Eugene821/smart_first_aid_box/assets/68239029/c3378719-52ea-44a9-a537-e493a1765fa3)


  


<!--
사용 부품
- Raspberry pi4 (server)
- Raspberry pi4 (client) - 음성인식
- Jetson Nano (client) - 영상처리
- Arduino UNO (client) - 기기 제어
- XPT2046 Touch Screen Controller
- Motor * 3
- Servo Motor * 2
- PLEOMAX 300K PIXELS Camera
- USB SPEAKER
- SF-555B MICROPHONE
- Mouse
- IR Sensor : HAM4311 * 4

2024.03.29 update
-->
