import librosa
import pygame
import time
import numpy as np
from PrintBeats import PrintBeats

PATH = "Mag mell.mp3"


def main() -> None:
    y, sr = librosa.load(PATH)  # 信号序列，采样率
    onsetEnv = librosa.onset.onset_strength(y, sr=sr)
    bpm = librosa.beat.tempo(onset_envelope=onsetEnv)[0]
    bpm //= 2
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, onset_envelope=onsetEnv, bpm=bpm)  # 节奏（次/分钟），节拍帧序列
    beats_suppressed = suppression(beats, onsetEnv)
    beatsTime = librosa.frames_to_time(beats, sr=sr)  # 帧序列转时间序列
    length = int(librosa.get_duration(filename=PATH))
    pygame.mixer.init()
    pygame.mixer.music.load(PATH)
    printBeats = PrintBeats(beatsTime)
    printBeats.start()
    time.sleep(0.2)
    pygame.mixer.music.play()
    time.sleep(length)


def suppression(beats, onsetEnv):
    beats_suppressed = list(np.array(beats).tolist())
    i = 1
    while i < len(beats) - 1:
        prev = onsetEnv[beats[i - 1]]
        cur = onsetEnv[beats[i]]
        next = onsetEnv[beats[i + 1]]
        if cur < prev or cur < next:
            beats_suppressed[i] = 0
        i += 1
    while 0 in beats_suppressed:
        beats_suppressed.remove(0)
    beats_suppressed = np.array(beats_suppressed)
    return beats_suppressed


main()
