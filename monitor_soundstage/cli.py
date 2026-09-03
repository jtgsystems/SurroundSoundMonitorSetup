import argparse
import sys
from .discovery import discover_monitors
from .profiles import SoundProfileManager
from .persist import save_pipewire_configuration
from .tui import interactive_menu, run_1v1_battle

def main():
    parser = argparse.ArgumentParser(
        prog="monitor-soundstage",
        description="Automatic Multi-Monitor Audio Setup & Spatial Soundstage Calibrator for Linux"
    )
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("list", help="List all detected monitors, spatial coordinates, and audio sinks")
    subparsers.add_parser("auto", help="Auto-detect monitor layout and load the optimal sound profile")
    subparsers.add_parser("stereo", help="Activate Unified Wide Stereo profile")
    subparsers.add_parser("surround", help="Activate 5.1 Spatial Surround profile")
    subparsers.add_parser("battle", help="Run 1v1 Audio Battle A/B comparison")
    
    args = parser.parse_args()
    
    if args.command == "list":
        monitors, optimal_profile = discover_monitors()
        print(f"🔱 Auto-Detected {len(monitors)} Monitor Endpoints (Optimal: {optimal_profile.upper()}):")
        for idx, m in enumerate(monitors, 1):
            print(f"  [{idx}] {m.display_name} @ ({m.pos_x}, {m.pos_y}) -> Role: {m.spatial_role} -> Sink: {m.sink_name}")
    elif args.command == "auto":
        monitors, optimal_profile = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, 90)
        
        if optimal_profile in ("surround_5_1", "surround_7_1"):
            SoundProfileManager.create_5_1_surround_profile(sinks, 20)
            save_pipewire_configuration(sinks, "surround_5_1")
            print(f"✓ Auto-detected {len(monitors)}-screen layout: Applied 5.1 Spatial Surround Sound!")
        else:
            SoundProfileManager.create_wide_stereo_profile(sinks, 20)
            save_pipewire_configuration(sinks, "stereo")
            print(f"✓ Auto-detected {len(monitors)}-screen layout: Applied Unified Wide Stereo Soundstage!")
    elif args.command == "stereo":
        monitors, _ = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, 90)
        SoundProfileManager.create_wide_stereo_profile(sinks, 20)
        save_pipewire_configuration(sinks, "stereo")
        print("✓ Activated Unified Wide Stereo profile!")
    elif args.command == "surround":
        monitors, _ = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, 90)
        SoundProfileManager.create_5_1_surround_profile(sinks, 20)
        save_pipewire_configuration(sinks, "surround_5_1")
        print("✓ Activated 5.1 Spatial Surround profile!")
    elif args.command == "battle":
        monitors, _ = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, 90)
        run_1v1_battle(sinks)
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
