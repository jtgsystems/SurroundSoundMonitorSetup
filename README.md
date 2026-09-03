# 🔱 Monitor Soundstage

> **Automatic Multi-Monitor Audio Setup & Spatial Soundstage Calibrator for Linux (PipeWire / PulseAudio / WirePlumber)**

Turn your multi-monitor battlestation into a cohesive **Spatial Surround Sound (5.1 / 7.1)** or **Unified Wide Stereo (Wall of Sound)** acoustic array in seconds.

---

## ✨ Features

- 🖥️ **Zero-Config Display & Audio Discovery**: Automatically discovers all connected HDMI/DisplayPort audio endpoints across NVIDIA GPUs, AMD iGPUs/dGPUs, and Intel graphics.
- 🎚️ **Automatic Hardware Level Calibration**: Balances individual monitor physical speakers (e.g. 90%) while keeping master volume comfortable (e.g. 20%).
- 🔊 **Instant Sound Profiles**:
  - `1`: **Unified Wide Stereo (Wall of Sound)** — Parallel synchronized wide stereo across all monitors with balanced center fill.
  - `2`: **5.1 Spatial Surround Sound** — Discrete channel routing (Center dialogue on middle/top screens, bass on 34" ultrawides, surround wings on outer displays).
  - `3`: **7.1 Immersive Surround** — Multi-channel surround for 4+ screen battlestations.
- ⚔️ **Interactive 1v1 Audio Battle**: Built-in soundcheck and A/B test suite with synthesized multi-track stems and voice channel checks.
- 🌐 **YouTube Open Source / CC Audio Downloader**: Pulls Creative Commons surround sound reference tests via `yt-dlp`.
- 💾 **One-Click Persistence**: Automatically writes PipeWire drop-ins (`~/.config/pipewire/pipewire-pulse.conf.d/`) and desktop autostart so your audio profile survives reboots.

---

## 🚀 Installation & Quick Start

```bash
# Clone the repository
git clone https://github.com/jtgsystems/monitor-soundstage.git
cd monitor-soundstage

# Install locally
pip install -e .
```

### Run Interactive Menu:
```bash
monitor-soundstage
```

### CLI Quick Commands:
```bash
# Auto-detect and configure 5.1 surround sound
monitor-soundstage auto

# Switch to Wide Stereo profile
monitor-soundstage stereo

# Switch to 5.1 Surround profile
monitor-soundstage surround

# Run 1v1 Audio Comparison Battle
monitor-soundstage battle

# List detected monitor audio sinks
monitor-soundstage list
```

---

## 📐 Spatial Layout Architecture

```
                                [Top Ultrawide: LG 34"]
                                (Center Height / Dialogue)

                              [Center Vertical: LG 29"]
                                 (Center Vocal Anchor)

[Bottom-Left: Samsung 34"]                                 [Bottom-Right: Samsung 34"]           [Far-Right: Dell 27"]
   (Front Left + Bass)                                        (Front Right + Bass)             (Rear / Right Surround)
```

---

## 📜 License

MIT License © 2026 JTG Systems.
