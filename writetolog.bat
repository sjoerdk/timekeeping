@echo off
REM 11:16 AM 2/19/2013 Sjoerd
REM awesome batch file time tracking
REM Usage: in console type 'writetolog.bat "a message"' to write message with current date/time to logfile

REM parameters 	   ========================================
SET msg=%1
SET logFile=".\timing.log"
REM end parameters ========================================

REM get current date
SET fulldate=%date%
SET MM=%fulldate:~4,2%
SET DD=%fulldate:~7,2%
SET YYYY=%fulldate:~10,4%
SET TODAY=%YYYY%%MM%%DD%

REM output your action and write to log
echo %TODAY% %time% - writing %msg% 
echo %TODAY% %time% - %msg% >> %logfile%
