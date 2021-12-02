import vlc
import time
import os
import sys

def get_vb_device_string():
    instance = vlc.Instance()
    player = instance.media_player_new()
    mods = player.audio_output_device_enum() 

    device = ""
    if mods:
        mod = mods
        while mod:
            mod = mod.contents
            if "VB" in mod.description.decode():
                device = mod.device
            mod = mod.next

    vlc.libvlc_audio_output_device_list_release(mods)
    return device

def play(src, vol=100):
    instance = vlc.Instance()
    if src.startswith("https://") or os.path.exists(src):
        player = instance.media_player_new(src)
    else:
        print(f"{src} file does not exists or src is not a valid link (starts with https://)")
        sys.exit()
    
    device = get_vb_device_string()
    player.play()
    player.audio_output_device_set(None, device) 
    player.audio_set_volume(vol)
    time.sleep(.2)
    while player.is_playing(): pass
if __name__ == "__main__":
    play("bruhj.mp3", 50)
