@echo off
pyinstaller ..\exploit\exploit.py
pyinstaller ..\virtual_cmd\server_side.py
pyinstaller ..\virtual_cmd\client_side.py
pyinstaller ..\virtual_cmd\communication\CA.py