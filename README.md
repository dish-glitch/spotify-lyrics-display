
[![Krishna Pulivendala](https://img.shields.io/badge/Author-Krishna%20Pulivendala-blue)](https://github.com/dish-glitch)
[![June 2026](https://img.shields.io/badge/Updated-June%202026-green)]()

# spotify-lyrics-display

Displays real-time Spotify lyrics and song info on hardware displays connected to an Arduino Uno.

---

## Version 2 (Current) — June 2026

Upgraded hardware and switched to **timestamp-synced lyrics** via LRCLIB. Python handles all API calls and lyric timing, sending data to the Arduino over serial.

## Pictures! 
Cinderella - Mac Miller & Ty Dolla $ign
<img width="1024" height="576" alt="image" src="https://github.com/user-attachments/assets/75599aa5-789a-488b-8200-5a8f58f336a1" />
<img width="576" height="1024" alt="image" src="https://github.com/user-attachments/assets/716a14c2-bb22-47c6-85e8-5d3e0b3497ad" />



NOBLE - F3miii 
<img width="576" height="1024" alt="image" src="https://github.com/user-attachments/assets/e7893fdc-c3af-4a79-b577-8e710e50f968" />

(Any song works as long as LRCLIB can find the lyrics)



### New Hardware

| Component | Role |
|---|---|
| Arduino Uno | Main controller |
| 16x2 LCD with I2C backpack | Artist name + song title |
| SSD1306 128x64 OLED | Synced lyrics — typewriter effect, blinking cursor, music visualizer |
| WS2812B NeoPixel ring (16 LED) | Song progress arc, green → yellow → red |

### Wiring (v2)

```
LCD  (I2C backpack)  →  SDA=A4, SCL=A5, 5V, GND
OLED (SSD1306)       →  SDA=A4, SCL=A5, 3.3V, GND
NeoPixel ring        →  DATA=pin 6, 5V, GND  (connect DI side only)
```

LCD and OLED share the same I2C bus. If LCD stays blank, change `LCD_ADDR` in the sketch from `0x27` to `0x3F`.

### New Features

- Timestamp-synced lyrics via [LRCLIB](https://lrclib.net) (free, no API key needed)
- Typewriter effect with blinking cursor on OLED
- Animated equalizer bars on OLED
- Song progress bar on OLED
- NeoPixel ring fills with smooth green → yellow → red gradient
- LCD refreshes every 30s so Arduino resets don't leave it stuck
- Local time interpolation between Spotify polls for tighter sync

### Tech Stack (v2)

- **Python**: Spotipy, PySerial, Requests
- **Arduino**: C++, LiquidCrystal_I2C, Adafruit SSD1306/GFX, Adafruit NeoPixel
- **APIs**: Spotify Web API, LRCLIB

### Setup (v2)

**Arduino Libraries** — install via Library Manager:
- `LiquidCrystal I2C` by Frank de Brabander
- `Adafruit GFX Library`
- `Adafruit SSD1306`
- `Adafruit NeoPixel`

**Python:**
```bash
pip install spotipy pyserial requests
```

**Spotify API:**
1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Create an app and add redirect URI: `http://127.0.0.1:8888/callback`
3. Copy your Client ID and Client Secret

**Configure** `spotify_display.py`:
```python
ARDUINO_PORT  = 'COM3'               # your Arduino port
CLIENT_ID     = "your_client_id"
CLIENT_SECRET = "your_client_secret"
```

**Run:**
```bash
python spotify_display.py
```

A browser window opens for Spotify login on first run. After that the token is saved automatically.

### Files (v2)

- `spotify_display.ino` — Arduino sketch
- `spotify_display.py` — Python script

---
## AI Tools Used

- **[Claude (Anthropic)](https://claude.ai/)** — Helped write and organize this
  README into a presentable format, and helped diagnose an LCD display freeze
  that was resolved with a firmware fix. Wiring (OLED, LCD, NeoPixel ring),
  all testing, firmware, and troubleshooting were done by me.

## Version 1 (Original) — April 2026

### Demo

<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/fd5f7e6c-a62a-4fc3-85b1-dc0b7d127114" />

![WhatsAppVideo2026-04-04at4 17 35PM-ezgif com-optimize](https://github.com/user-attachments/assets/929f20b4-4876-4f1c-ba31-b85b29493e06)

This project displays the lyrics of the currently playing Spotify track on a 16x2 LCD connected to an Arduino. Additionally, LEDs indicate the progress of the song in real time: Green → start of the song Yellow → middle Red → end. The project uses Python to fetch song info and lyrics, and communicates with the Arduino via serial.

> Built as a hardware + software integration project combining real-time APIs, embedded systems, and serial communication.

### Features (v1)

- Real-time Spotify playback synchronization
- Live lyrics fetching from Genius API
- LED progress bar (Green 0-33%, Yellow 34-66%, Red 67-100%)
- Arduino hardware integration
- Auto-refreshing display

### Tech Stack (v1)

- **Python**: Spotipy, LyricsGenius, PySerial
- **Arduino**: C++, LiquidCrystal library
- **APIs**: Spotify Web API, Genius API

### Requirements (v1)

- Arduino Uno (or compatible)
- 16x2 LCD Display
- 3 LEDs (Green, Yellow, Red) + Resistors (220 ohm)
- Python 3.8+
- Spotify Premium account (for API access)
- 10kΩ Potentiometer (for LCD contrast control)

### Wiring (v1)

**LCD Display:**
- RS: Pin 12
- E: Pin 11
- D4: Pin 5
- D5: Pin 4
- D6: Pin 3
- D7: Pin 2
- V0 (Contrast): Potentiometer middle pin (outer pins to 5V/GND)

**LEDs:**
- Green LED: Pin 6 (with 220Ω resistor)
- Yellow LED: Pin 7 (with 220Ω resistor)
- Red LED: Pin 8 (with 220Ω resistor)

### Setup (v1)

```bash
pip install spotipy lyricsgenius pyserial
```

**Spotify API:**
1. Go to https://developer.spotify.com/dashboard
2. Create an app and copy Client ID + Client Secret
3. Set Redirect URI: `http://localhost:8888/callback`

**Genius API:**
1. Go to https://genius.com/api-clients
2. Generate an access token

**Configure** `config.py`:
```python
SPOTIFY_CLIENT_ID = "your_client_id"
SPOTIFY_CLIENT_SECRET = "your_client_secret"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
GENIUS_ACCESS_TOKEN = "your_genius_token"
SERIAL_PORT = "COM3"
BAUD_RATE = 9600
```

**Run:**
```bash
python spotify_lcd.py
```

### Files (v1)

- `spotify_lcd.ino` — Arduino sketch
- `spotify_lcd.py` — Python script

---

## License

This project is licensed under the MIT License.
