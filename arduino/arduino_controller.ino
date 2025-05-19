const int pinX = A1;
const int pinY = A0;
const int upload = 2;
const int comment = 4;

const int UP_LED = 7;
const int DOWN_LED = 8;
const int LEFT_LED = 3;
const int RIGHT_LED = 12;

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

# define PIN  11
# define NUMPIXELS 16

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

bool up = true, down = true, left = true, right = true;

String currentJoystickState = "NEUTRAL";


void turnOnLED(String direction) {
  if (direction == "UP") digitalWrite(UP_LED, HIGH);
  else if (direction == "DOWN") digitalWrite(DOWN_LED, HIGH);
  else if (direction == "LEFT") digitalWrite(LEFT_LED, HIGH);
  else if (direction == "RIGHT") digitalWrite(RIGHT_LED, HIGH);
}

void turnOffLED(String direction) {
  if (direction == "UP") digitalWrite(UP_LED, LOW);
  else if (direction == "DOWN") digitalWrite(DOWN_LED, LOW);
  else if (direction == "LEFT") digitalWrite(LEFT_LED, LOW);
  else if (direction == "RIGHT") digitalWrite(RIGHT_LED, LOW);
}

void setup() {
  Serial.begin(9600);
  pinMode(upload, INPUT_PULLUP);
  pinMode(comment, INPUT_PULLUP);

  pinMode(UP_LED, OUTPUT);
  pinMode(DOWN_LED, OUTPUT);
  pinMode(LEFT_LED, OUTPUT);
  pinMode(RIGHT_LED, OUTPUT);

  digitalWrite(UP_LED, HIGH);
  digitalWrite(DOWN_LED, HIGH);
  digitalWrite(LEFT_LED, HIGH);
  digitalWrite(RIGHT_LED, HIGH);

  #if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
  #endif
  // END of Trinket-specific code.
  pixels.begin();
  pixels.clear();
  for (int i = 0; i < 1; i++) {
    pixels.setPixelColor(i, pixels.Color(200, 200, 255));
  }
  pixels.show();
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

  String newState = "NEUTRAL";

  if (uploadState == HIGH) {
    newState = "SAVE";
  } else if (commentState == HIGH) {
    newState = "COMMENT";
  } else if (mapX < -25) {
    newState = "RIGHT";
  } else if (mapX > 25) {
    newState = "LEFT";
  } else if (mapY < -25) {
    newState = "UP";
  } else if (mapY > 25) {
    newState = "DOWN";
  }

  if (currentJoystickState == "NEUTRAL" && newState != "NEUTRAL") {
    Serial.println(newState);
  }
  currentJoystickState = newState;

  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.startsWith("LED:") && command.length() > 4) {
      command.remove(0, 4); // Remove "LED:"

      // Flags for each direction
      up = down = left = right = false;

      int start = 0;
      while (true) {
        int commaIndex = command.indexOf(',', start);
        String dir = (commaIndex == -1) ? command.substring(start) : command.substring(start, commaIndex);
        dir.trim();  // Still needed, but must reassign
        dir.toUpperCase(); // Also must reassign

        if (dir == "UP") up = true;
        if (dir == "DOWN") down = true;
        if (dir == "LEFT") left = true;
        if (dir == "RIGHT") right = true;

        if (commaIndex == -1) break;
        start = commaIndex + 1;
      }
    }
  }
    // Turn LEDs on/off based on flags
    digitalWrite(UP_LED, up ? HIGH : LOW);
    digitalWrite(DOWN_LED, down ? HIGH : LOW);
    digitalWrite(LEFT_LED, left ? HIGH : LOW);
    digitalWrite(RIGHT_LED, right ? HIGH : LOW);
}