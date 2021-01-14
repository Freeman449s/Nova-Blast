import Global, librosa, numpy as np, soundfile
from warnings import filterwarnings

filterwarnings("ignore")  # 忽略PySoundFile警告


def analyzeMusic() -> list:
    """
    分析音乐的节拍时间\n
    :return: 节拍时间序列
    """
    print("Analyzing music...", end="")
    y, sr = librosa.load(Global.PATH)  # 返回值：信号序列，采样率
    onsetEnv = librosa.onset.onset_strength(y, sr=sr)  # 返回值：帧强度
    bpm = librosa.beat.tempo(onset_envelope=onsetEnv)[0]
    bpm = bpm
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, onset_envelope=onsetEnv, bpm=bpm)  # 返回值：节奏（次/分钟），节拍帧序列
    suppressed = suppress(onsetEnv, beats.tolist())
    beatsTime = librosa.frames_to_time(suppressed, sr=sr).tolist()  # 帧序列转时间序列
    beatsTime = shift(beatsTime, -0.08)  # 节拍点略微前移，增强视觉效果
    print("OK")
    return beatsTime


def suppress(onsetEnv: np.ndarray, beats: list) -> list:
    """
    节拍抑制，只保留一定比例的最强节拍\n
    :param onsetEnv: 所有帧的能量
    :param beats: 节拍帧向量
    :return:
    """
    envAtBeats = []
    for i in range(0, len(beats)):
        envAtBeats.append(onsetEnv[beats[i]])
    T = sorted(envAtBeats)[int(len(envAtBeats) / Global.sensitivity)]
    ret = beats[:]
    index = 0
    while index < len(ret):
        if onsetEnv[ret[index]] < T:
            ret.pop(index)
            index -= 1
        index += 1
    return ret


def shift(beatsTime: list, duration: float) -> list:
    """
    节拍时间平移一个常量，增强视觉效果\n
    :param beatsTime: 节拍时间序列
    :param duration: 平移量
    :return: 平移后的节拍时间序列
    """
    ret = []
    for i in range(0, len(beatsTime)):
        this = beatsTime[i] + duration
        if this < 0:
            this = 0
        ret.append(this)
    return ret
