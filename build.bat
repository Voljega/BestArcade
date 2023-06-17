@echo off
set /p "version=Version number: "
echo .
echo Clean build directory content
rd /s /q .\build
if exist .\build rd /s /q .\build
if not exist .\build mkdir .\build
cd build
echo Copy build files
copy ..\*.py .
copy ..\*.ico .
echo .
echo .
echo Build with pyinstaller
echo .
pyinstaller --icon=bestarcade.ico --clean -F BestArcade.py
echo .
echo Pyinstaller has ended its work
echo .
echo Clean build directory
del *.py
move *.ico .\dist
del *.spec
rd /s /q .\build
if exist .\build rd /s /q .\build
echo Moving conf files
if not exist .\dist\data mkdir .\dist\data
copy ..\data\*.ini .\dist\data
copy ..\data\*.dat .\dist\data
if not exist .\dist\data\images mkdir .\dist\data\images
copy ..\data\images\*.png .\dist\data\images
if not exist .\dist\data\n2 mkdir .\dist\data\n2
copy ..\data\n2\*.csv .\dist\data\n2
if not exist .\dist\data\n100 mkdir .\dist\data\n100
copy ..\data\n100\*.csv .\dist\data\n100
if not exist .\dist\data\pi3 mkdir .\dist\data\pi3
copy ..\data\pi3\*.csv .\dist\data\pi3
if not exist .\dist\conf mkdir .\dist\conf
copy ..\conf\*.conf .\dist\conf
if not exist .\dist\GUI mkdir .\dist\GUI
copy ..\GUI\*.* .\dist\GUI
copy ..\*.md .\dist
copy ..\*.sh .\dist
echo .
echo Rename exec and dir
ren .\dist\BestArcade.exe BestArcade-%version%.exe
ren .\dist BestArcade-%version%
cd ..
echo Finished building version %version%
