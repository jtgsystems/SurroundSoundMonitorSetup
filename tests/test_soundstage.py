import unittest
from monitor_soundstage.discovery import discover_monitors
from monitor_soundstage.profiles import SoundProfileManager
from monitor_soundstage.synth import generate_stereo_soundstage_demo, generate_surround_5_1_demo
import os

class TestMonitorSoundstage(unittest.TestCase):
    def test_discovery(self):
        monitors = discover_monitors()
        self.assertIsInstance(monitors, list)
        self.assertGreater(len(monitors), 0)
        
    def test_synth_stereo(self):
        wav = generate_stereo_soundstage_demo(duration=1.0)
        self.assertTrue(os.path.exists(wav))
        self.assertGreater(os.path.getsize(wav), 1000)
        os.remove(wav)

    def test_synth_surround(self):
        wav = generate_surround_5_1_demo(duration=1.0)
        self.assertTrue(os.path.exists(wav))
        self.assertGreater(os.path.getsize(wav), 1000)
        os.remove(wav)

if __name__ == "__main__":
    unittest.main()
