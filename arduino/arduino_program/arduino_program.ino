String versionString = "VERSION:DEMO_0.1";
String sensorString = "SENSORS:LED1,BUTTON1";

unsigned long startTime;
unsigned int interval = 1000; // 1 second

void setup() {
 pinMode(2, INPUT);
 pinMode(3, OUTPUT);

 startTime = millis();

 Serial.begin(9600); 
}

int switchState = 0;
int lastSwitchState = 0;

void printStatus() {
 Serial.println(versionString);
 Serial.println(sensorString);
}


void loop() {
  // Broadcast arduino info
  if(startTime + interval < millis()) {
    printStatus();
    startTime = startTime + interval;
  }
  // Handle button
  switchState = digitalRead(2);
  if (lastSwitchState != switchState) {
    // Button pressed or released
    lastSwitchState = switchState;
    if (switchState == LOW) {
      Serial.println("BUTTON1:LOW");
    } else {
      Serial.println("BUTTON1:HIGH");
    }
  }

  // Handle led
  String sensorName;
  String sensorValue;
  bool handleSensor = true;
  while (Serial.available()) {
    delay(3);  //delay to allow buffer to fill 
    if (Serial.available() >0) {
      char c = Serial.read();  //gets one byte from serial buffer
      if(c == ':') {
        handleSensor=false;
        continue;
      }
      if(handleSensor) {
        sensorName += c;
      } else {
        sensorValue += c;
      }
    }
  }
  if(sensorName == "LED1") {
    if (sensorValue == "ON") {
      digitalWrite(3, HIGH);
    } else {
      digitalWrite(3, LOW);
    }
  }
  delay(20);
}
