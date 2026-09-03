from setuptools import setup, find_packages

setup(
    name="monitor-soundstage",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "numpy>=1.20.0"
    ],
    entry_points={
        "console_scripts": [
            "monitor-soundstage=monitor_soundstage.cli:main",
        ],
    },
)
