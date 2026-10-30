@echo off
rem version is defined in version.py
for /f %%v in ('python -c "import version; print(version.VERSION)"') do set "version=%%v"
echo Building version %version%
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
pyinstaller --icon=bestarcade.ico --clean --collect-all ttkbootstrap -F BestArcade.py
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
copy ..\data\*.properties .\dist\data
if not exist .\dist\data\images mkdir .\dist\data\images
copy ..\data\images\*.png .\dist\data\images
copy ..\data\images\*.gif .\dist\data\images
if not exist .\dist\data\retroarch mkdir .\dist\data\retroarch
copy ..\data\retroarch\*.csv .\dist\data\retroarch
if not exist .\dist\conf mkdir .\dist\conf
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
