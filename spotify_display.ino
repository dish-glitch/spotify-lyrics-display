#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_NeoPixel.h>

#define NEO_PIN   6
#define LCD_ADDR  0x27   // try 0x3F if LCD stays blank
#define OLED_ADDR 0x3C
#define OLED_W    128
#define OLED_H     64
#define NEO_N      16

LiquidCrystal_I2C lcd(LCD_ADDR, 16, 2);
Adafruit_SSD1306  oled(OLED_W, OLED_H, &Wire, -1);
Adafruit_NeoPixel ring(NEO_N, NEO_PIN, NEO_GRB + NEO_KHZ800);

char     lyric[64]  = "Waiting...";
char     partial[64];
uint8_t  twPos      = 0;
uint32_t twMs       = 0;
#define  TW_MS 38

uint32_t flashUntil = 0;
int      progress   = 0;

int8_t   bH[8]   = {3,5,2,6,4,1,7,3};
int8_t   bTgt[8] = {5,2,6,1,5,4,2,6};
uint32_t bMs     = 0;

char    rxBuf[84];
uint8_t rxIdx = 0;

uint32_t oledMs = 0;

void updateRing() {
    int ledsOn = ((long)progress * NEO_N) / 100;
    ring.clear();
    for (int i = 0; i < ledsOn; i++) {
        uint8_t r = (i < 8) ? map(i, 0, 7, 0, 255) : 255;
        uint8_t g = (i < 8) ? 180 : map(i, 8, 15, 150, 0);
        ring.setPixelColor(i, ring.Color(r, g, 0));
    }
    if (ledsOn < NEO_N)
        ring.setPixelColor(ledsOn, ring.Color(25, 25, 100));
    ring.show();
}

void animBars() {
    uint32_t now = millis();
    if (now - bMs < 110) return;
    bMs = now;
    for (int i = 0; i < 8; i++) {
        if      (bH[i] < bTgt[i]) bH[i]++;
        else if (bH[i] > bTgt[i]) bH[i]--;
        else                       bTgt[i] = random(1, 9);
    }
}

void drawOLED() {
    oled.clearDisplay();

    int pw = (long)progress * OLED_W / 100;
    oled.fillRect(0, 0, pw, 4, SSD1306_WHITE);
    oled.drawLine(0, 4, OLED_W - 1, 4, SSD1306_WHITE);

    if (millis() < flashUntil)
        oled.fillRect(0, 6, OLED_W, 2, SSD1306_WHITE);

    uint8_t len  = strlen(lyric);
    uint8_t show = (twPos < len) ? twPos : len;
    memcpy(partial, lyric, show);
    partial[show] = '\0';

    bool big = (len <= 10);
    oled.setTextSize(big ? 2 : 1);
    oled.setTextWrap(true);
    oled.setCursor(0, 10);
    oled.print(partial);

    if (twPos < len && (millis() / 350) % 2 == 0) {
        int cpl = big ? 10 : 21;
        int cw  = big ? 12 : 6;
        int ch  = big ? 16 : 8;
        int cx  = (show % cpl) * cw;
        int cy  = 10 + (show / cpl) * ch;
        if (cy < OLED_H - 15)
            oled.fillRect(cx, cy, cw - 2, ch - 1, SSD1306_WHITE);
    }

    animBars();
    for (int i = 0; i < 8; i++) {
        int h = bH[i] * 2 + 2;
        oled.fillRect(2 + i * 16, OLED_H - h, 10, h, SSD1306_WHITE);
    }

    oled.display();
}

void parseRx() {
    if (rxBuf[0]=='L' && rxBuf[1]==':') {
        char* artist = rxBuf + 2;
        char* sep1   = strchr(artist, '|');
        if (!sep1) return;
        *sep1 = '\0';
        char* title = sep1 + 1;
        char* sep2  = strchr(title, '|');
        if (sep2) *sep2 = '\0';
        lcd.clear();
        lcd.setCursor(0, 0); lcd.print(artist);
        lcd.setCursor(0, 1); lcd.print(title);

    } else if (rxBuf[0]=='Y' && rxBuf[1]==':') {
        char* newL = rxBuf + 2;
        if (strcmp(newL, lyric) != 0) {
            strncpy(lyric, newL, sizeof(lyric) - 1);
            lyric[sizeof(lyric) - 1] = '\0';
            twPos      = 0;
            twMs       = millis();
            flashUntil = millis() + 100;
        }

    } else if (rxBuf[0]=='P' && rxBuf[1]==':') {
        int p = atoi(rxBuf + 2);
        if (p != progress) {
            progress = constrain(p, 0, 100);
            updateRing();
        }
    }
}

void setup() {
    Serial.begin(9600);

    lcd.init();
    lcd.backlight();
    lcd.print(F("  Spotify LCD   "));
    lcd.setCursor(0, 1);
    lcd.print(F("  Loading...    "));

    oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
    oled.clearDisplay();
    oled.setTextColor(SSD1306_WHITE);
    oled.setTextSize(1);
    oled.setCursor(14, 28);
    oled.print(F("Spotify Lyrics"));
    oled.display();

    ring.begin();
    ring.setBrightness(55);
    ring.clear();
    ring.show();
}

void loop() {
    while (Serial.available()) {
        char c = Serial.read();
        if (c == '\n') {
            rxBuf[rxIdx] = '\0';
            parseRx();
            rxIdx = 0;
        } else if (rxIdx < sizeof(rxBuf) - 1) {
            rxBuf[rxIdx++] = c;
        }
    }

    uint32_t now = millis();

    if (twPos < strlen(lyric) && now - twMs >= TW_MS) {
        twPos++;
        twMs = now;
    }

    if (now - oledMs >= 50) {
        drawOLED();
        oledMs = now;
    }
}
