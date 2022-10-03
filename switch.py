import ctypes
import configparser
import os
import shutil
import winreg
import subprocess
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
    else:
        PCGameSDK_status.set('b服')
    # elif os.path.isfile(PCGameSDK_path):
    #     PCGameSDK_status.set('b服')
    # else:
    #     PCGameSDK_status.set('状态异常')

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

    if old == 'error':
        return

    elif old == 'mihoyo':
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


def get_launcher_install_path():
    registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                  r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\原神',
                                  0, winreg.KEY_READ)
    value, regtype = winreg.QueryValueEx(registry_key, 'InstallPath')
    winreg.CloseKey(registry_key)
    return value


def open_launcher_config_in_explorer():
    subprocess.Popen(r'explorer /select,"' + launcher_config_path + '"')


def open_game_config_in_explorer():
    subprocess.Popen(r'explorer /select,"' + game_config_path + '"')


def open_PCGameSDK_in_explorer():
    if PCGameSDK_status.get() == '官服':
        subprocess.Popen(r'explorer "' + PCGameSDK_folder + '"')
    elif PCGameSDK_status.get() == 'b服':
        subprocess.Popen(r'explorer /select,"' + PCGameSDK_path + '"')


if __name__ == "__main__":
    if is_admin():
        # 各种常量定义
        mihoyo = {'channel': '1', 'sub_channel': '1', 'cps': 'mihoyo'}
        bilibili = {'channel': '14', 'sub_channel': '0', 'cps': 'bilibili'}

        launcher_config = configparser.ConfigParser()
        game_config = configparser.ConfigParser()

        launcher_config_path = get_launcher_install_path() + r'\config.ini'
        launcher_config.read(launcher_config_path)
        game_install_path = launcher_config['launcher']['game_install_path']
        game_config_path = game_install_path.replace('/', '\\') + r'\config.ini'

        PCGameSDK_path = game_install_path.replace('/', '\\') + r'\YuanShen_Data\Plugins\PCGameSDK.dll'
        PCGameSDK_folder, PCGameSDK_name = os.path.split(PCGameSDK_path)

        old = ''

        # ============= GUI ============
        # adapt high dpi display
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

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

        ttk.Label(mainframe, text="启动器配置文件").grid(column=0, row=1, sticky=W)
        ttk.Label(mainframe, text="游戏配置文件").grid(column=0, row=2, sticky=W)
        ttk.Label(mainframe, text="PCGameSDK.dll 文件").grid(column=0, row=3, sticky=W)

        ttk.Label(mainframe, text="打开文件位置").grid(column=1, row=0, sticky=(W, E))
        ttk.Label(mainframe, text="状态").grid(column=2, row=0, sticky=E)

        ttk.Button(mainframe, text="位置", command=open_launcher_config_in_explorer).grid(column=1, row=1, sticky=(W, E))
        ttk.Button(mainframe, text="位置", command=open_game_config_in_explorer).grid(column=1, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="位置", command=open_PCGameSDK_in_explorer).grid(column=1, row=3, sticky=(W, E))

        ttk.Label(mainframe, textvariable=launcher_config_status).grid(column=2, row=1, sticky=E)
        ttk.Label(mainframe, textvariable=game_config_status).grid(column=2, row=2, sticky=E)
        ttk.Label(mainframe, textvariable=PCGameSDK_status).grid(column=2, row=3, sticky=E)

        check_button = ttk.Button(mainframe, text="检查", command=check)
        check_button.grid(column=0, row=4, sticky=W)
        check_and_switch_button = ttk.Button(mainframe, text="检查并切换", command=check_and_switch)
        check_and_switch_button.grid(column=2, row=4, sticky=E)

        mainframe.columnconfigure((0, 1, 2), weight=1)
        mainframe.rowconfigure((0, 1, 2, 3, 4), weight=1)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        check_and_switch_button.focus()

        # 居中窗口
        # get screen width and height
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen
        w = ws / 5  # width for the Tk root
        h = hs / 4  # height for the Tk root

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.mainloop()

    else:
        messagebox.showinfo(message="需要以管理员权限运行")
