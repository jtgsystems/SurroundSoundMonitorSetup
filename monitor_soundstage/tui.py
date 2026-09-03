import sys
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from .discovery import discover_monitors
from .profiles import SoundProfileManager
from .synth import (
    generate_voice_intro,
    generate_stereo_soundstage_demo,
    generate_surround_5_1_demo,
    play_audio
)
from .persist import save_pipewire_configuration
from .youtube import CURATED_AUDIO_TRACKS, download_youtube_audio

console = Console()

def render_banner():
    console.print(Panel.fit(
        "[bold cyan]🔱 MONITOR SOUNDSTAGE CALIBRATOR (SOTA 2026)[/bold cyan]\n"
        "[italic white]Auto-Detecting Multi-Monitor Layout & Synthesizing Spatial Soundstage[/italic white]",
        border_style="cyan"
    ))

def display_monitors(monitors, optimal_profile: str):
    table = Table(title=f"[bold green]Auto-Detected Workstation Topology ({len(monitors)} Displays)[/bold green]", border_style="blue")
    table.add_column("No.", style="cyan", justify="center")
    table.add_column("Display / Model", style="bold white")
    table.add_column("Position (X, Y)", style="yellow", justify="center")
    table.add_column("Auto-Assigned Spatial Role", style="bold green")
    table.add_column("Hardware Sink", style="magenta")
    
    for idx, m in enumerate(monitors, 1):
        pos_str = f"({m.pos_x}, {m.pos_y})"
        table.add_row(str(idx), m.display_name, pos_str, m.spatial_role, m.sink_name)
    console.print(table)
    
    profile_names = {
        "stereo": "Stereo Mode",
        "stereo_pair": "Dual-Monitor Expanded Stereo",
        "surround_3_1": "3.1 Front Soundstage",
        "surround_5_1": "5.1 Spatial Surround Sound",
        "surround_7_1": "7.1 Immersive Surround Sound"
    }
    rec_name = profile_names.get(optimal_profile, "5.1 Spatial Surround")
    console.print(Panel(
        f"[bold gold1]🎯 Optimal Detected Profile:[/bold gold1] [bold green]{rec_name}[/bold green]\n"
        f"[dim white]Based on {len(monitors)} detected physical displays and their spatial desk placement.[/dim white]",
        border_style="gold1"
    ))

def run_1v1_battle(sinks):
    console.print("\n[bold yellow]⚔️  STARTING 1v1 AUDIO BATTLE: WIDE STEREO vs 5.1 SURROUND ⚔️[/bold yellow]\n")
    
    intro1 = "/tmp/tui_intro1.wav"
    intro2 = "/tmp/tui_intro2.wav"
    generate_voice_intro("Round One: Unified Wide Stereo across all monitor speakers.", intro1)
    generate_voice_intro("Round Two: Five Point One Spatial Surround Sound.", intro2)
    
    stereo_wav = generate_stereo_soundstage_demo()
    surround_wav = generate_surround_5_1_demo()
    
    # 1. Round 1
    console.print("[bold cyan]>>> [ROUND 1] Playing Wide Stereo (All Monitors Unified)...[/bold cyan]")
    SoundProfileManager.create_wide_stereo_profile(sinks, 20)
    play_audio("All_Monitors", intro1)
    play_audio("All_Monitors", stereo_wav)
    
    console.print("[dim]... Pausing 2 seconds ...[/dim]")
    time.sleep(2)
    
    # 2. Round 2
    console.print("[bold magenta]>>> [ROUND 2] Playing 5.1 Spatial Surround Sound...[/bold magenta]")
    SoundProfileManager.create_5_1_surround_profile(sinks, 20)
    play_audio("Surround_5_1_Monitors", intro2)
    play_audio("Surround_5_1_Monitors", surround_wav)
    
    for p in [intro1, intro2, stereo_wav, surround_wav]:
        if os.path.exists(p): os.remove(p)
        
    console.print("\n[bold green]✓ 1v1 Battle Completed![/bold green]\n")

def interactive_menu():
    render_banner()
    monitors, optimal_profile = discover_monitors()
    
    if not monitors:
        console.print("[bold red]No HDMI/DP monitor audio sinks detected.[/bold red]")
        return
        
    display_monitors(monitors, optimal_profile)
    sinks = [m.sink_name for m in monitors]
    
    # Ensure hardware volumes are at 90%
    SoundProfileManager.apply_hardware_volume(sinks, 90)
    
    while True:
        console.print(Panel(
            "[bold white]Choose an Action / Sound Profile:[/bold white]\n\n"
            "  [bold green][a][/bold green]  [white]Load [bold]Optimal Auto-Detected Profile[/bold] (Recommended)[/white]\n"
            "  [bold cyan][1][/bold cyan]  [white]Activate [bold]Unified Wide Stereo[/bold] (Wall of Sound)[/white]\n"
            "  [bold magenta][2][/bold magenta]  [white]Activate [bold]5.1 Spatial Surround Sound[/bold] (Directional Stems)[/white]\n"
            "  [bold blue][3][/bold blue]  [white]Activate [bold]7.1 Immersive Surround[/bold] (For 4+ Displays)[/white]\n"
            "  [bold yellow][b][/bold yellow]  [white]Play [bold]1v1 Audio Battle[/bold] (A/B Test Stereo vs Surround)[/white]\n"
            "  [bold bright_cyan][y][/bold bright_cyan]  [white]Download & Play [bold]YouTube Open Source / CC Audio[/bold][/white]\n"
            "  [bold red][s][/bold red]  [white]Save Current Profile & Set as [bold]Permanent Default[/bold][/white]\n"
            "  [bold white][q][/bold white]  [dim]Quit[/dim]",
            border_style="bright_blue",
            title="[bold yellow]Menu Controls[/bold yellow]"
        ))
        
        choice = Prompt.ask("[bold cyan]Enter choice[/bold cyan]", default="a").strip().lower()
        
        if choice == "a":
            if optimal_profile == "surround_5_1" or optimal_profile == "surround_7_1":
                console.print("[magenta]Applying Auto-Detected 5.1 Spatial Surround Sound...[/magenta]")
                SoundProfileManager.create_5_1_surround_profile(sinks, 20)
                save_pipewire_configuration(sinks, "surround_5_1")
            else:
                console.print("[cyan]Applying Auto-Detected Wide Stereo Soundstage...[/cyan]")
                SoundProfileManager.create_wide_stereo_profile(sinks, 20)
                save_pipewire_configuration(sinks, "stereo")
            console.print("[bold green]✓ Optimal profile loaded, calibrated at 20% master, and saved![/bold green]")
        elif choice == "1":
            console.print("[green]Activating Unified Wide Stereo (20% Master Volume)...[/green]")
            SoundProfileManager.create_wide_stereo_profile(sinks, 20)
            console.print("[bold green]✓ Wide Stereo is now active![/bold green]")
        elif choice == "2":
            console.print("[magenta]Activating 5.1 Spatial Surround Sound (20% Master Volume)...[/magenta]")
            SoundProfileManager.create_5_1_surround_profile(sinks, 20)
            console.print("[bold magenta]✓ 5.1 Surround Sound is now active![/bold magenta]")
        elif choice == "3":
            console.print("[blue]Activating 7.1 Immersive Surround (20% Master Volume)...[/blue]")
            SoundProfileManager.create_7_1_surround_profile(sinks, 20)
            console.print("[bold blue]✓ 7.1 Surround Sound is now active![/bold blue]")
        elif choice == "b":
            run_1v1_battle(sinks)
        elif choice == "y":
            console.print("\n[bold yellow]Available Royalty-Free / Creative Commons YouTube Audio Tracks:[/bold yellow]")
            for k, item in CURATED_AUDIO_TRACKS.items():
                console.print(f"  [cyan]{k}[/cyan]: [bold white]{item['title']}[/bold white] - [dim]{item['description']}[/dim]")
            yt_ch = Prompt.ask("Select track to download and test (or enter custom YouTube URL)", default="1").strip()
            url = CURATED_AUDIO_TRACKS.get(yt_ch, {}).get("url", yt_ch)
            console.print(f"[cyan]Downloading audio stream with yt-dlp...[/cyan]")
            wav = download_youtube_audio(url)
            if wav:
                console.print(f"[green]Playing {url} through active audio profile...[/green]")
                play_audio("Surround_5_1_Monitors", wav)
                if os.path.exists(wav): os.remove(wav)
            else:
                console.print("[red]Failed to download audio from YouTube. Check URL or connection.[/red]")
        elif choice == "s":
            save_pipewire_configuration(sinks, "surround_5_1")
            console.print("[bold green]✓ Configuration saved to ~/.config/pipewire/ and ~/.config/autostart![/bold green]")
        elif choice == "q":
            console.print("[cyan]Exiting Monitor Soundstage. Enjoy the sound![/cyan]")
            break
