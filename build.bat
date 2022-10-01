call .\venv\Scripts\activate.bat
pyinstaller -w --uac-admin --noconfirm .\switch.py
call .\venv\Scripts\deactivate.bat

copy PCGameSDK.dll .\dist\switch
pause