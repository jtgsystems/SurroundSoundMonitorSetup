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
    width: int = 1920
    height: int = 1080
    spatial_role: str = "Front-Center"
    channel_assignment: str = "FC"

def run_cmd(cmd: List[str]) -> str:
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return ""

def ensure_pro_audio_profiles():
    """Ensure multi-output GPU cards have pro-audio enabled so all HDMI/DP audio sinks exist."""
    cards_out = run_cmd(["pactl", "list", "cards"])
    for block in cards_out.split("Card #"):
        if not block.strip():
            continue
        name_match = re.search(r"Name:\s+(\S+)", block)
        if name_match:
            card_name = name_match.group(1)
            # Exclude motherboard analog chipsets
            if "12_00.6" in card_name or "Realtek" in block:
                continue
            has_hdmi = "hdmi" in block.lower() or "displayport" in block.lower() or "video-display" in block.lower()
            if has_hdmi and "pro-audio: Pro Audio" in block:
                if "Active Profile: pro-audio" not in block:
                    subprocess.run(["pactl", "set-card-profile", card_name, "pro-audio"], capture_output=True)

def get_screen_geometries() -> Dict[str, Dict]:
    """Retrieve visual coordinates and resolutions directly from OS display settings across all compositors."""
    geom_map = {}
    
    # 1. KDE Plasma (kscreen-doctor)
    try:
        out = run_cmd(["kscreen-doctor", "-j"])
        if out:
            data = json.loads(out)
            for o in data.get("outputs", []):
                if o.get("connected") and o.get("enabled"):
                    name = o.get("name", "")
                    pos = o.get("pos", {})
                    size = o.get("size", {})
                    geom_map[name] = {
                        "x": pos.get("x", 0),
                        "y": pos.get("y", 0),
                        "w": size.get("width", 1920),
                        "h": size.get("height", 1080),
                        "rotation": o.get("rotation", 1)
                    }
            if geom_map:
                return geom_map
    except Exception:
        pass

    # 2. Hyprland (hyprctl)
    try:
        out = run_cmd(["hyprctl", "monitors", "-j"])
        if out:
            data = json.loads(out)
            for m in data:
                name = m.get("name", "")
                geom_map[name] = {
                    "x": m.get("x", 0),
                    "y": m.get("y", 0),
                    "w": m.get("width", 1920),
                    "h": m.get("height", 1080),
                    "rotation": m.get("transform", 0)
                }
            if geom_map:
                return geom_map
    except Exception:
        pass

    # 3. Sway / wlroots (swaymsg)
    try:
        out = run_cmd(["swaymsg", "-t", "get_outputs", "-r"])
        if out:
            data = json.loads(out)
            for o in data:
                if o.get("active"):
                    name = o.get("name", "")
                    rect = o.get("rect", {})
                    geom_map[name] = {
                        "x": rect.get("x", 0),
                        "y": rect.get("y", 0),
                        "w": rect.get("width", 1920),
                        "h": rect.get("height", 1080),
                        "rotation": 1
                    }
            if geom_map:
                return geom_map
    except Exception:
        pass

    # 4. X11 (xrandr)
    try:
        out = run_cmd(["xrandr", "--query"])
        for line in out.splitlines():
            match = re.search(r"^(\S+)\s+connected\s+(?:primary\s+)?(\d+)x(\d+)\+(\d+)\+(\d+)", line)
            if match:
                name, w, h, x, y = match.groups()
                geom_map[name] = {
                    "x": int(x),
                    "y": int(y),
                    "w": int(w),
                    "h": int(h),
                    "rotation": 1
                }
    except Exception:
        pass

    return geom_map

def solve_2d_spatial_soundstage(monitors: List[MonitorDevice]) -> str:
    """
    2D Spatial Layout Solver:
    Analyzes physical monitor coordinates (X, Y), dimensions, and vertical stacking
    directly from the user's OS display settings to assign optimal surround channels.
    """
    if not monitors:
        return "stereo"
        
    count = len(monitors)
    if count == 1:
        monitors[0].spatial_role = "Stereo Full-Range"
        monitors[0].channel_assignment = "FL+FR"
        return "stereo"
        
    if count == 2:
        sorted_m = sorted(monitors, key=lambda m: m.pos_x)
        sorted_m[0].spatial_role = "Front-Left Display"
        sorted_m[0].channel_assignment = "FL"
        sorted_m[1].spatial_role = "Front-Right Display"
        sorted_m[1].channel_assignment = "FR"
        return "stereo_pair"
        
    if count == 3:
        sorted_m = sorted(monitors, key=lambda m: m.pos_x)
        min_y = min(m.pos_y for m in monitors)
        top_monitors = [m for m in monitors if m.pos_y == min_y]
        
        if len(top_monitors) == 1 and min(m.pos_y for m in monitors if m != top_monitors[0]) > min_y + 300:
            top_monitors[0].spatial_role = "Top Stacked / Height Dialogue"
            top_monitors[0].channel_assignment = "FC"
            bottoms = sorted([m for m in monitors if m != top_monitors[0]], key=lambda m: m.pos_x)
            bottoms[0].spatial_role = "Front-Left Display"
            bottoms[0].channel_assignment = "FL"
            bottoms[1].spatial_role = "Front-Right Display"
            bottoms[1].channel_assignment = "FR"
        else:
            sorted_m[0].spatial_role = "Front-Left Display"
            sorted_m[0].channel_assignment = "FL"
            sorted_m[1].spatial_role = "Center Dialogue"
            sorted_m[1].channel_assignment = "FC"
            sorted_m[2].spatial_role = "Front-Right Display"
            sorted_m[2].channel_assignment = "FR"
        return "surround_3_1"

    # Multi-Monitor Layout (4, 5, 6+ Displays)
    min_x = min(m.pos_x for m in monitors)
    max_x = max(m.pos_x + m.width for m in monitors)
    span_x = max(max_x - min_x, 1)
    mid_x = min_x + span_x / 2.0
    
    min_y = min(m.pos_y for m in monitors)
    max_y = max(m.pos_y + m.height for m in monitors)
    
    y_coords = sorted(set(m.pos_y for m in monitors))
    is_vertically_stacked = len(y_coords) > 1 and (y_coords[1] - y_coords[0] >= 300)
    
    for m in monitors:
        center_x = m.pos_x + m.width / 2.0
        dist_from_mid_x = center_x - mid_x
        norm_x = dist_from_mid_x / (span_x / 2.0)
        
        # 1. Stacking: If screen is on top row above bottom displays
        if is_vertically_stacked and m.pos_y == min_y:
            m.spatial_role = "Top Stacked / Height Dialogue"
            m.channel_assignment = "FC"
        # 2. Center Column: Within middle 25% of horizontal space
        elif abs(norm_x) < 0.25:
            m.spatial_role = "Center Vocal Anchor"
            m.channel_assignment = "FC"
        # 3. Far Left Wing
        elif norm_x <= -0.55:
            m.spatial_role = "Left Wing / Surround Left"
            m.channel_assignment = "RL"
        # 4. Front Left Main
        elif norm_x < 0:
            m.spatial_role = "Front-Left Main + Bass"
            m.channel_assignment = "FL+LFE"
        # 5. Far Right Wing
        elif norm_x >= 0.55:
            m.spatial_role = "Right Wing / Surround Right"
            m.channel_assignment = "RR"
        # 6. Front Right Main
        else:
            m.spatial_role = "Front-Right Main + Bass"
            m.channel_assignment = "FR+LFE"
            
    return "surround_5_1" if count <= 5 else "surround_7_1"

def discover_monitors() -> Tuple[List[MonitorDevice], str]:
    """Discover all connected monitors, parse exact settings geometry, and assign spatial soundstage roles."""
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
                mon_name = mon_name_m.group(1).strip() if mon_name_m else "Display Audio"
                
                conn_type_m = re.search(r"connection_type\s+([^\n\r]+)", content)
                conn_type = conn_type_m.group(1).strip() if conn_type_m else "HDMI/DP"
                
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
        
        # Only include hardware HDMI / DisplayPort video display audio sinks
        if "alsa_output" not in sink_name:
            continue
            
        desc_m = re.search(r"Description:\s+([^\n\r]+)", block)
        desc = desc_m.group(1).strip() if desc_m else sink_name
        
        # Exclude internal analog soundcards, USB microphones, headsets, and webcams
        desc_lower = desc.lower()
        if any(w in desc_lower for w in ["analog", "mic", "headset", "headphone", "usb audio", "hyperx", "solocast", "realtek"]):
            continue
        if "12_00.6" in sink_name:
            continue
            
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
            
        geom_keys = list(geom_map.keys())
        geom = {}
        for k in geom_keys:
            if k.lower() in sink_name.lower() or k.lower() in desc.lower():
                geom = geom_map[k]
                break
                
        if not geom and len(monitors) < len(geom_keys):
            geom = geom_map[geom_keys[len(monitors)]]
            
        pos_x = geom.get("x", len(monitors) * 1920)
        pos_y = geom.get("y", 0)
        w = geom.get("w", 1920)
        h = geom.get("h", 1080)
        
        mon = MonitorDevice(
            display_name=display_name,
            connector=desc,
            card_id=card_id,
            device_id=dev_id,
            sink_name=sink_name,
            pos_x=pos_x,
            pos_y=pos_y,
            width=w,
            height=h
        )
        monitors.append(mon)
        
    optimal_profile = solve_2d_spatial_soundstage(monitors)
    return monitors, optimal_profile
