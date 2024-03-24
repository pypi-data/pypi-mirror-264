import numpy as np
import sounddevice as sd

def beep(frequency, duration):
    
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    sd.play(tone, samplerate=sample_rate)
    sd.wait()
