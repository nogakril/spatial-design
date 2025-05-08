const int pinX = A1;
const int pinY = A0;
const int upload = 8;
const int comment = 7;

void setup() {
  Serial.begin(9600);
  pinMode(upload, INPUT_PULLUP);
  pinMode(comment, INPUT_PULLUP);
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

  delay(300);
}
