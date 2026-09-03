import subprocess
from typing import List, Dict
from .discovery import MonitorDevice

class SoundProfileManager:
    @staticmethod
    def apply_hardware_volume(sinks: List[str], volume_pct: int = 90):
        """Set physical monitor speaker sink volumes."""
        for sink in sinks:
            subprocess.run(["pactl", "set-sink-volume", sink, f"{volume_pct}%"], capture_output=True)

    @staticmethod
    def create_wide_stereo_profile(sinks: List[str], master_vol_pct: int = 20) -> str:
        """Create and activate Unified Wide Stereo sink."""
        slaves_str = ",".join(sinks)
        sink_name = "All_Monitors"
        
        # Unload existing if present
        subprocess.run(["pactl", "unload-module", "module-combine-sink"], capture_output=True)
        
        cmd = [
            "pactl", "load-module", "module-combine-sink",
            f"sink_name={sink_name}",
            r'sink_properties=device.description="All Monitors (Wide Stereo Soundstage)"',
            f"slaves={slaves_str}"
        ]
        subprocess.run(cmd, capture_output=True)
        subprocess.run(["pactl", "set-default-sink", sink_name], capture_output=True)
        subprocess.run(["pactl", "set-sink-volume", sink_name, f"{master_vol_pct}%"], capture_output=True)
        return sink_name

    @staticmethod
    def create_5_1_surround_profile(sinks: List[str], master_vol_pct: int = 20) -> str:
        """Create and activate 5.1 Spatial Surround sink."""
        slaves_str = ",".join(sinks)
        sink_name = "Surround_5_1_Monitors"
        
        cmd = [
            "pactl", "load-module", "module-combine-sink",
            f"sink_name={sink_name}",
            "channels=6",
            "channel_map=front-left,front-right,front-center,lfe,rear-left,rear-right",
            r'sink_properties=device.description="All Monitors (5.1 Surround Sound)"',
            f"slaves={slaves_str}"
        ]
        subprocess.run(cmd, capture_output=True)
        subprocess.run(["pactl", "set-default-sink", sink_name], capture_output=True)
        subprocess.run(["pactl", "set-sink-volume", sink_name, f"{master_vol_pct}%"], capture_output=True)
        return sink_name

    @staticmethod
    def create_7_1_surround_profile(sinks: List[str], master_vol_pct: int = 20) -> str:
        """Create and activate 7.1 Immersive Surround sink."""
        slaves_str = ",".join(sinks)
        sink_name = "Surround_7_1_Monitors"
        
        cmd = [
            "pactl", "load-module", "module-combine-sink",
            f"sink_name={sink_name}",
            "channels=8",
            "channel_map=front-left,front-right,front-center,lfe,rear-left,rear-right,side-left,side-right",
            r'sink_properties=device.description="All Monitors (7.1 Immersive Surround)"',
            f"slaves={slaves_str}"
        ]
        subprocess.run(cmd, capture_output=True)
        subprocess.run(["pactl", "set-default-sink", sink_name], capture_output=True)
        subprocess.run(["pactl", "set-sink-volume", sink_name, f"{master_vol_pct}%"], capture_output=True)
        return sink_name
