import pyaudio
import wave
import sys


class Player:
    """ class to wrap pyaudio audio playback """    
    
    def __init__(self):
        self.CHUNK = 1024
        self.pyaudio_instance = pyaudio.PyAudio()

    """ context manager """
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.pyaudio_instance.terminate()

    def play(self, wave_file_path, device=None):
        """ 
        Play wave_file located in wave_file_path
        if no device is specified the audio will be played on default device.
        """
        
        if device is None:
            device = self.pyaudio_instance.get_default_output_device_info().get("index")

        wave_file = wave.open(wave_file_path)
        
        stream = self.pyaudio_instance.open(format=self.pyaudio_instance.get_format_from_width(wave_file.getsampwidth()),
                        channels=wave_file.getnchannels(),
                        rate=wave_file.getframerate(),
                        output=True,
                        output_device_index=device)
        
        data = wave_file.readframes(self.CHUNK)
        while data:
            stream.write(data)
            data = wave_file.readframes(self.CHUNK)
    
        stream.stop_stream()
        stream.close()

"""
usage example
    with player as p:
        p.play("chirp.wav")
"""

