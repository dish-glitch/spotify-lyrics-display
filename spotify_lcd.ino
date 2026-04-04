#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// LED pins
const int greenLED = 6;
const int yellowLED = 7;
const int redLED = 8;

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);

  pinMode(greenLED, OUTPUT);
  pinMode(yellowLED, OUTPUT);
  pinMode(redLED, OUTPUT);

  lcd.print("Waiting...");
}

void loop() {
  if (Serial.available() > 0) {
    String text = Serial.readStringUntil('\n');
    text.trim();

    // Check if the message is a lyric chunk or progress
    if (text.startsWith("PROG:")) {
      // Format from Python: PROG:45  (percentage 0-100)
      int percent = text.substring(5).toInt();

      // LED logic
      if (percent < 34) {
        digitalWrite(greenLED, HIGH);
        digitalWrite(yellowLED, LOW);
        digitalWrite(redLED, LOW);
      } else if (percent < 67) {
        digitalWrite(greenLED, LOW);
        digitalWrite(yellowLED, HIGH);
        digitalWrite(redLED, LOW);
      } else {
        digitalWrite(greenLED, LOW);
        digitalWrite(yellowLED, LOW);
        digitalWrite(redLED, HIGH);
      }

    } else {
      // Lyric chunk (old code)
      lcd.clear();
      String line1 = text.substring(0, min(16, text.length()));
      String line2 = "";
      if (text.length() > 16) line2 = text.substring(16, min(32, text.length()));

      lcd.setCursor(0, 0);
      lcd.print(line1);
      lcd.setCursor(0, 1);
      lcd.print(line2);
    }
  }
}