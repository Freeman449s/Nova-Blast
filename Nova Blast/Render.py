import random, time, math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Particle import Particle
from PIL import Image
from Player import Player
import Global, MusicAnalysis


def renderFrame(pGeneSpeed: float) -> None:
    """
    真正绘制图形的函数\n
    :param pGeneSpeed: 生成粒子的速度（每帧生成粒子的个数）
    :return: 无返回值
    """
    # 每20毫秒：更新粒子位置，删除不可见粒子，并生成新粒子
    if time.time() - Global.lastUpdateTime >= 0.02:
        Global.nParticlesToRender += pGeneSpeed
        Global.lastUpdateTime = time.time()
        for p in Global.particles:
            p.updateMovement()
            if p.position.z > 0:
                Global.particles.remove(p)
        # 生成新粒子
        while Global.nParticlesToRender > 1:
            x = random.random() * 5
            y = random.random() * 5
            z = -150
            vz = 0.5
            theta = random.randint(0, 359)
            rad = theta / 360 * 2 * math.pi
            if Global.forceSim != Global.ForceType.NONE:
                basicSpeed = 0.03  # 开启力学模拟时，基础速度需要略微降低，避免运动过快
            else:
                basicSpeed = 0.05
            vx = basicSpeed * math.sin(rad)
            vy = basicSpeed * math.cos(rad)
            if Global.bSpeedUp:  # 加速状态下，新生成粒子也需加速
                vx *= Global.speedUpRatio_particle
                vy *= Global.speedUpRatio_particle
                vz *= Global.speedUpRatio_particle
            Global.particles.append(Particle(0.5, x, y, z, vx, vy, vz, random.randint(1, len(Global.darkTextureIDs))))
            Global.nParticlesToRender -= 1
    # 绘制
    for p in Global.particles:
        drawParticle(p, 16)


def speedUp() -> None:
    """
    调整所有粒子的速度使它们加速\n
    :return: 无返回值
    """
    for p in Global.particles:
        p.vx = p.vx * Global.speedUpRatio_particle
        p.vy = p.vy * Global.speedUpRatio_particle
        p.vz = p.vz * Global.speedUpRatio_particle


def slowDown() -> None:
    """
    调整所有粒子的速度使它们恢复原来的速度\n
    :return: 无返回值
    """
    for p in Global.particles:
        p.vx = p.vx / Global.speedUpRatio_particle
        p.vy = p.vy / Global.speedUpRatio_particle
        p.vz = p.vz / Global.speedUpRatio_particle


def drawParticle(p: Particle, fineness: int) -> None:
    """
    绘制粒子\n
    :param p: 粒子对象
    :param fineness: 分几段绘制圆形
    :return: 无返回值
    """
    glEnable(GL_TEXTURE_2D)
    if Global.bSpeedUp:
        glBindTexture(GL_TEXTURE_2D, p.darkTextureID + len(Global.darkTextureIDs))  # 加速时使用亮色
    else:
        glBindTexture(GL_TEXTURE_2D, p.darkTextureID)
    # glBegin(GL_QUADS)
    # glTexCoord2d(0, 0)
    # glVertex3d(p.x - p.r / 2, p.y - p.r / 2, p.z)
    # glTexCoord2d(0, 1)
    # glVertex3d(p.x - p.r / 2, p.y + p.r / 2, p.z)
    # glTexCoord2d(1, 1)
    # glVertex3d(p.x + p.r / 2, p.y + p.r / 2, p.z)
    # glTexCoord2d(1, 0)
    # glVertex3d(p.x + p.r / 2, p.y - p.r / 2, p.z)
    glBegin(GL_POLYGON)
    for i in range(0, fineness):
        rad = i / fineness * 2 * math.pi
        cos = math.cos(rad)
        sin = math.sin(rad)
        glTexCoord2d(0.5 + 0.5 * cos, 0.5 + 0.5 * sin)
        if Global.bSpeedUp:
            glVertex3d(p.position.x + p.r * cos * Global.scaleRatio, p.position.y + p.r * sin * Global.scaleRatio,
                       p.position.z)
        else:
            glVertex3d(p.position.x + p.r * cos, p.position.y + p.r * sin, p.position.z)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def redraw() -> None:
    """
    绘制每帧时调用\n
    :return: 无返回值
    """

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()  # 重置模型视景矩阵

    eye = [0, 0, 1]  # 相机所处位置
    center = [0, 0, 0]  # 相机朝向
    if Global.bSpeedUp:
        Global.camUpRad += Global.rotateSpeed * Global.speedUpRatio_rotate
    else:
        Global.camUpRad += Global.rotateSpeed
    gluLookAt(eye[0], eye[1], eye[2],
              center[0], center[1], center[2],
              math.cos(Global.camUpRad), math.sin(Global.camUpRad), 0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    # 确定是否加速
    if time.time() - Global.nextBeatTime > 0:
        Global.lastBeatTime = Global.nextBeatTime
        if len(Global.beatsTime) > 0:  # 列表中尚存在节拍时间，更新下次节拍时间
            Global.nextBeatTime = Global.beatsTime[0] + Global.playStartTime
            Global.beatsTime.pop(0)
        else:  # 不再加速
            Global.nextBeatTime = 1e38
        # speedUp()
        Global.bSpeedUp = True
    if time.time() - Global.lastBeatTime > Global.speedUpDuration:
        # if bSpeedUp:  # 只在加速状态时减速，避免重复减速
        #     slowDown()
        Global.bSpeedUp = False
    if Global.forceSim == Global.ForceType.NONE:
        basicPGeneSpeed = 0.5  # 基础粒子产生速度
    else:
        basicPGeneSpeed = 0.4  # 出于性能考虑，粒子产生速度略微下调
    if Global.bSpeedUp:
        renderFrame(basicPGeneSpeed * Global.speedUpRatio_num)
    else:
        renderFrame(basicPGeneSpeed)

    glutSwapBuffers()


def init() -> None:
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(1280, 720)
    glutCreateWindow("Nova Blast")
    readTexture()
    glutDisplayFunc(redraw)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)

    Global.lastUpdateTime = time.time()
    Global.beatsTime = MusicAnalysis.analyzeMusic()
    Global.nextBeatTime = Global.beatsTime[0]
    Global.beatsTime.pop(0)

    Global.c.acquire()
    p = Player("Music/Mag mell.mp3")
    p.start()  # 开启音乐播放线程
    Global.c.wait()  # 等待音乐准备完毕

    glutMainLoop()


def idle() -> None:
    """
    空闲回调函数，不存在未完成的任务时，会不停调用此函数\n
    :return: 无返回值
    """
    glutPostRedisplay()  # 在完成图形绘制操作后，要调用此函数来重绘图形，否则只有在相应鼠标或键盘消息时进行绘制


def readTexture() -> None:
    """
    读取纹理\n
    :return: 无返回值
    """
    texture = Image.open("Alpha/Light Blue.jpg")
    height, width = texture.size
    data = texture.tobytes("raw", "RGBX", 0, -1)
    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, Global.lightTextureIDs[0])
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    setTextureParameters()

    texture = Image.open("Alpha/Light Cyan.jpg")
    height, width = texture.size
    data = texture.tobytes("raw", "RGBX", 0, -1)
    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, Global.lightTextureIDs[1])
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    setTextureParameters()

    texture = Image.open("Alpha/Light Green.jpg")
    height, width = texture.size
    data = texture.tobytes("raw", "RGBX", 0, -1)
    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, Global.lightTextureIDs[2])
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    setTextureParameters()

    texture = Image.open("Alpha/Light Purple.jpg")
    height, width = texture.size
    data = texture.tobytes("raw", "RGBX", 0, -1)
    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, Global.lightTextureIDs[3])
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    setTextureParameters()

    texture = Image.open("Alpha/Dark Blue.jpg")
    height, width = texture.size
    data = texture.tobytes("raw", "RGBX", 0, -1)
    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, Global.darkTextureIDs[0])
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    setTextureParameters()

    texture = Image.open("Alpha/Dark Cyan.jpg")
    height, width = texture.size
    data = texture.tobytes("raw", "RGBX", 0, -1)
    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, Global.darkTextureIDs[1])
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    setTextureParameters()

    texture = Image.open("Alpha/Dark Green.jpg")
    height, width = texture.size
    data = texture.tobytes("raw", "RGBX", 0, -1)
    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, Global.darkTextureIDs[2])
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    setTextureParameters()

    texture = Image.open("Alpha/Dark Purple.jpg")
    height, width = texture.size
    data = texture.tobytes("raw", "RGBX", 0, -1)
    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, Global.darkTextureIDs[3])
    glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    setTextureParameters()

    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)


def reshape(width: int, height: int) -> None:
    """
    窗口尺寸变化时调用的函数\n
    :param width: 窗口宽度
    :param height: 窗口高度
    :return: 无返回值
    """
    if height == 0:
        height = 1  # 避免除0

    glViewport(0, 0, width, height)  # 设置视口。视口是显示区域，可能比窗口大也可能比窗口小。

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # 重置投影矩阵
    gluPerspective(45.0, width / height, 0.1, 200.0)  # 计算宽高比

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()  # 重置模型视景矩阵


def setTextureParameters() -> None:
    """
    将纹理属性设置为默认值，避免代码重复\n
    :return: 无返回值
    """
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
