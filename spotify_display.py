import spotipy
from spotipy.oauth2 import SpotifyOAuth
import serial
import time
import requests
import re
import os

# ============ CONFIG ============
ARDUINO_PORT  = 'COM8'                      # change to your port
BAUD_RATE     = 9600
CLIENT_ID     = "YOUR_CLIENT_ID"            # from developer.spotify.com
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI  = "http://127.0.0.1:8888/callback"
# ================================

def fetch_synced_lyrics(artist, title):
    try:
        r = requests.get(
            "https://lrclib.net/api/get",
            params={"artist_name": artist, "track_name": title},
            timeout=6
        )
        if r.status_code == 200:
            data = r.json()
            if data.get("syncedLyrics"):
                return parse_lrc(data["syncedLyrics"])
    except Exception as e:
        print(f"  [lrclib] {e}")
    return None

def parse_lrc(text):
    lines = []
    pat = re.compile(r'\[(\d{2}):(\d{2})[\.:](\d{2,3})\](.*)')
    for line in text.split('\n'):
        m = pat.match(line.strip())
        if m:
            mins, secs, frac, lyric = m.groups()
            ms = int(mins)*60000 + int(secs)*1000 + int(frac.ljust(3,'0')[:3])
            lyric = lyric.strip()
            if lyric:
                lines.append((ms, lyric))
    return lines or None

def get_lyric_at(lyrics, ms):
    result = ""
    for ts, text in lyrics:
        if ms >= ts:
            result = text
        else:
            break
    return result

def tx(ser, msg):
    try:
        ser.write((msg + '\n').encode('utf-8', errors='replace'))
    except Exception as e:
        print(f"  [serial] {e}")

# ---- Init ----
if os.path.exists(".cache"):
    os.remove(".cache")

print("Connecting to Arduino...")
ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
print("Arduino connected.")

print("Connecting to Spotify...")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-currently-playing",
    open_browser=True
))
print("Ready.\n")

last_id       = ""
lyrics        = None
last_lyric    = ""
last_pct      = -1
snapshot_ms   = 0
snapshot_time = 0.0
last_lcd_send = 0

while True:
    try:
        cur = sp.current_user_playing_track()

        if cur and cur.get('is_playing') and cur.get('item'):
            item     = cur['item']
            track_id = item['id']
            prog_ms  = cur['progress_ms']
            dur_ms   = item['duration_ms']

            snapshot_ms   = prog_ms
            snapshot_time = time.time()

            pct = int((prog_ms / dur_ms) * 100)

            now_t = time.time()
            if track_id != last_id or (now_t - last_lcd_send) > 30:
                last_lcd_send = now_t
                if track_id != last_id:
                    last_id = track_id
                    lyrics  = None
                    last_lyric = ""

                artist = item['artists'][0]['name']
                title  = item['name']
                album  = item.get('album', {}).get('name', '')

                print(f"\n>> {artist} - {title}")
                tx(ser, f"L:{artist}|{title}|{album}")

                if lyrics is None:
                    clean  = re.sub(r'\s*[\(\[][^)\]]+[\)\]]', '', title).strip()
                    lyrics = fetch_synced_lyrics(artist, clean)
                    print(f"   Lyrics: {'synced ({} lines)'.format(len(lyrics)) if lyrics else 'not found'}")
                    if not lyrics:
                        tx(ser, "Y:No synced lyrics")

            if lyrics:
                estimated = snapshot_ms + int((time.time() - snapshot_time) * 1000)
                lyric = get_lyric_at(lyrics, estimated)
                if lyric != last_lyric:
                    last_lyric = lyric
                    print(f"   ♪ {lyric}")
                    tx(ser, f"Y:{lyric}")

            if pct != last_pct:
                last_pct = pct
                tx(ser, f"P:{pct}")

        else:
            if last_id:
                last_id = ""
                tx(ser, "L:Paused||")
                tx(ser, "Y:Nothing playing")
                tx(ser, "P:0")

        time.sleep(0.4)

    except Exception as e:
        print(f"[error] {e}")
        time.sleep(5)
