"""
定义全局变量
"""
import math
from threading import Condition
from enum import Enum


class ForceType(Enum):
    """
    指明模拟何种力的枚举类
    """
    NONE = 0  # 不开启力学模拟
    ELECTROSTATIC_REPULSION = 1  # 静电斥力
    SPRING = 2  # 弹簧力


PATH = "Music/Mag mell.mp3"
particles = []  # 粒子列表
camUpRad = math.pi / 2  # 相机上方向
lastUpdateTime = 0
lastSpeedUpTime = 0
rotateSpeed = 0.005  # 基础旋转速度
nextBeatTime = 0  # 下一次节拍时间（绝对值）
lastBeatTime = 0  # 上一次节拍时间（绝对值）
beatsTime = []  # 节拍时间（相对值）
playStartTime = 0  # 开始播放时间（绝对值）
speedUpRatio_particle = 2.5  # 加速时，粒子速度为原来的多少倍
speedUpRatio_rotate = 3  # 加速时，镜头旋转速度为原来的多少倍
speedUpRatio_num = 2.5  # 加速时，例子生成速度为原来的多少倍
bSpeedUp = False  # 是否处于加速状态
darkTextureIDs = [1, 2, 3, 4]  # 暗纹理索引
lightTextureIDs = [5, 6, 7, 8]  # 亮纹理索引
speedUpDuration = 0.3  # 加速时长
c = Condition()  # 条件对象，用于线程协作
nParticlesToRender = 0  # 待绘制粒子数，当待绘制粒子数大于1时，绘制一个新粒子。用于控制粒子生成速度
forceSim = ForceType.NONE  # 力学模拟类别
scaleRatio = 1.4  # 加速情况下粒子的缩放比例
usingChinese = False
sensitivity = 4  # 节拍检测敏感度
