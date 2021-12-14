#include <MotorDriver.h>

#define MOTORTYPE YF_IIC_TB //
uint8_t SerialDebug = 0;    // 串口打印调试 0-否 1-是

// these constants are used to allow you to make your motor configuration
// line up with function names like forward.  Value can be 1 or -1
const int offsetm1 = 1;
const int offsetm2 = -1;
const int offsetm3 = 1;
const int offsetm4 = -1;

char Key;

// Initializing motors.
MotorDriver motorDriver = MotorDriver(MOTORTYPE);

void setup()
{
    Serial.begin(9600);
    Serial.println("Motor Drive test!");
    motorDriver.begin();
    motorDriver.motorConfig(offsetm1, offsetm2, offsetm3, offsetm4);
    delay(1000); // wait 2s
    Serial.println("Start...");
}

void loop()
{
    while (Serial.available() > 0) {
        Key = Serial.read();
        delay(10);
    }

    switch (Key) {
        case 'S': {
            motorDriver.setMotor(2048, 2048, 2048, 2048);
            break;
        }
        case 's': {
            motorDriver.setMotor(512, 512, 512, 512);
            break;
        }
        case 'W': {
            motorDriver.setMotor(-2048, -2048, -2048, -2048);
            break;
        }
        case 'w': {
            motorDriver.setMotor(-512, -512, -512, -512);
            break;
        }
        case 'A': {
            motorDriver.setMotor(-4096, 4096, -4096, 4096);
            break;
        }
        case 'a': {
            motorDriver.setMotor(-1024, 1024, -1024, 1024);
            break;
        }
        case 'D': {
            motorDriver.setMotor(4096, -4096, 4096, -4096);
            break;
        }
        case 'd': {
            motorDriver.setMotor(1024, -1024, 1024, -1024);
            break;
        }
        default: {
            motorDriver.setMotor(0, 0, 0, 0);
            break;
        }
    }
}