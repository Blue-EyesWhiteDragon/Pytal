@echo off
echo YOU WILL PROMPTED TWICE FOR ADMIN PRIVILEDGE!
echo PLEASE HIT ENTER TO CONTINUE
pause
"%~dp0/scripts/install_python.bat"
"%~dp0/scripts/install_requirements.bat"
pause