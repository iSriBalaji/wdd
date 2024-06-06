import sounddevice as sd
import numpy as np

def measure_noise_level(duration=1, sample_rate=44100, num_measurements=5):
    noise_levels = []
    # spl = 20*log10(Prms/Pref)
    for i in range(num_measurements):
        print(f"Recording Sample...{i}")
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()
        print("Recording complete.\n")
        # Calculate root mean square (RMS) to measure noise level
        rms = np.sqrt(np.mean(audio_data**2))
        # Calculate noise level in decibels (dB)
        noise_level_db = 20 * np.log10(rms / (20e-6))
        noise_levels.append(noise_level_db)
    
    avg_noise_level_db = np.mean(noise_levels)
    return avg_noise_level_db

if __name__ == "__main__":
    noise_level = measure_noise_level(num_measurements=5)
    print(f"Noise level: {noise_level:.2f} dB")
