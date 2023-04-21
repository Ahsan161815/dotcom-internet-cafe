pip install pyinstaller
pyinstaller --noconsole --onefile ./dotcom_2.5.py
Echo batch file delete build
@RD /S /Q "./build"
Echo batch file rename
ren dist dotcom_2.5
