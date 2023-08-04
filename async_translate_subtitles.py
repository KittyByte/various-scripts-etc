import os
from pathlib import Path
import asyncio
import aiohttp


""" переводчик субтитров by glit-hh-ch """

path_to_all_subtitles = r'путь к папке со всеми субтитрами'
save_where_take = 0  # сохранить переведенные субтитры там же где и получены: 0 - да, 1 - нет
source_language = "en"  # текущий язык субтитров
target_language = "ru"  # язык на который надо перевести

path_to_files = []


async def translate(text):
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_language}&tl={target_language}&dt=t&q={text}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
            return result[0][0][0]


async def open_file(path_to_file):
    path_file = Path(path_to_file)
    name_file = path_file.name.replace('en', 'ru')
    print(f"[ + ] Work with - {name_file} | path - {path_to_file}")

    with open(path_to_file, encoding='utf8') as file:
        f = file.readlines()

    for i in range(2, len(f), 4):
        text = f[i].replace('\n', '')
        translated_text = await translate(text)
        f[i] = translated_text+'\n'

    if save_where_take:
        with open(fr'subtitles\{name_file}', 'w', encoding='utf8') as file:
            file.write(''.join(f))
    else:
        with open(fr'{path_file.parent}\{name_file}', 'w', encoding='utf8') as file:
            file.write(''.join(f))

    print("[ + ] Done -", name_file, ' | path -', path_to_file)


async def get_paths():
    for root, dirs, files in os.walk(path_to_all_subtitles):
        files[:] = [i for i in files if i.endswith('srt')]
        if files:
            path_to_files.extend([f'{root}\\{file}' for file in files])

    tasks = []
    for i in path_to_files:
        task = asyncio.create_task(open_file(i))
        tasks.append(task)
    await asyncio.gather(*tasks)


def main():
    if not os.path.exists('subtitles') and save_where_take:
        os.mkdir('subtitles')

    asyncio.run(get_paths())


if __name__ == '__main__':
    main()
