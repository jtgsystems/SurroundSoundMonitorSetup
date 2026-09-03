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
    
    subparsers.add_parser("list", help="List all detected monitors and HDMI/DP audio sinks")
    subparsers.add_parser("auto", help="Auto-configure monitors to 5.1 surround sound")
    subparsers.add_parser("stereo", help="Activate Unified Wide Stereo profile")
    subparsers.add_parser("surround", help="Activate 5.1 Spatial Surround profile")
    subparsers.add_parser("battle", help="Run 1v1 Audio Battle A/B comparison")
    
    args = parser.parse_args()
    
    if args.command == "list":
        monitors = discover_monitors()
        print(f"Found {len(monitors)} monitor audio endpoints:")
        for m in monitors:
            print(f"  - {m.display_name} -> {m.sink_name}")
    elif args.command == "auto":
        monitors = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, 90)
        SoundProfileManager.create_5_1_surround_profile(sinks, 20)
        save_pipewire_configuration(sinks, "surround_5_1")
        print("✓ Auto-configured 5.1 Surround Sound across all monitor speakers!")
    elif args.command == "stereo":
        monitors = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, 90)
        SoundProfileManager.create_wide_stereo_profile(sinks, 20)
        save_pipewire_configuration(sinks, "stereo")
        print("✓ Activated Unified Wide Stereo profile!")
    elif args.command == "surround":
        monitors = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, 90)
        SoundProfileManager.create_5_1_surround_profile(sinks, 20)
        save_pipewire_configuration(sinks, "surround_5_1")
        print("✓ Activated 5.1 Spatial Surround profile!")
    elif args.command == "battle":
        monitors = discover_monitors()
        sinks = [m.sink_name for m in monitors]
        SoundProfileManager.apply_hardware_volume(sinks, 90)
        run_1v1_battle(sinks)
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
