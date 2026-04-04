# spotify-lyrics-display
This project displays the lyrics of the currently playing Spotify track on a 16x2 LCD connected to an Arduino. Additionally, LEDs indicate the progress of the song in real time:  Green → start of the song Yellow → middle Red → end  The project uses Python to fetch song info and lyrics, and communicates with the Arduino via serial.

## Demo picture 
<img width="1600" height="1200" alt="image" src="https://github.com/user-attachments/assets/fd5f7e6c-a62a-4fc3-85b1-dc0b7d127114" />

![WhatsAppVideo2026-04-04at4 17 35PM-ezgif com-optimize](https://github.com/user-attachments/assets/929f20b4-4876-4f1c-ba31-b85b29493e06)


## Features
-  Real-time Spotify playback synchronization
-  Live lyrics fetching from Genius API  
-  LED progress bar (Green 0-33%, Yellow 34-66%, Red 67-100%)
-  Arduino hardware integration
-  Auto-refreshing display

## Tech Stack
- **Python**: Spotipy, LyricsGenius, PySerial
- **Arduino**: C++, LiquidCrystal library
- **APIs**: Spotify Web API, Genius API

## Requirements
- Arduino Uno (or compatible)
- 16x2 LCD Display
- 3 LEDs (Green, Yellow, Red) + Resistors (220 ohm)
- Python 3.8+
- Spotify Premium account (for API access)
- 10kΩ Potentiometer (for LCD contrast control)
-----------------------------------------------------------------------------------------------------

## Setup Instructions

### 1. Hardware Wiring
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
------------------------------------------
### 2. Download and Install Python Dependencies 
```bash
pip install spotipy lyricsgenius pyserial
```
------------------------------------------
### API Setup
#### Spotify API(must have premium)

1. Go to https://developer.spotify.com/dashboard
2. Create an app
3. Copy:

Client ID
Client Secret
4. Set Redirect URI:
```
http://localhost:8888/callback
```

#### Genius API

1. Go to https://genius.com/api-clients
2. Generate an access token

------------------------------------------------------------------------
### Configure Project

Create a file called `config.py`:

```python
SPOTIFY_CLIENT_ID = "your_client_id"
SPOTIFY_CLIENT_SECRET = "your_client_secret"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

GENIUS_ACCESS_TOKEN = "your_genius_token"
SERIAL_PORT = "COM3"  # Change if needed
BAUD_RATE = 9600
```

----------------------------------------------------------------------

### Run the Project

1. Upload Arduino code
2. Connect Arduino via USB
3. Run Python script:

```bash
python main.py
```

----------------------------------------------------------------------

## 📁 Project Structure

```
spotify-lyrics-display/
│
├── Arduino/
│   └── lyrics_display.ino
│
├── Python/
│   └── main.py
│
├── config.py
├── README.md
└── .gitignore
```

---------------------------------------------------------------------

## Notes

* Make sure your Spotify app is **actively playing music**
* Serial port (COM3, etc.) may vary
* Lyrics timing is approximate (not timestamp-synced)

----------------------------------------------------------------------
## Future Improvemnts
*
Add real-time song timer
Sync lyrics with timestamps
Upgrade to OLED display
Add buttons for control
Wireless version using ESP32
---------------------------------------------------------------------
## License

This project is licensed under the MIT License.

