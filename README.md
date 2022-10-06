# genshin-server-switch
原神pc端简易转服脚本，官服与b服互转

适用于3.1版本

## 安装
在[Releases](https://github.com/Leo01234/genshin-server-switch/releases)下载最新版文件，解压到任意位置即可使用。为方便使用可以将`switch.exe`发送到桌面快捷方式。

## 用法
1. 当无原神相关程序运行时，运行`switch.exe`（需要管理员权限）
2. 点击`检查并切换`，当所有文件状态为“官服”时则游戏为官服，当所有文件状态为“b服”时则游戏为b服。

## 原理
原神3.1版本官服与b服切换只需要变动3个文件：
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
若出现错误`配置文件或 PCGameSDK.dll 文件异常, 请手动检查`，需要使用`位置`按钮手动检查上述3个文件的状态，使其为官服或b服的状态，后续才可以进行快速切换。这是为了防止出现无法事先预知的特殊情况。

## TODO
- [x] 根据注册表检测游戏启动器安装位置
- [x] 添加“文件位置”按钮，可打开手动修改
- [ ] 检测游戏是否在运行，并且只在未运行时进行服务器切换
- [x] 打包为可执行文件，摆脱python解释器依赖
- [x] 图形化界面