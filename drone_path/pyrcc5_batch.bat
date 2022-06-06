@echo off
call "C:\Program Files (x86)\QGIS 3.16\bin\o4w_env.bat"
call "C:\Program Files (x86)\QGIS 3.16\bin\qt5_env.bat"
call "C:\Program Files (x86)\QGIS 3.16\bin\py3_env.bat"

@echo on
pyrcc5 -o resources.py resources.qrc