@echo off

set folder=.
set source=./source
set out=%folder%/out
set out_data=%folder%/out/data
set name_space=easyConverter

python ..\easy_to_java.py -source %source% -out %out% -outdata %out_data% -namespace %name_space%

pause
