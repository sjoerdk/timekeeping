@echo off
REM 01/10/2013 Sjoerd
REM launchy will not run python script with parameters directly so I need to use this instead

REM parameters 	   ========================================
SET msg=%1
SET time_shift=%2

python write_to_log.py -d googledoc %msg% -t "%time_shift%"
