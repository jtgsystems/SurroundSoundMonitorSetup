import subprocess
import os
import tempfile
from typing import Optional

# Curated high-quality royalty-free / Creative Commons test audio URLs
CURATED_AUDIO_TRACKS = {
    "1": {
        "title": "Dolby 5.1 Channel Identification & Spatial Sound Test (CC-BY)",
        "url": "https://www.youtube.com/watch?v=PqVCPE8_nw4",
        "description": "True 5.1 channel voice check panning across all 6 speakers"
    },
    "2": {
        "title": "Royalty-Free Synthwave Surround Bassline Demo",
        "url": "https://www.youtube.com/watch?v=36YnV9STBqc",
        "description": "Multi-track dynamic synthwave with rich stereo & bass response"
    },
    "3": {
        "title": "Open Source Cinematic Orchestral Suite (CC0)",
        "url": "https://www.youtube.com/watch?v=1tqA4a7t3cE",
        "description": "Full orchestral acoustic soundstage with high dynamic range"
    }
}

def download_youtube_audio(url: str, out_dir: Optional[str] = None) -> Optional[str]:
    """Download audio stream from YouTube URL using yt-dlp."""
    if not out_dir:
        out_dir = tempfile.gettempdir()
    out_template = os.path.join(out_dir, "%(id)s.%(ext)s")
    
    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "wav",
        "-o", out_template,
        "--no-playlist",
        url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        for f in os.listdir(out_dir):
            if f.endswith(".wav") and (url.split("v=")[-1] in f if "v=" in url else True):
                return os.path.join(out_dir, f)
    except Exception as e:
        pass
    return None
