#include <Wire.h>

const int MPU=0x68;  //MPU 6050 의 I2C 기본 주소
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;

int vib_left_pin = 3;
int vib_right_pin = 2;
int grad_virt_pin = 9;
int grad_hori_pin = 10;

void setup(){
  Serial.begin(9600);
  Wire.begin();      //Wire 라이브러리 초기화
  Wire.beginTransmission(MPU); //MPU로 데이터 전송 시작
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     //MPU-6050 시작 모드로
  Wire.endTransmission(true); 

  pinMode(vib_left_pin, INPUT);
  pinMode(vib_right_pin, INPUT);
  pinMode(grad_virt_pin, INPUT);
  pinMode(grad_hori_pin, INPUT);
}

void loop(){
  Wire.beginTransmission(MPU);    //데이터 전송시작
  Wire.write(0x3B);               // register 0x3B (ACCEL_XOUT_H), 큐에 데이터 기록
  Wire.endTransmission(false);    //연결유지
  Wire.requestFrom(MPU,14,true);  //MPU에 데이터 요청
  //데이터 한 바이트 씩 읽어서 반환
  AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
  AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  GyX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GyY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  GyZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
  
  //delay(60);
  //long vib_left = pulseIn(vib_left_pin, HIGH, 100);
  //delay(60);
  //long vib_right = pulseIn(vib_right_pin, HIGH, 100);
  int grad_virt = digitalRead(grad_virt_pin);
  int grad_hori = digitalRead(grad_hori_pin);
  
  //시리얼 모니터에 출력
  // ACX ACY ACZ TMP GYX GYY GYZ GV GH
  Serial.print(""); Serial.print(AcX);
  Serial.print("|"); Serial.print(AcY);
  Serial.print("|"); Serial.print(AcZ);
  Serial.print("|"); Serial.print(Tmp/340.00+36.53);  
  Serial.print("|"); Serial.print(GyX);
  Serial.print("|"); Serial.print(GyY);
  Serial.print("|"); Serial.print(GyZ);
  //Serial.print("|"); Serial.print(vib_left);
  //Serial.print("|"); Serial.print(vib_right);
  Serial.print("|"); Serial.print(grad_virt);
  Serial.print("|"); Serial.print(grad_hori);
  Serial.println();
  delay(100);
}
