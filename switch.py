import ctypes
import configparser
import os
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == "__main__":
    if is_admin():
        # 各种常量定义
        mihoyo = {'channel': '1', 'sub_channel': '1', 'cps': 'mihoyo'}
        bilibili = {'channel': '14', 'sub_channel': '0', 'cps': 'bilibili'}
        launcher_config_path = r'C:\Program Files\Genshin Impact\config.ini'
        game_config_path = r'C:\Program Files\Genshin Impact\Genshin Impact Game\config.ini'

        PCGameSDK_path = r'C:\Program Files\Genshin Impact\Genshin Impact Game\YuanShen_Data\Plugins\PCGameSDK.dll'
        PCGameSDK_folder, PCGameSDK_name = os.path.split(PCGameSDK_path)
        
        launcher_config = configparser.ConfigParser()
        game_config = configparser.ConfigParser()

        launcher_config.read(launcher_config_path)
        game_config.read(game_config_path)

        # ============= 检查 ============
        if (mihoyo.items() <= launcher_config['launcher'].items() and
            mihoyo.items() <= game_config['General'].items() and
            not os.path.isfile(PCGameSDK_path)):
            # 现在是官服
            old = 'mihoyo'
            print("当前是官服")

        elif (bilibili.items() <= launcher_config['launcher'].items() and
            bilibili.items() <= game_config['General'].items() and
            os.path.isfile(PCGameSDK_path)):
            # 现在是b服
            old = 'bilibili'
            print("当前是b服")

        else:
            print("配置文件或 PCGameSDK.dll 文件异常")
            sys.exit()

        # ============= 变更 ============
        if old == 'mihoyo':
            launcher_config['launcher'].update(bilibili)
            game_config['General'].update(bilibili)

            os.system("copy " + PCGameSDK_name + ' "' + PCGameSDK_folder + '"')
            if not os.path.isfile(PCGameSDK_path):
                print("文件复制错误")
                sys.exit()

        elif old == 'bilibili':

            launcher_config['launcher'].update(mihoyo)
            game_config['General'].update(mihoyo)

            os.remove(PCGameSDK_path)
            if os.path.isfile(PCGameSDK_path):
                print("文件未正常删除")
                sys.exit()

        with open(launcher_config_path, 'w') as configfile:
            launcher_config.write(configfile)
        with open(game_config_path, 'w') as configfile:
            game_config.write(configfile)

        if old == 'mihoyo':
            print("已从官服转为b服")
        elif old == 'bilibili':
            print("已从b服转为官服")

    else:
        print("需要以管理员权限运行")