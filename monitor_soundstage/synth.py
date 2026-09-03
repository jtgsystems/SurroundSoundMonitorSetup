import wave
import tempfile
import os
import subprocess
import numpy as np
from typing import Tuple

def get_bundled_audio_path(filename: str) -> str:
    """Check for bundled audio file in package directory or fallback."""
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidate = os.path.join(pkg_dir, "audio", filename)
    if os.path.exists(candidate):
        return candidate
    return ""

def generate_voice_intro(text: str, out_wav: str):
    """Generate spoken announcement using espeak-ng."""
    try:
        subprocess.run(["espeak-ng", "-w", out_wav, "-s", "150", text], capture_output=True, check=True)
    except Exception:
        sr = 48000
        t = np.linspace(0, 0.5, int(sr * 0.5), False)
        tone = (np.sin(2 * np.pi * 440 * t) * 0.3 * 32767).astype(np.int16)
        with wave.open(out_wav, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(tone.tobytes())

def generate_stereo_soundstage_demo(duration: float = 6.0, sample_rate: int = 48000) -> str:
    """Load or generate lossless stereo soundstage demo WAV."""
    bundled = get_bundled_audio_path("wide_stereo_soundstage_sweep.wav")
    if bundled:
        return bundled
        
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    pan = 0.5 * (1 + np.sin(2 * np.pi * 0.35 * t - np.pi/2))
    
    f0, f1, f2, f3 = 220, 277.18, 329.63, 440
    note = np.sin(2 * np.pi * f0 * t) + 0.7 * np.sin(2 * np.pi * f1 * t) + 0.5 * np.sin(2 * np.pi * f2 * t) + 0.3 * np.sin(2 * np.pi * f3 * t)
    env = np.exp(-0.25 * t) * (1 - np.exp(-10 * t))
    audio = note * env
    
    left_ch = (audio * (1 - pan) * 0.6 * 32767).astype(np.int16)
    right_ch = (audio * pan * 0.6 * 32767).astype(np.int16)
    stereo_audio = np.column_stack((left_ch, right_ch))
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name
        with wave.open(wav_path, "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(stereo_audio.tobytes())
    return wav_path

def generate_surround_5_1_demo(duration: float = 8.0, sample_rate: int = 48000) -> str:
    """Load or generate lossless 6-channel 5.1 discrete surround demo WAV."""
    bundled = get_bundled_audio_path("surround_5_1_cinematic_demo.wav")
    if bundled:
        return bundled
        
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    chords = [
        {"root": 220.0, "notes": [220.0, 261.63, 329.63, 440.0]},
        {"root": 174.61, "notes": [174.61, 220.0, 261.63, 349.23]},
        {"root": 130.81, "notes": [261.63, 329.63, 392.0, 523.25]},
        {"root": 196.00, "notes": [196.0, 246.94, 293.66, 392.0]}
    ]
    
    bass = np.zeros_like(t)
    for i, ch in enumerate(chords):
        t_start, t_end = i * 2.0, (i + 1) * 2.0
        idx = (t >= t_start) & (t < t_end)
        t_sec = t[idx] - t_start
        f = ch["root"] / 2.0 if ch["root"] > 150 else ch["root"]
        bass[idx] = (np.sin(2 * np.pi * f * t_sec) + 0.3 * np.sin(4 * np.pi * f * t_sec))
        
    track_l = np.zeros_like(t)
    track_r = np.zeros_like(t)
    for i, ch in enumerate(chords):
        t_start, t_end = i * 2.0, (i + 1) * 2.0
        idx = (t >= t_start) & (t < t_end)
        t_sec = t[idx] - t_start
        for j, n in enumerate(ch["notes"][:2]):
            t_note = np.clip(t_sec - j * 0.5, 0, None)
            track_l[idx] += np.sin(2 * np.pi * n * t_note) * np.exp(-1.5 * (t_note % 1.0))
        for j, n in enumerate(ch["notes"][2:]):
            t_note = np.clip(t_sec - j * 0.5, 0, None)
            track_r[idx] += np.sin(2 * np.pi * n * t_note) * np.exp(-1.5 * (t_note % 1.0))
            
    lead = np.zeros_like(t)
    melody_notes = [440.0, 523.25, 659.25, 783.99, 659.25, 523.25, 440.0, 392.0]
    for i, n in enumerate(melody_notes):
        t_start, t_end = i * 1.0, (i + 1) * 1.0
        idx = (t >= t_start) & (t < t_end)
        t_sec = t[idx] - t_start
        lead[idx] = (np.sin(2 * np.pi * n * t_sec) + 0.5 * np.sin(4 * np.pi * n * t_sec)) * np.exp(-1.2 * t_sec)
        
    shimmer_l = track_l * 0.6 * np.sin(2 * np.pi * 0.25 * t)
    shimmer_r = track_r * 0.6 * np.cos(2 * np.pi * 0.25 * t)
    
    ch_fl = (track_l / (np.max(np.abs(track_l)) + 1e-6) * 0.7 * 32767).astype(np.int16)
    ch_fr = (track_r / (np.max(np.abs(track_r)) + 1e-6) * 0.7 * 32767).astype(np.int16)
    ch_fc = (lead / (np.max(np.abs(lead)) + 1e-6) * 0.8 * 32767).astype(np.int16)
    ch_lfe = (bass / (np.max(np.abs(bass)) + 1e-6) * 0.8 * 32767).astype(np.int16)
    ch_rl = (shimmer_l / (np.max(np.abs(shimmer_l)) + 1e-6) * 0.6 * 32767).astype(np.int16)
    ch_rr = (shimmer_r / (np.max(np.abs(shimmer_r)) + 1e-6) * 0.6 * 32767).astype(np.int16)
    
    surround_mix = np.column_stack((ch_fl, ch_fr, ch_fc, ch_lfe, ch_rl, ch_rr))
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav_path = f.name
        with wave.open(wav_path, "wb") as wf:
            wf.setnchannels(6)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(surround_mix.tobytes())
    return wav_path

def play_audio(device_name: str, wav_path: str):
    """Play audio file through target PipeWire/Pulse device."""
    subprocess.run(["paplay", f"--device={device_name}", wav_path], capture_output=True)
