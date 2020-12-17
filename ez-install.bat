@echo off
echo YOU MAY BE PROMPTED TWICE FOR ADMIN PRIVILEDGE!
echo PLEASE HIT ENTER TO CONTINUE
pause
"%~dp0/bin/install_python.bat"
"%~dp0/bin/install_requirements.bat"
pause