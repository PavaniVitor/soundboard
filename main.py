from player import Player
from threading import Thread
import configparser


def auto_detect(player):
    """
    auto detect VB-Cable device index
    """
    for i in range(player.get_device_count()):
        a = player.get_device_info_by_index(i)

        if a.get("name") == "CABLE Input (VB-Audio Virtual C":
            return a.get("index")

def load_binds():
    pass

def main():
    player = Player()
    vb_ind = auto_detect(player.p)
    with player as p:
        Thread(p.play("chirp.wav"))
        Thread(p.play("chirp.wav",device=vb_ind))
    

if __name__ == "__main__":
    main()