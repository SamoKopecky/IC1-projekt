@echo off
pyinstaller --onefile ..\exploit\exploit.py
pyinstaller --onefile ..\virtual_cmd\server_side.py
pyinstaller --onefile ..\virtual_cmd\client_side.py
pyinstaller --onefile ..\virtual_cmd\communication\CertificateAuthority.py