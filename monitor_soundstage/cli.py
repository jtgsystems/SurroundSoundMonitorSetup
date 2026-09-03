import argparse
import sys
import subprocess
from .discovery import discover_monitors
from .profiles import SoundProfileManager
from .persist import save_pipewire_configuration
from .tui import interactive_menu, run_1v1_battle

def set_volume(pct: int):
    """Adjust active soundstage master volume."""
    sinks = ["Surround_5_1_Monitors", "All_Monitors"]
    for s in sinks:
        subprocess.run(["pactl", "set-sink-volume", s, f"{pct}%"], capture_output=True)
    print(f"✓ Soundstage master volume set to {pct}%")

def main():
    parser = argparse.ArgumentParser(
        prog="surround-sound-monitor-setup",
        description="Automatic Multi-Monitor Audio Setup & Spatial Soundstage Calibrator for Linux"
    )
    parser.add_argument("-v", "--volume", type=int, default=20, help="Initial master volume percentage (default: 20%%)")
    parser.add_argument("-w", "--hw-volume", type=int, default=90, help="Physical monitor speaker level percentage (default: 90%%)")
    
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("list", help="List all detected monitors, spatial coordinates, and audio sinks")
    
    auto_p = subparsers.add_parser("auto", help="Auto-detect monitor layout and load the optimal sound profile (default: 20%% master)")
    auto_p.add_argument("-v", "--volume", type=int, default=20, help="Master volume percentage (default: 20%%)")
    
    stereo_p = subparsers.add_parser("stereo", help="Activate Unified Wide Stereo profile")
    stereo_p.add_argument("-v", "--volume", type=int, default=20, help="Master volume percentage")
    
    surround_p = subparsers.add_parser("surround", help="Activate 5.1 Spatial Surround profile")
    surround_p.add_argument("-v", "--volume", type=int, default=20, help="Master volume percentage")
    
    vol_p = subparsers.add_parser("volume", help="Set the soundstage master volume to any percentage")
    vol_p.add_argument("percent", type=int, help="Volume percentage (0-100 or higher)")
    
    subparsers.add_parser("battle", help="Run 1v1 Audio Battle A/B comparison")
    
    args = parser.parse_args()
    
    if args.command == "volume":
        set_volume(args.percent)
    elif args.command == "list":
        monitors, optimal_profile = discover_monitors()
        print(f"🔱 Auto-Detected {len(monitors)} Monitor Endpoints (Optimal: {optimal_profile.upper()}):")
        for idx, m in enumerate(monitors, 1):
            print(f"  [{idx}] {m.display_name} @ ({m.pos_x}, {m.pos_y}) -> Role: {m.spatial_role} -> Sink: {m.sink_name}")
    elif args.command == "auto":
        target_vol = getattr(args, "volume", 20)
        monitors, optimal_profile = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, args.hw_volume)
        
        if optimal_profile in ("surround_5_1", "surround_7_1"):
            SoundProfileManager.create_5_1_surround_profile(sinks, target_vol)
            save_pipewire_configuration(sinks, "surround_5_1", target_vol)
            print(f"✓ Auto-detected {len(monitors)}-screen layout: Applied 5.1 Spatial Surround Sound at {target_vol}% volume!")
        else:
            SoundProfileManager.create_wide_stereo_profile(sinks, target_vol)
            save_pipewire_configuration(sinks, "stereo", target_vol)
            print(f"✓ Auto-detected {len(monitors)}-screen layout: Applied Unified Wide Stereo Soundstage at {target_vol}% volume!")
    elif args.command == "stereo":
        target_vol = getattr(args, "volume", 20)
        monitors, _ = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, args.hw_volume)
        SoundProfileManager.create_wide_stereo_profile(sinks, target_vol)
        save_pipewire_configuration(sinks, "stereo", target_vol)
        print(f"✓ Activated Unified Wide Stereo profile at {target_vol}% volume!")
    elif args.command == "surround":
        target_vol = getattr(args, "volume", 20)
        monitors, _ = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, args.hw_volume)
        SoundProfileManager.create_5_1_surround_profile(sinks, target_vol)
        save_pipewire_configuration(sinks, "surround_5_1", target_vol)
        print(f"✓ Activated 5.1 Spatial Surround profile at {target_vol}% volume!")
    elif args.command == "battle":
        monitors, _ = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, args.hw_volume)
        run_1v1_battle(sinks)
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
