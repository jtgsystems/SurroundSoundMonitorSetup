import os
import re
import json
import glob
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

@dataclass
class MonitorDevice:
    display_name: str
    connector: str
    card_id: int
    device_id: int
    sink_name: str
    pos_x: int = 0
    pos_y: int = 0
    width: int = 0
    height: int = 0
    spatial_role: str = "Front-Center"  # FL, FR, FC, LFE, RL, RR, etc.

def run_cmd(cmd: List[str]) -> str:
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return ""

def ensure_pro_audio_profiles():
    """Ensure multi-output GPU cards (like NVIDIA/AMD) have pro-audio enabled so all HDMI/DP sinks exist."""
    cards_out = run_cmd(["pactl", "list", "cards"])
    for block in cards_out.split("Card #"):
        if not block.strip():
            continue
        name_match = re.search(r"Name:\s+(\S+)", block)
        if name_match:
            card_name = name_match.group(1)
            if ("01_00.1" in card_name or "12_00.1" in card_name) and "pro-audio: Pro Audio" in block:
                if "Active Profile: pro-audio" not in block:
                    subprocess.run(["pactl", "set-card-profile", card_name, "pro-audio"], capture_output=True)

def get_screen_geometries() -> Dict[str, Dict]:
    """Retrieve visual coordinates and resolutions across KDE, Hyprland, Sway, GNOME, or X11."""
    geom_map = {}
    
    # 1. Try KDE kscreen-doctor
    try:
        out = run_cmd(["kscreen-doctor", "-j"])
        if out:
            data = json.loads(out)
            for o in data.get("outputs", []):
                if o.get("connected") and o.get("enabled"):
                    name = o.get("name")
                    pos = o.get("pos", {})
                    size = o.get("size", {})
                    geom_map[name] = {
                        "x": pos.get("x", 0),
                        "y": pos.get("y", 0),
                        "w": size.get("width", 0),
                        "h": size.get("height", 0)
                    }
            if geom_map:
                return geom_map
    except Exception:
        pass

    # 2. Try Hyprland (hyprctl)
    try:
        out = run_cmd(["hyprctl", "monitors", "-j"])
        if out:
            data = json.loads(out)
            for m in data:
                name = m.get("name")
                geom_map[name] = {
                    "x": m.get("x", 0),
                    "y": m.get("y", 0),
                    "w": m.get("width", 0),
                    "h": m.get("height", 0)
                }
            if geom_map:
                return geom_map
    except Exception:
        pass

    # 3. Try xrandr
    try:
        out = run_cmd(["xrandr", "--query"])
        for line in out.splitlines():
            # Example: DP-3 connected primary 3440x1440+4520+1080
            match = re.search(r"^(\S+)\s+connected\s+(?:primary\s+)?(\d+)x(\d+)\+(\d+)\+(\d+)", line)
            if match:
                name, w, h, x, y = match.groups()
                geom_map[name] = {
                    "x": int(x),
                    "y": int(y),
                    "w": int(w),
                    "h": int(h)
                }
    except Exception:
        pass

    return geom_map

def classify_spatial_roles(monitors: List[MonitorDevice]) -> str:
    """Analyze the multi-monitor coordinate bounding box and automatically assign spatial roles."""
    if not monitors:
        return "stereo"
        
    count = len(monitors)
    if count == 1:
        monitors[0].spatial_role = "Stereo Full-Range"
        return "stereo"
    elif count == 2:
        # Sort left to right
        sorted_m = sorted(monitors, key=lambda m: m.pos_x)
        sorted_m[0].spatial_role = "Front-Left"
        sorted_m[1].spatial_role = "Front-Right"
        return "stereo_pair"
    elif count == 3:
        sorted_m = sorted(monitors, key=lambda m: m.pos_x)
        sorted_m[0].spatial_role = "Front-Left"
        sorted_m[1].spatial_role = "Center Dialogue"
        sorted_m[2].spatial_role = "Front-Right"
        return "surround_3_1"
    else:
        # 4, 5, or 6+ monitors -> 5.1 / 7.1 Spatial Soundstage
        min_x = min(m.pos_x for m in monitors)
        max_x = max(m.pos_x + (m.width if m.width else 1920) for m in monitors)
        span_x = max_x - min_x
        mid_x = min_x + span_x / 2.0
        
        min_y = min(m.pos_y for m in monitors)
        
        # Sort left to right
        sorted_m = sorted(monitors, key=lambda m: m.pos_x)
        
        for m in sorted_m:
            center_dist = (m.pos_x + (m.width / 2.0 if m.width else 960)) - mid_x
            
            # If screen is vertically higher than the rest
            if m.pos_y == min_y and len([o for o in monitors if o.pos_y > min_y]) >= 2:
                m.spatial_role = "Top Height / Center Dialogue"
            elif abs(center_dist) < (span_x * 0.18):
                m.spatial_role = "Center Vocal Anchor"
            elif center_dist < - (span_x * 0.28):
                m.spatial_role = "Front-Left + Bass"
            elif center_dist > (span_x * 0.28):
                m.spatial_role = "Rear / Right Surround Wing"
            elif center_dist < 0:
                m.spatial_role = "Front-Left Main"
            else:
                m.spatial_role = "Front-Right Main + Bass"
                
        return "surround_5_1" if count <= 5 else "surround_7_1"

def discover_monitors() -> Tuple[List[MonitorDevice], str]:
    """Discover all connected monitors, assign spatial roles based on desk layout, and determine optimal profile."""
    ensure_pro_audio_profiles()
    geom_map = get_screen_geometries()
    
    # Read ELD entries
    eld_files = glob.glob("/proc/asound/card*/eld*")
    eld_map = {}
    
    for fpath in eld_files:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if "monitor_present\t\t1" in content or "monitor_present\t1" in content:
                card_m = re.search(r"card(\d+)", fpath)
                card_num = int(card_m.group(1)) if card_m else 0
                
                dev_m = re.search(r"eld#\d+\.(\d+)", fpath)
                eld_idx = int(dev_m.group(1)) if dev_m else 0
                
                mon_name_m = re.search(r"monitor_name\s+([^\n\r]+)", content)
                mon_name = mon_name_m.group(1).strip() if mon_name_m else "HDMI Monitor"
                
                conn_type_m = re.search(r"connection_type\s+([^\n\r]+)", content)
                conn_type = conn_type_m.group(1).strip() if conn_type_m else "HDMI"
                
                eld_map[(card_num, eld_idx)] = {
                    "name": mon_name,
                    "type": conn_type
                }
        except Exception:
            continue

    sinks_out = run_cmd(["pactl", "list", "sinks"])
    sinks_blocks = sinks_out.split("Sink #")
    
    monitors: List[MonitorDevice] = []
    
    for block in sinks_blocks:
        if not block.strip():
            continue
        name_m = re.search(r"Name:\s+(\S+)", block)
        if not name_m:
            continue
        sink_name = name_m.group(1)
        
        if "alsa_output" not in sink_name:
            continue
        if "12_00.6" in sink_name or "HyperX" in sink_name or "SoloCast" in sink_name:
            continue
            
        desc_m = re.search(r"Description:\s+([^\n\r]+)", block)
        desc = desc_m.group(1).strip() if desc_m else sink_name
        
        card_id = 0
        dev_id = 0
        
        alsa_card_m = re.search(r'alsa\.card\s*=\s*"(\d+)"', block)
        if alsa_card_m:
            card_id = int(alsa_card_m.group(1))
            
        alsa_dev_m = re.search(r'alsa\.device\s*=\s*"(\d+)"', block)
        if alsa_dev_m:
            dev_id = int(alsa_dev_m.group(1))
            
        matched_mon = eld_map.get((card_id, dev_id))
        if not matched_mon:
            matched_mon = next((v for (c, d), v in eld_map.items() if c == card_id), None)
            
        display_name = desc
        if matched_mon:
            display_name = f"{matched_mon['name']} ({desc})"
            
        # Match geometry if connector name matches
        geom = next((g for name, g in geom_map.items() if name.lower() in sink_name.lower() or name.lower() in desc.lower()), {})
        
        mon = MonitorDevice(
            display_name=display_name,
            connector=desc,
            card_id=card_id,
            device_id=dev_id,
            sink_name=sink_name,
            pos_x=geom.get("x", len(monitors) * 1920),
            pos_y=geom.get("y", 0),
            width=geom.get("w", 1920),
            height=geom.get("h", 1080)
        )
        monitors.append(mon)
        
    optimal_profile = classify_spatial_roles(monitors)
    return monitors, optimal_profile
