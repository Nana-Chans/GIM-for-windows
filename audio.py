
from pygame import mixer
from time import sleep, time
from deef import *
from fractions import Fraction

#    C  D  E  F  G  A  B
# 3 26 28 30 31 33 35 37
# 4 38 40 42 43 45 47 49
# 5 50 52 54 55 57 59 61

mixer.init()
mixer.set_num_channels(100)  # 最大通道数设置为100

c3 = mixer.Sound('audio/26.wav')
d3 = mixer.Sound('audio/28.wav')
e3 = mixer.Sound('audio/30.wav')
f3 = mixer.Sound('audio/31.wav')
g3 = mixer.Sound('audio/33.wav')
a3 = mixer.Sound('audio/35.wav')
b3 = mixer.Sound('audio/37.wav')

c4 = mixer.Sound('audio/38.wav')
d4 = mixer.Sound('audio/40.wav')
e4 = mixer.Sound('audio/42.wav')
f4 = mixer.Sound('audio/43.wav')
g4 = mixer.Sound('audio/45.wav')
a4 = mixer.Sound('audio/47.wav')
b4 = mixer.Sound('audio/49.wav')

c5 = mixer.Sound('audio/50.wav')
d5 = mixer.Sound('audio/52.wav')
e5 = mixer.Sound('audio/54.wav')
f5 = mixer.Sound('audio/55.wav')
g5 = mixer.Sound('audio/57.wav')
a5 = mixer.Sound('audio/59.wav')
b5 = mixer.Sound('audio/61.wav')

abc = ['z', 'x', 'c', 'v', 'b', 'n', 'm',
       'a', 's', 'd', 'f', 'g', 'h', 'j',
       'q', 'w', 'e', 'r', 't', 'y', 'u']
sound = [c3, d3, e3, f3, g3, a3, b3,
         c4, d4, e4, f4, g4, a4, b4,
         c5, d5, e5, f5, g5, a5, b5]


class Audio:
    def __init__(self):

        self.pause = False

    def listen(self, k, t, type, tick=0):
        print(self.pause)
        print(k)
        print(t)
        i = 0
        while t[i] < tick:  # 定位播放位置
            i += 1
        print(i)
        t0 = time() - tick
        while i < len(k):  # 从指定位置开始播放
            #print(self.pause)

            for ii in k[i]:
                if type == 'sound':
                    sound[abc.index(ii)].play()
            while time() - t0 < t[i]:  # 等待时间
                sleep(0.005)
                'True'
            for ii in k[i]:
                if type == 'sound':
                    sound[abc.index(ii)].fadeout(667)
            i += 1
