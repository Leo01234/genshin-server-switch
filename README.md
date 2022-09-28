# genshin-server-switch
原神pc端简易转服脚本，官服与b服互转

适用于3.0版本

## 依赖
- `python3`
- python启动器`py`

## 用法
1. 查看原神安装路径，若为默认路径`C:\Program Files\Genshin Impact`，则跳到第3步
2. 根据安装路径，对`main.py`文件中变量`launcher_config_path`、 `game_config_path`、 `PCGameSDK_path`进行修改
3. 当无原神相关程序运行时，运行`switch.bat`文件，会自动检测当前为哪一个服务器，并作出切换

## 原理
原神3.0版本官服与b服切换只需要变动3个文件：
- 启动器配置文件`C:\Program Files\Genshin Impact\config.ini`
- 游戏配置文件`C:\Program Files\Genshin Impact\Genshin Impact Game\config.ini`
- `PCGameSDK.dll`文件`C:\Program Files\Genshin Impact\Genshin Impact Game\YuanShen_Data\Plugins\PCGameSDK.dll`

若为以下状态：
1. 启动器配置文件，和游戏配置文件中
    - channel=1
    - sub_channel=1
    - cps=mihoyo
2. `PCGameSDK.dll`不存在

则当前是官服；

若为以下状态：
1. 启动器配置文件，和游戏配置文件中
    - channel=14
    - sub_channel=0
    - cps=bilibili
2. `PCGameSDK.dll`存在

则当前是b服

## 注意事项
若出现错误`配置文件或 PCGameSDK.dll 文件异常`，需要先手动检查上述3个文件的状态，使其为官服或b服的状态，后续才可以使用脚本进行快速切换。这是为了防止出现无法事先预知的特殊情况。

## TODO
- 根据注册表检测游戏启动器安装位置
- 检测游戏是否在运行，并且只在未运行时进行服务器切换