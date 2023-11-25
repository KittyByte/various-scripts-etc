import json
import os
import argparse

import aiohttp
import asyncio

from pathlib import Path

parser = argparse.ArgumentParser(prog='Ключи:',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog='Пример использования для одного токена:\n'
                                        'check-ds-token.py -t NTY1Ocs5NTctNDQzDg3tTA0.GF45lL.IzqsUS7ti5uAGic7K9nnF98ibBlPlLgBptgvo\n'
                                        'Для файла с токенами(каждый токен должен начинаться с новой строки и без лишних знаков):\n'
                                        'check-ds-token.py -t C:\\data\\ds_token\\tokens.txt\n'
                                        'Добавьте этот ключ если хотите изменить место вывода\n'
                                        '-o C:\\data\\ds_token\\result.json',
                                 description='Написал glit-hh-ch')

parser.add_argument('-t', '--token', help='Токен дискорда или путь к списку токенов дискорда')
parser.add_argument('-o', '--output', help='Путь вывода результатов')

args = parser.parse_args()

current_path = Path(__file__).parent
path_output = f'{current_path}\\DiscordToken_data.json'
result = []

# ------------- check arguments -------------------------
if args.token is None:
    print('[!] Используйте <python check-ds-token.py -h> для получения информации')
    exit()

check_path = Path(args.token).parent
if os.path.exists(check_path) and str(check_path) != '.':
    if os.path.isfile(args.token):
        with open(args.token, 'r') as f:
            lst_tokens = [i.replace('\n', '') for i in f.readlines()]
    else:
        print('[!] Путь к файлу не действителен')
        exit()
else:
    lst_tokens = [args.token]

if args.output:
    try:
        with open(args.output + '.json', 'w') as f:
            f.write('check path')
            path_output = args.output + '.json'
    except:
        print('[!] Проверьте путь значения -o ключа')
        exit()
# ------------- end check arguments ----------------------


badgeList = [
    {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "Developer "},
    {"Name": 'Bug_Hunter_Level_2',           'Value': 16384,  'Emoji': "Bughunter_2 "},
    {"Name": 'Early_Supporter',              'Value': 512,    'Emoji': "Early_supporter "},
    {"Name": 'House_Balance',                'Value': 256,    'Emoji': "HypeSquad:balance "},
    {"Name": 'House_Brilliance',             'Value': 128,    'Emoji': "HypeSquad:brilliance "},
    {"Name": 'House_Bravery',                'Value': 64,     'Emoji': "HypeSquad:bravery "},
    {"Name": 'Bug_Hunter_Level_1',           'Value': 8,      'Emoji': "Bughunter_1 "},
    {"Name": 'HypeSquad_Events',             'Value': 4,      'Emoji': "hypesquad_events "},
    {"Name": 'Partnered_Server_Owner',       'Value': 2,      'Emoji': "Partner "},
    {"Name": 'Discord_Employee',             'Value': 1,      'Emoji': "Staff "}
]


async def header(token):
    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }


async def GetTokenInfo(token, session):
    async with session.get("https://discordapp.com/api/v6/users/@me", headers=await header(token)) as responce:
        userjson = await responce.json()

    username = userjson["username"]
    hashtag = userjson["discriminator"]
    email = userjson["email"]
    idd = userjson["id"]
    pfp = userjson["avatar"]
    flags = userjson["public_flags"]
    verified = userjson["verified"]
    nitro = ""
    phone = " - "

    if "premium_type" in userjson:
        nitrot = userjson["premium_type"]
        if nitrot == 1:
            nitro = "Нитро классик"
        elif nitrot == 2:
            nitro = "Нитро буст, Нитро классик"
    if "phone" in userjson:
        phone = f'{userjson["phone"]}'

    return username, hashtag, email, idd, pfp, flags, nitro, phone, verified


async def GetBilling(token, session):
    try:
        async with session.get("https://discord.com/api/users/@me/billing/payment-sources", headers=await header(token)) as responce:
            billingjson = await responce.json()

        if not billingjson:
            return " - "

        billing = ""
        for methode in billingjson:
            if not methode["invalid"]:
                if methode["type"] == 1:
                    billing += "Есть карта!"
                elif methode["type"] == 2:
                    billing += ":parking: "

        return billing
    except:
        return False


def GetBadge(flags):
    if flags == 0: return ''

    OwnedBadges = ''
    for badge in badgeList:
        if flags // badge["Value"] != 0:
            OwnedBadges += badge["Emoji"]
            flags = flags % badge["Value"]

    return OwnedBadges


async def GetUHQFriends(token, session):
    try:
        async with session.get("https://discord.com/api/v6/users/@me/relationships", headers=await header(token)) as responce:
            friendlist = await responce.json()

            uhqlist = ''
            for friend in friendlist:
                OwnedBadges = ''
                flags = friend['user']['public_flags']
                for badge in badgeList:
                    if flags // badge["Value"] != 0 and friend['type'] == 1:
                        if not "House" in badge["Name"]:
                            OwnedBadges += badge["Emoji"]
                        flags = flags % badge["Value"]
                if OwnedBadges != '':
                    uhqlist += f"{OwnedBadges} | {friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})\n"
            return uhqlist
    except:
        return False


async def get_info_from_token(token, session):
    global result
    username, hashtag, email, idd, pfp, flags, nitro, phone, verified = await GetTokenInfo(token, session)

    if pfp is None:
        pfp = "https://cdn.discordapp.com/attachments/963114349877162004/992593184251183195/7c8f476123d28d103efe381543274c25.png"
    else:
        pfp = f"https://cdn.discordapp.com/avatars/{idd}/{pfp}"

    billing = await GetBilling(token, session)
    badge = GetBadge(flags)
    friends = await GetUHQFriends(token, session)
    if friends == '':
        friends = "No Rare Friends"
    if not billing:
        badge, phone, billing = "🔒", "🔒", "🔒"
    if nitro == '' and badge == '':
        nitro = " - "

    data = {
        "Token": f"{token}",
        "Username": f"{username}",
        "Hashtag": f"{hashtag}",
        "avater url": f"{pfp}",
        "Email": f"`{email}`",
        "Phone number": f"{phone}",
        "Verified":f'{verified}',
        "Credit card": f"{billing}",
        "HQ Friends": f"{friends}",
        "Badges": f"{nitro}{badge}",
    }

    result.append(data)


def write_data(data):
    with open(path_output, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=4)


async def GetDiscord(token, session):
    try:
        await get_info_from_token(token, session)
        print(f'[+] Токен {token} действителен')
    except:
        print(f'[-] Токен {token} не действителен')


async def get_ds_datas():
    tasks = []
    print('[+] Проверка запущена...')
    async with aiohttp.ClientSession() as session:
        for token in lst_tokens:
            task = asyncio.create_task(GetDiscord(token, session))
            tasks.append(task)

        await asyncio.gather(*tasks)

    write_data(result)
    print(fr'[+] Файл сохранен по пути - {path_output}')


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_ds_datas())
