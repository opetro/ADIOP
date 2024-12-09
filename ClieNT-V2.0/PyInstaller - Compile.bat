@echo off
set "WorkingPath=C:\Users\User\New York College\Oresti Petro - StylianosAss1\Agile - CyberTool - Code"
set "CompilerFolder=---Compiler Files---"
set "PrimaryPythonFile=CLieNT.py"

cd "%WorkingPath%"

python -m PyInstaller --onefile "%PrimaryPythonFile%" --workpath "%WorkingPath%\%CompilerFolder%\Build" --distpath "%WorkingPath%" --specpath "%WorkingPath%\%CompilerFolder%\Spec"

pause