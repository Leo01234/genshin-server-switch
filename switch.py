import ctypes
import configparser
import os
import shutil
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def report_callback_exception(self, exc, val, tb):
    messagebox.showerror("Error", message=str(val))


def check():
    global launcher_config
    global game_config

    global launcher_config_status
    global game_config_status
    global PCGameSDK_status

    global old

    launcher_config = configparser.ConfigParser()
    game_config = configparser.ConfigParser()

    launcher_config.read(launcher_config_path)
    game_config.read(game_config_path)

    if mihoyo.items() <= launcher_config['launcher'].items():
        launcher_config_status.set('官服')
    elif bilibili.items() <= launcher_config['launcher'].items():
        launcher_config_status.set('b服')
    else:
        launcher_config_status.set('状态异常')

    if mihoyo.items() <= game_config['General'].items():
        game_config_status.set('官服')
    elif bilibili.items() <= game_config['General'].items():
        game_config_status.set('b服')
    else:
        game_config_status.set('状态异常')

    if not os.path.isfile(PCGameSDK_path):
        PCGameSDK_status.set('官服')
    elif os.path.isfile(PCGameSDK_path):
        PCGameSDK_status.set('b服')
    else:
        PCGameSDK_status.set('状态异常')

    if (launcher_config_status.get() == '官服' and
            game_config_status.get() == '官服' and
            PCGameSDK_status.get() == '官服'):
        old = 'mihoyo'
    elif (launcher_config_status.get() == 'b服' and
          game_config_status.get() == 'b服' and
          PCGameSDK_status.get() == 'b服'):
        old = 'bilibili'
    else:
        old = 'error'
        messagebox.showinfo(message="配置文件或 PCGameSDK.dll 文件异常, 请手动检查")


def check_and_switch():
    check()

    if old == 'mihoyo':
        launcher_config['launcher'].update(bilibili)
        game_config['General'].update(bilibili)

        shutil.copy(PCGameSDK_name, PCGameSDK_folder)
        # os.system("copy " + PCGameSDK_name + ' "' + PCGameSDK_folder + '"')
        if not os.path.isfile(PCGameSDK_path):
            messagebox.showinfo(message="文件复制错误")

    elif old == 'bilibili':
        launcher_config['launcher'].update(mihoyo)
        game_config['General'].update(mihoyo)

        os.remove(PCGameSDK_path)
        if os.path.isfile(PCGameSDK_path):
            messagebox.showinfo(message="文件未正常删除")

    with open(launcher_config_path, 'w') as configfile:
        launcher_config.write(configfile)
    with open(game_config_path, 'w') as configfile:
        game_config.write(configfile)

    check()


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

        old = ''

        # ============= GUI ============
        # override method
        Tk.report_callback_exception = report_callback_exception

        root = Tk()

        launcher_config_status = StringVar()
        game_config_status = StringVar()
        PCGameSDK_status = StringVar()

        check()

        root.title("官服b服转换")

        mainframe = ttk.Frame(root, padding="3 3 3 3")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text="启动器配置文件状态: ").grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="游戏配置文件状态: ").grid(column=1, row=2, sticky=W)
        ttk.Label(mainframe, text="PCGameSDK.dll 文件状态: ").grid(column=1, row=3, sticky=W)

        ttk.Label(mainframe, textvariable=launcher_config_status).grid(column=2, row=1, sticky=E)
        ttk.Label(mainframe, textvariable=game_config_status).grid(column=2, row=2, sticky=E)
        ttk.Label(mainframe, textvariable=PCGameSDK_status).grid(column=2, row=3, sticky=E)

        check_button = ttk.Button(mainframe, text="检查", command=check)
        check_button.grid(column=1, row=4, sticky=W)
        check_and_switch_button = ttk.Button(mainframe, text="检查并切换", command=check_and_switch)
        check_and_switch_button.grid(column=2, row=4, sticky=E)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        check_and_switch_button.focus()

        root.mainloop()

    else:
        messagebox.showinfo(message="需要以管理员权限运行")
