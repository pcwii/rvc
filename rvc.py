import alsaaudio
import threading
import socket
from time import sleep


audio_mixer = alsaaudio.Mixer()


class NewThread:
    id = 0
    idStop = False
    idThread = threading.Thread


def set_volume_master(new_level):
    current_volume = audio_mixer.getvolume()  # Get the current Volume
    audio_mixer.setvolume(new_level)  # Set the volume to 70%.


