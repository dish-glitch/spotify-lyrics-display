import spotipy
from spotipy.oauth2 import SpotifyOAuth
import serial
import time
import os
import lyricsgenius

# ================= CONFIG =================
ARDUINO_PORT = 'COM20'  # change to your Arduino port
SPOTIFY_CLIENT_ID = "ADD YOUR OWN ID "
SPOTIFY_CLIENT_SECRET = "ADD YOUR OWN SECRET"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
GENIUS_API_KEY = "ADD YOUR OWN API KEY"
# ==========================================

# Genius setup
genius = lyricsgenius.Genius(GENIUS_API_KEY)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True

# Clear Spotify cache
if os.path.exists(".cache"):
    os.remove(".cache")

# Connect Arduino
print("🔌 Connecting to Arduino...")
ser = serial.Serial(ARDUINO_PORT, 9600, timeout=1)
time.sleep(2)
print("✅ Connected")

# Connect Spotify
print("🎵 Connecting to Spotify...")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-currently-playing",
    open_browser=True
))

print("🎶 Running...\n")

last_song_id = ""
lyrics_chunks = []
chunk_index = 0
prev_chunk = ""

while True:
    try:
        current = sp.current_user_playing_track()

        if current and current.get('is_playing') and current.get('item'):
            track_id = current['item']['id']

            # Only fetch new lyrics if song changed
            if track_id != last_song_id:
                last_song_id = track_id
                track = current['item']['name']
                artist = current['item']['artists'][0]['name']
                track_clean = track.split("(")[0].strip()

                print(f"🎵 New song detected: {track} - {artist}")

                try:
                    song = genius.search_song(track_clean, artist)
                except Exception as e:
                    print("❌ Genius error:", e)
                    song = None

                if song and song.lyrics:
                    lyrics = song.lyrics.split("\n")
                    # Break each line into 32-char chunks
                    lyrics_chunks = []
                    for line in lyrics:
                        line = line.strip()
                        if not line:
                            continue
                        if "[" in line and "]" in line:
                            continue
                        for i in range(0, len(line), 32):
                            chunk = line[i:i+32]
                            # Add "||" if it's a new lyric line
                            if prev_chunk and chunk != prev_chunk:
                                chunk = "|| " + chunk
                                if len(chunk) > 32:
                                    chunk = chunk[:32]
                            lyrics_chunks.append(chunk)
                            prev_chunk = chunk.replace("|| ", "")
                    chunk_index = 0
                else:
                    lyrics_chunks = ["Lyrics not found"]
                    chunk_index = 0

            # Send current lyric chunk
            if lyrics_chunks:
                ser.write((lyrics_chunks[chunk_index] + "\n").encode())
                print(lyrics_chunks[chunk_index])
                chunk_index = (chunk_index + 1) % len(lyrics_chunks)

            # Send song progress to Arduino
            progress_ms = current['progress_ms']
            duration_ms = current['item']['duration_ms']
            percent = int((progress_ms / duration_ms) * 100)
            ser.write(f"PROG:{percent}\n".encode())

        else:
            ser.write("No music\n".encode())

        time.sleep(1)  # wait before next update (lyric chunk + progress) 

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(5)