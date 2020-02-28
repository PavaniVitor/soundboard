import pyaudio
import wave
import sys


class Player:
    def __init__(self):
        """ class to wrap pyaudio audio playback """    
        self.CHUNK = 1024
        self.p = pyaudio.PyAudio()

    """ context manager """
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.p.terminate()

    def play(self, wf, device=None):
        """ 
        Play wf file in device
        if no device is specified the audio will be played on default device.
        """
        
        if device is None:
            device = self.p.get_default_output_device_info().get("index")

        wf = wave.open(wf)
        
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        output_device_index=device)
        
        data = wf.readframes(self.CHUNK)

        while data != b'':
            stream.write(data)
            data = wf.readframes(self.CHUNK)
    
        stream.stop_stream()
        stream.close()

"""
usage example

if __name__=="__main__":
    player = Player()
    with player as p:
        p.play("chirp.wav")

"""
