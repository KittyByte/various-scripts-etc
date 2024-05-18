# Набор различных скритов для жизни

- async_translate_subtitles.py - используйте для быстрого перевода субтитров (настройки внутри файла)
- --

- video_ffmpeg_compressor.bat - простой скрипт для сжатся всех видео в папке (настройки внутри файла)
  > **Использование**
  > - Скачать ffmpeg.exe (ссылка: https://www.gyan.dev/ffmpeg/builds/ файл называется ffmpeg-git-full.7z прямая ссылка: [тык](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z))
  > - Откройте архив и вытащите ffmpeg.exe из папки bin
  > - После перенесите скрипт и ffmpeg.exe в туже папку что и все видео которые вы хотите сжать и запустите скрипт
  > - После запуска программы будет создана папка, в которой будут храниться все ваши сжимаемые видео.

- --
- check-ds-token.py - чекер дискорд токенов
  > **Использование**
  > - перед первым запуском пропишите: pip install aiohttp pathlib argparse asyncio json requests
  > - теперь пропишите check-ds-token.py -h и вы получите инструкцию по использованию
   
  > **краткое описание:**
  > - check-ds-token.py -t <ТОКЕН или ПУТЬ К СПИСКУ ТОКЕНОВ(каждый токен должен начинаться с новой строки и без лишних знаков)>
  > - check-ds-token.py -t Jx34NNgtCIN4huH -o <путь вывода результатов(по умолчанию в той же директории где находиться скрипт)>

  > **Пример вывода:**
   ```
   [
      {
          "Token": "NTY1OTc5NTczNgQzODg3MTA0.GF45lL.IzqsUShti5uAGic7K9nzFj8iIbBlPlLgBptgvo",
          "Username": "Alma",
          "Hashtag": "alma_palm",
          "avater url": "https://cdn.discordapp.com/attachments/963114349877162004/992593184251183195/7c8f476123d28d103efe381543274c25.png",
          "Email": "`lolo2345lolo@gmail.com`",
          "Phone number": "+16102458472",
          "Verified": "True",
          "Credit card": " - ",
          "HQ Friends": "No Rare Friends",
          "Badges": "HypeSquad:bravery "
      },
      и т.д.
   ]
   ```
- --


   
