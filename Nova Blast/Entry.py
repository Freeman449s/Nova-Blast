"""
交互相关
"""
import sys, os
import Global, Render

CONFIG_FILE_PATH = "Configs/configs.cfg"
ENCODING = "UTF-8"


def main():
    print("(C)2021, Gordon Freeman")
    print("Nova Blast")
    print("Powered by OpenGL and librosa")
    if not importConfigs():
        specifyLanguage()
    mainMenu()


def importConfigs() -> bool:
    """
    尝试读取配置文件\n
    :return: 成功读取配置文件返回True，否则返回False
    """
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r", encoding=ENCODING) as file:
            line = file.readline().strip()
            Global.usingChinese = bool(line.split(" ")[-1])
            line = file.readline().strip()
            forceType = line.split(" ")[-1]
            if forceType == "ForceType.ELECTROSTATIC_REPULSION":
                Global.forceSim = Global.ForceType.ELECTROSTATIC_REPULSION
            elif forceType == "ForceType.SPRING":
                Global.forceSim = Global.ForceType.SPRING
            else:
                Global.forceSim = Global.ForceType.NONE
            line = file.readline().strip()
            Global.sensitivity = float(line.split(" ")[-1])
            return True
    else:
        return False


def specifyLanguage() -> None:
    """
    选择语言\n
    :return: 无返回值
    """
    print("Specify your language:")
    print("1. English")
    print("2. 中文")
    choice = input(" > ")
    try:
        choice = int(choice)
    except ValueError:
        print("Input " + choice + " is not valid.")
        writeConfigs()
        sys.exit(0)
    if choice == 1:
        Global.usingChinese = False
    else:
        Global.usingChinese = True
    settings()


def mainMenu() -> None:
    """
    主选单\n
    :return: 无返回值
    """
    if Global.usingChinese:
        print("1. 开始")
        print("2. 设置")
        choice = input(" > ")
        try:
            choice = int(choice)
        except ValueError:
            print("警告：无法将 " + choice + " 转为整数。")
            writeConfigs()
            sys.exit(0)
    else:
        print("1. Start!")
        print("2. Settings")
        choice = input(" > ")
        try:
            choice = int(choice)
        except ValueError:
            print("Warning: Cannot convert " + choice + " to integer.")
            writeConfigs()
            sys.exit(0)
    if choice == 1:
        selectSong()
    else:
        settings()


def selectSong() -> None:
    """
    选择歌曲\n
    :return: 无返回值
    """
    if Global.usingChinese:
        print("输入音乐文件的路径：")
        path = input(" > ")
        if not os.path.exists(path):
            print("警告：文件 " + path + " 不存在，请检查路径并重试。")
            writeConfigs()
            sys.exit(0)
    else:
        print("Input file path:")
        path = input(" > ")
        if not os.path.exists(path):
            print("Warning: file " + path + " does not exist, please check your input and try again.")
            writeConfigs()
            sys.exit(0)
    Global.PATH = path
    Render.init()


def settings() -> None:
    """
    系统设置\n
    :return: 无返回值
    """
    if Global.usingChinese:
        print("节奏检测敏感度[1~10范围内的整数]：")
        sensitivity = input(" > ")
        print("力学模拟类型：")
        print("（开启力学模拟可以得到更加自然的动画效果，但性能可能有所下降）")
        print("1. 仅模拟静电斥力")
        print("2. 模拟弹簧力")
        print("3. 不开启力学模拟")
        forceType = input(" > ")
        try:
            sensitivity = int(sensitivity)
        except ValueError:
            print("警告：无法将 " + sensitivity + " 转为整数。")
            writeConfigs()
            sys.exit(0)
        else:
            if sensitivity >= 2 and sensitivity <= 10:
                Global.sensitivity = sensitivity
            elif sensitivity == 1:
                Global.sensitivity = 1.25
            else:
                Global.sensitivity = 4
        try:
            forceType = int(forceType)
        except ValueError:
            print("警告：无法将 " + forceType + " 转为整数。")
            writeConfigs()
            sys.exit(0)
        else:
            if forceType == 1:
                Global.forceSim = Global.ForceType.ELECTROSTATIC_REPULSION
            elif forceType == 2:
                Global.forceSim = Global.ForceType.SPRING
            else:
                Global.forceSim = Global.ForceType.NONE
    else:
        print("Beats detection sensitivity (an integer in range [1~10]):")
        sensitivity = input(" > ")
        print("Mechanical simulation type:")
        print("(Mechanical simulation yields a more natural animation effect, but the performance may be degraded.)")
        print("1. Electrostatic repulsion only")
        print("2. Spring force")
        print("3. Disable mechanical simulation")
        forceType = input(" > ")
        try:
            sensitivity = int(sensitivity)
        except ValueError:
            print("Warning: Cannot convert " + sensitivity + " to integer.")
            writeConfigs()
            sys.exit(0)
        else:
            if sensitivity > 0 and sensitivity <= 10:
                Global.sensitivity = sensitivity
            else:
                Global.sensitivity = 4
        try:
            forceType = int(forceType)
        except ValueError:
            print("Warning: Cannot convert " + forceType + " to integer.")
            writeConfigs()
            sys.exit(0)
        else:
            if forceType == 1:
                Global.forceSim = Global.ForceType.ELECTROSTATIC_REPULSION
            elif forceType == 2:
                Global.forceSim = Global.ForceType.SPRING
            else:
                Global.forceSim = Global.ForceType.NONE
    writeConfigs()
    selectSong()


def writeConfigs() -> None:
    """
    保存配置文件\n
    :return: 无返回值
    """
    if not os.path.exists("Configs"):
        os.mkdir("Configs")
    with open(CONFIG_FILE_PATH, "w+", encoding=ENCODING) as file:
        file.write("Using Chinese: " + str(Global.usingChinese) + "\n")
        file.write("Force Type: " + str(Global.forceSim) + "\n")
        file.write("Sensitivity: " + str(Global.sensitivity) + "\n")


main()
