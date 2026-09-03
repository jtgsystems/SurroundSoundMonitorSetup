from setuptools import setup, find_packages

setup(
    name="surround-sound-monitor-setup",
    version="1.0.0",
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
