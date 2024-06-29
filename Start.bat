@echo off

set project_path=%~dp0

cd ../environments/helbimmo_env/scripts
call activate.bat 
call activate.bat

cd %project_path%/HELBImmo

start /B cmd