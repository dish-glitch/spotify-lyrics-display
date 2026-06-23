
[![Krishna Pulivendala](https://img.shields.io/badge/Author-Krishna%20Pulivendala-blue)](https://github.com/dish-glitch)
[![June 2026](https://img.shields.io/badge/Updated-June%202026-green)]()

# spotify-lyrics-display v2

Displays real-time **timestamp-synced lyrics** and song info across multiple hardware displays connected to an Arduino Uno. Python handles all the Spotify API calls and lyric fetching, sending data to the Arduino over serial.

> Built as a hardware + software integration project combining real-time APIs, embedded systems, and serial communication.

## Demo

*(coming soon)*

## Hardware

| Component | Role |
|---|---|
| Arduino Uno | Main controller |
| 16x2 LCD with I2C backpack | Artist name + song title |
| SSD1306 128x64 OLED | Synced lyrics — typewriter effect, blinking cursor, music visualizer |
| WS2812B NeoPixel ring (16 LED) | Song progress arc, green → yellow → red |

## Wiring

```
LCD  (I2C backpack)  →  SDA=A4, SCL=A5, 5V, GND
OLED (SSD1306)       →  SDA=A4, SCL=A5, 3.3V, GND
NeoPixel ring        →  DATA=pin 6, 5V, GND  (connect DI side only)
```

LCD and OLED share the same I2C bus (different addresses). If the LCD stays blank, change `LCD_ADDR` in the sketch from `0x27` to `0x3F`.

## Features

- Timestamp-synced lyrics via [LRCLIB](https://lrclib.net) (free, no API key)
- Typewriter effect with blinking cursor on OLED
- Animated equalizer bars on OLED
- Song progress bar on OLED
- NeoPixel ring fills as song progresses with smooth color gradient
- LCD refreshes every 30s so Arduino resets don't leave it stuck on the startup screen
- Local time interpolation between Spotify polls for tighter lyric sync

## Tech Stack

- **Python**: Spotipy, PySerial, Requests
- **Arduino**: C++, LiquidCrystal_I2C, Adafruit SSD1306/GFX, Adafruit NeoPixel
- **APIs**: Spotify Web API, LRCLIB

## Setup

### 1. Arduino Libraries

Install via Arduino IDE → Library Manager:
- `LiquidCrystal I2C` by Frank de Brabander
- `Adafruit GFX Library`
- `Adafruit SSD1306`
- `Adafruit NeoPixel`

### 2. Python Dependencies

```bash
pip install spotipy pyserial requests
```

### 3. Spotify API

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Create an app
3. Add redirect URI: `http://127.0.0.1:8888/callback`
4. Copy your **Client ID** and **Client Secret**

### 4. Configure

Edit `spotify_display.py` and fill in your credentials:

```python
ARDUINO_PORT  = 'COM3'               # your Arduino port
CLIENT_ID     = "your_client_id"
CLIENT_SECRET = "your_client_secret"
```

### 5. Run

1. Upload `spotify_display.ino` to the Arduino
2. Play something on Spotify
3. Run:

```bash
python spotify_display.py
```

A browser window opens for Spotify login on first run — after that the token is cached automatically.

## Serial Protocol

Python sends newline-terminated messages to the Arduino:

| Prefix | Example | Purpose |
|---|---|---|
| `L:` | `L:Artist\|Title\|Album` | LCD update |
| `Y:` | `Y:lyric line here` | OLED lyric |
| `P:` | `P:45` | Progress % → NeoPixel ring |

## Notes

- Lyrics depend on LRCLIB coverage — works great for popular/English songs
- Lyrics timing is interpolated locally between polls so sync stays tight
- Arduino Uno RAM is tight (~48% used) — adding more displays requires upgrading the board

## License

This project is licensed under the MIT License.
