import os
import platform

system = platform.system()

if system == "Windows":
    os.system(
        "pyinstaller -F -w "
        "-n checkers "
        "-i .\\assets\\icon.ico "
        "-p .\\src "
        '--hidden-import="PIL._tkinter_finder" '
        ".\\src\\main.py "
        '&& xcopy /Y /I ".\\assets\\" ".\\dist\\assets\\"'
    )
elif system == "Linux":
    os.system(
        "pyinstaller -F -w "
        "-n checkers "
        "-i ./assets/icon.png "
        "-p ./src "
        '--hidden-import="PIL._tkinter_finder" '
        "./src/main.py "
        "&& /bin/cp -rf ./assets ./dist"
    )
