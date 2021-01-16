@echo off

set folder=.
set source=./source
set out=%folder%/out
set out_data=%folder%/out/data
set name_space=easyConverter
set script=../easy_to_java.py

set NEWLINE=^

python -c "import sys%NEWLINE% import os%NEWLINE%sys.path.append(os.path.dirname('%script%')) "

python %script% -source %source% -out %out% -outdata %out_data% -namespace %name_space%

pause