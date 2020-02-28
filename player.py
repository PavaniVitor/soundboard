import pyaudio
import wave
import sys


class Player:
    """ class to wrap pyaudio audio playback """
    pyaudio_instance = pyaudio.PyAudio()
    CHUNK = 1024

    @staticmethod
    def play(wave_file_path, device=None):
        """ 
        Play wave_file located in wave_file_path
        if no device is specified the audio will be played on default device.
        """
        
        if device is None:
            device = Player.pyaudio_instance.get_default_output_device_info()["index"]

        wave_file = wave.open(wave_file_path)
        
        stream = Player.pyaudio_instance.open(format=Player.pyaudio_instance.get_format_from_width(wave_file.getsampwidth()),
                        channels=wave_file.getnchannels(),
                        rate=wave_file.getframerate(),
                        output=True,
                        output_device_index=device)
       
        data = wave_file.readframes(Player.CHUNK)
        while data:
            stream.write(data)
            data = wave_file.readframes(Player.CHUNK)
        
        stream.stop_stream()
        stream.close()