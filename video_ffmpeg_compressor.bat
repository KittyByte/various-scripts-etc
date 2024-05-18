@echo off
setlocal enabledelayedexpansion

REM Создать выходную папку, если она не существует
set OUTPUT_DIR=compressed_videos
if not exist %OUTPUT_DIR% (mkdir %OUTPUT_DIR%)

REM Пройти через все mp4 файлы в текущей директории
for %%f in (*.mp4) do (
    set "input=%%f"
    set "output=%OUTPUT_DIR%\%%~nf.mp4"
    echo =================================================
    echo Compres: "!input!" and save as: "!output!"
    echo =================================================
    ffmpeg -i "!input!" -c:v libx264 -crf 23 -c:a aac -strict -2 "!output!"

)

echo DONE!
echo =================================================
pause