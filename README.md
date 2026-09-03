# 🔱 Monitor Soundstage

<div align="center">

![Monitor Soundstage 5.1 Architecture](assets/monitor-soundstage-5-1.jpg)

**Automatic Multi-Monitor Audio Setup & Spatial Soundstage Calibrator for Linux (PipeWire / PulseAudio / WirePlumber)**

[![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20PipeWire%20%7C%20PulseAudio-purple.svg)]()
[![Created By](https://img.shields.io/badge/Created%20By-JTG%20Systems-gold.svg)](https://jtgsystems.com)

*Turn your multi-monitor battlestation into a cohesive **Spatial Surround Sound (5.1 / 7.1)** or **Unified Wide Stereo (Wall of Sound)** acoustic array in seconds using your screens as speakers.*

</div>

---

## ✨ Why Monitor Soundstage?

Most desktop battlestations feature 2 to 6 monitors with built-in speakers that sit unused or play in isolated stereo pairs. **Monitor Soundstage** unifies all monitor hardware audio endpoints into a coordinated spatial soundstage directly from PipeWire and PulseAudio.

- 🖥️ **Zero-Config Display & Audio Discovery**: Automatically discovers all connected HDMI/DisplayPort audio endpoints across NVIDIA GPUs, AMD iGPUs/dGPUs, and Intel graphics.
- 🎚️ **Automatic Hardware Level Calibration**: Locks individual monitor physical speakers (e.g. 90%) while keeping master volume comfortable (e.g. 20%).
- 🔊 **Instant 1-2-3 Sound Profiles**:
  - `[1]`: **Unified Wide Stereo (Wall of Sound)** — Parallel synchronized wide stereo across all monitors with balanced center fill.
  - `[2]`: **5.1 Spatial Surround Sound** — Discrete channel routing (Center dialogue on middle/top displays, bass on 34" ultrawides, surround wings on outer screens).
  - `[3]`: **7.1 Immersive Surround** — Multi-channel surround for 4+ screen battlestations.
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

## 🏆 Created by JTG Systems

<div align="center">

![JTG Systems Attribution & Tips](assets/jtgsystems-attribution-banner.jpg)

**Engineered with pride by [JTG Systems](https://jtgsystems.com)**  
*Leading computer systems, enterprise networking, and custom workstation architecture.*

🌐 **Website**: [jtgsystems.com](https://jtgsystems.com)  
☕ **Tips & Sponsorship**: `jtgsystems@gmail.com`

</div>

---

## 📜 License

MIT License © 2026 [JTG Systems](https://jtgsystems.com).
