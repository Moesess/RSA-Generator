import os
import numpy as np
import random

from pytube import YouTube, Playlist


def dec2bin(number):
    return bin(number).replace("0b", "").zfill(8)


def obtain():
    try:
        # Links and file const
        link = "https://www.youtube.com/watch?v=xS57RWAJfZU&list=PLT0yj5YzlBjF55KYPpnKUStc8froio9_j"
        new_file = 'temp.mp3'
        intsFromFile = []
        mergedByte = []

        # Select random video from playlist
        playlist = Playlist(link)
        yt = YouTube(str(playlist[random.randrange(1, 2229)]))
        video = yt.streams.filter(only_audio=True).first()

        # Download video and save it
        response = video.download()
        os.rename(response, new_file)
        file = open(new_file, "rb")

        # Get bytes
        for i in range(0, 512):
            byte = file.read(1)
            intsFromFile.append(int.from_bytes(byte, "big"))

        # Shuffle bytes and do xor on them
        random.shuffle(intsFromFile)
        for number in intsFromFile:
            temp = dec2bin(number)
            mergedByte.append(1 & (int(temp[-1]) ^ int(temp[-2]) ^ int(temp[-3])))

        num = np.packbits(np.array(mergedByte))

        # Close, delete file and return random number
        file.close()
        os.remove("temp.mp3")
        return num.item(0)
    except IndexError:
        obtain()


rand = obtain() + 127


def get_random(x):
    return os.urandom(rand)
