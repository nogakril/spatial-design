const int pinX = A1;
const int pinY = A0;
const int upload = 2;
const int comment = 4;

// const int UP_LED = 5;
// const int DOWN_LED = 6;
// const int LEFT_LED = 13;
// const int RIGHT_LED = 12;

// void turnOffAllLEDs() {
//   digitalWrite(UP_LED, LOW);
//   digitalWrite(DOWN_LED, LOW);
//   digitalWrite(LEFT_LED, LOW);
//   digitalWrite(RIGHT_LED, LOW);
// }
//
// void turnOnLED(String direction) {
//   if (direction == "UP") digitalWrite(UP_LED, HIGH);
//   else if (direction == "DOWN") digitalWrite(DOWN_LED, HIGH);
//   else if (direction == "LEFT") digitalWrite(LEFT_LED, HIGH);
//   else if (direction == "RIGHT") digitalWrite(RIGHT_LED, HIGH);
// }

void setup() {
  Serial.begin(9600);
  pinMode(upload, INPUT_PULLUP);
  pinMode(comment, INPUT_PULLUP);

//   pinMode(UP_LED, OUTPUT);
//   pinMode(DOWN_LED, OUTPUT);
//   pinMode(LEFT_LED, OUTPUT);
//   pinMode(RIGHT_LED, OUTPUT);
//
//   turnOffAllLEDs();
}

void loop() {
  int valX = analogRead(pinX);
  int valY = analogRead(pinY);
  int mapX = map(valX, 253, 768, -50, 50);
  int mapY = map(valY, 252, 769, -50, 50);

  int uploadState = digitalRead(upload);
  int commentState = digitalRead(comment);

  // Allow only one axis movement at a time
  if (abs(mapX) >= 25) mapY = 0;
  else if (abs(mapY) >= 25) mapX = 0;


  if (uploadState == LOW) {
    Serial.println("SAVE");
  } else if (commentState == LOW) {
    Serial.println("COMMENT");
  } else if (mapX > 25) {
    Serial.println("RIGHT");
  } else if (mapX < -25) {
    Serial.println("LEFT");
  } else if (mapY > 25) {
    Serial.println("UP");
  } else if (mapY < -25) {
    Serial.println("DOWN");
  }

//   if (Serial.available()) {
//     String command = Serial.readStringUntil('\n');
//     command.trim();
//
//     if (command.startsWith("LED:")) {
//         turnOffAllLEDs();
//
//         command.remove(0, 4);
//         int start = 0;
//
//         while (true) {
//         int commaIndex = command.indexOf(',', start);
//         String dir = (commaIndex == -1) ? command.substring(start) : command.substring(start, commaIndex);
//         dir.trim();
//         turnOnLED(dir);
//
//         if (commaIndex == -1) break;
//         start = commaIndex + 1;
//         }
//     }
//   }

  delay(300);
}
