from setuptools import setup, find_packages

setup(
    name="surround-sound-monitor-setup",
    version="1.0.0",
    description="Turn multi-monitor battlestations into 5.1/7.1 Spatial Surround Sound or Unified Wide Stereo arrays using computer screens as speakers. Automatic PipeWire & PulseAudio calibrator for Linux.",
    author="JTG Systems",
    author_email="jtgsystems@gmail.com",
    url="https://jtgsystems.com",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "numpy>=1.20.0"
    ],
    entry_points={
        "console_scripts": [
            "surround-sound-monitor-setup=monitor_soundstage.cli:main",
            "ssms=monitor_soundstage.cli:main",
            "monitor-soundstage=monitor_soundstage.cli:main",
        ],
    },
)
