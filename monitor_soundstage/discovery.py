import os
import re
import json
import glob
import subprocess
from dataclasses import dataclass
from typing import List, Dict

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

def run_cmd(cmd: List[str]) -> str:
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return ""

def ensure_pro_audio_profiles():
    """Ensure multi-output GPU cards (like NVIDIA) have pro-audio enabled so all HDMI/DP sinks exist."""
    cards_out = run_cmd(["pactl", "list", "cards"])
    for block in cards_out.split("Card #"):
        if not block.strip():
            continue
        name_match = re.search(r"Name:\s+(\S+)", block)
        if name_match:
            card_name = name_match.group(1)
            # Only enable pro-audio on GPU HDMI audio devices (NVIDIA/AMD GPU)
            if ("01_00.1" in card_name or "12_00.1" in card_name) and "pro-audio: Pro Audio" in block:
                if "Active Profile: pro-audio" not in block:
                    subprocess.run(["pactl", "set-card-profile", card_name, "pro-audio"], capture_output=True)

def get_kscreen_geometries() -> Dict[str, Dict]:
    """Retrieve visual position and resolutions of monitors from kscreen-doctor."""
    geom_map = {}
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
    except Exception:
        pass
    return geom_map

def discover_monitors() -> List[MonitorDevice]:
    """Discover all connected monitors, their ALSA ELD descriptions, PipeWire sinks, and physical layout."""
    ensure_pro_audio_profiles()
    geom_map = get_kscreen_geometries()
    
    # 1. Read ELD entries from /proc/asound/
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

    # 2. Get active sinks from pactl
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
        
        # We only want hardware HDMI / DP ALSA outputs from GPU devices (exclude motherboard analog)
        if "alsa_output" not in sink_name:
            continue
        if "12_00.6" in sink_name or "HyperX" in sink_name:
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
            
        # Match with ELD
        matched_mon = eld_map.get((card_id, dev_id))
        if not matched_mon:
            # Try finding any ELD for this card
            matched_mon = next((v for (c, d), v in eld_map.items() if c == card_id), None)
            
        display_name = desc
        if matched_mon:
            display_name = f"{matched_mon['name']} ({desc})"
            
        mon = MonitorDevice(
            display_name=display_name,
            connector=desc,
            card_id=card_id,
            device_id=dev_id,
            sink_name=sink_name
        )
        monitors.append(mon)
        
    return monitors
