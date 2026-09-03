# 🔱 SurroundSoundMonitorSetup

<div align="center">

![SurroundSoundMonitorSetup Architecture](assets/monitor-soundstage-5-1.jpg)

**Automatic Multi-Monitor Audio Setup & Spatial Soundstage Calibrator for Linux (PipeWire / PulseAudio / WirePlumber)**

[![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20PipeWire%20%7C%20PulseAudio-purple.svg)]()
[![Created By](https://img.shields.io/badge/Created%20By-JTG%20Systems-gold.svg)](https://jtgsystems.com)

*Turn any multi-monitor computer workstation (2, 3, 4, 5, or 6+ displays) into a cohesive **Spatial Surround Sound (5.1 / 7.1)** or **Unified Wide Stereo (Wall of Sound)** acoustic array in seconds using your screens as speakers.*

</div>

---

## ✨ Features

- 🖥️ **Universal Display & Audio Topology Discovery**: Auto-detects all connected HDMI and DisplayPort audio endpoints across any GPU configuration (NVIDIA, AMD, Intel) and analyzes the physical display coordinates ($X, Y$).
- 🎚️ **Automatic Hardware Level Calibration**: Safely balances individual monitor physical speakers (e.g. 90%) while keeping master volume comfortable (default: 20%, fully customizable).
- 🔊 **Adaptive Multi-Monitor Sound Profiles**:
  - `[1]`: **Unified Wide Stereo (Wall of Sound)** — Synchronizes all monitor speakers in parallel stereo with balanced center fill.
  - `[2]`: **5.1 Spatial Surround Sound** — Discrete channel routing (Center dialogue on middle/top screens, bass on primary displays, surround wings on outer screens).
  - `[3]`: **7.1 Immersive Surround** — Multi-channel surround for 4+ screen battlestations.
- ⚔️ **Interactive 1v1 Audio Battle**: Built-in soundcheck and A/B test suite with synthesized multi-track stems and voice channel checks.
- 🌐 **YouTube Open Source / CC Audio Downloader**: Pulls Creative Commons surround sound reference tests via `yt-dlp`.
- 💾 **One-Click Persistence**: Automatically writes PipeWire drop-ins (`~/.config/pipewire/pipewire-pulse.conf.d/`) and desktop autostart so your audio profile survives reboots.

---

## 🚀 Installation & Quick Start

```bash
# Clone the repository
git clone https://github.com/jtgsystems/SurroundSoundMonitorSetup.git
cd SurroundSoundMonitorSetup

# Install locally
pip install -e .
```

### Run Interactive Menu:
```bash
surround-sound-monitor-setup
# or short alias:
ssms
```

### CLI Quick Commands:
```bash
# Auto-detect any workstation setup and instantly apply the optimal profile
ssms auto

# Set master soundstage volume to any percentage (e.g., 25%)
ssms volume 25

# Switch to Wide Stereo profile
ssms stereo

# Switch to 5.1 Surround profile
ssms surround

# Run 1v1 Audio Comparison Battle
ssms battle

# List detected monitor audio endpoints and assigned spatial roles
ssms list
```

---

## 📐 Universal Spatial Topology Support

`SurroundSoundMonitorSetup` automatically classifies and adapts to any workstation geometry:

### 1. Dual Monitor Setup (2 Displays)
```
[Left Display]              [Right Display]
 (Front-Left)                 (Front-Right)
```

### 2. Triple Monitor Setup (3 Displays)
```
[Left Display]          [Center Display]         [Right Display]
 (Front-Left)           (Center Dialogue)         (Front-Right)
```

### 3. Multi-Monitor Battlestation (4 to 6+ Displays)
```
                                   [Top / Elevated Display]
                                  (Center Height / Dialogue)

                                    [Center / Main Display]
                                     (Center Vocal Anchor)

[Left Display / Wing]                                             [Right Display / Wing]             [Far Wing Display]
 (Front Left + Bass)                                               (Front Right + Bass)             (Rear / Side Surround)
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

## 🔍 Keyword Cloud & Search Index (Tags & Queries)

<details>
<summary><strong>Expand Exhaustive Search Index & Compatibility Keywords</strong></summary>

### 🏷️ Primary Keywords & Search Queries:
`multi monitor audio setup` · `use monitor speakers as surround sound` · `combine all monitor speakers linux` · `play audio through all monitors simultaneously` · `pipewire multi monitor audio` · `pulseaudio combine sinks multiple monitors` · `5.1 surround sound using monitor speakers` · `7.1 surround sound multi display` · `battlestation surround sound without speakers` · `dual monitor audio splitter linux` · `triple monitor surround sound setup` · `5 monitor audio wall of sound` · `simultaneous hdmi audio output linux` · `play sound on two monitors at the same time` · `combine hdmi and displayport audio linux` · `nvidia pro-audio multi hdmi output pipewire` · `wireplumber combine multiple audio sinks` · `spatial audio multi screen battlestation` · `monitor speakers spatial soundstage calibrator` · `linux virtual 5.1 surround sound sink` · `linux virtual 7.1 surround sound sink` · `display sound merger` · `multi screen sound fusion` · `screen surround sound linux` · `jtgsystems surround sound monitor setup` · `ssms audio tool` · `pipewire module-combine-sink automatic configuration`

### 💻 Supported Display Servers & Desktop Environments:
`KDE Plasma 6 Wayland kscreen-doctor audio` · `Hyprland hyprctl monitor audio setup` · `Sway swaymsg audio sink merger` · `GNOME Wayland simultaneous audio output` · `X11 xrandr multi monitor sound synchronization` · `Arch Linux pipewire audio setup` · `Ubuntu Debian Fedora OpenSUSE Linux Mint Pop OS audio soundstage`

### 🎮 Gaming & Workstation Audio Profiles:
`gaming battlestation audio optimization` · `curved ultrawide monitor bass audio routing` · `vertical monitor center dialogue speaker` · `overhead top monitor spatial audio height channel` · `simultaneous sound card combine sinks` · `lossless 48000Hz 24-bit 32-bit float audio fusion` · `zero latency monitor speaker synchronization` · `pipewire loopback spatial matrix` · `virtual surround sound headphones and monitors`

### 🛠️ Hardware & Audio Standards:
`NVIDIA GeForce RTX HDMI DisplayPort Audio` · `AMD Radeon RX RDNA iGPU Display Audio` · `Intel Arc Iris Xe Display Audio` · `Ultrawide Curved Gaming Monitor Built-in Speakers` · `Dual Triple Quad Monitor Audio Synchronization` · `LPCM 5.1 Surround Sound` · `LPCM 7.1 Surround Sound` · `Dolby Digital 5.1 Channel Mapping` · `ALSA ELD EDID Audio Parser`

</details>

---

## 📜 License

MIT License © 2026 [JTG Systems](https://jtgsystems.com).
