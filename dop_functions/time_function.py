import datetime
import time
import requests

import openpyxl
from openpyxl.worksheet import worksheet

from cfg.database import Database
db = Database('cfg/database')



def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now

    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        dt = dt.replace("days", "дней")
        dt = dt.replace("day", "день")
        return dt

def days_to_secons(days):
    return days * 24 * 60 * 60




async def doc_exel(name):
    i=1
    while True:
        filename = f"file/{name.from_user.id}.xlsx"
        book = openpyxl.load_workbook(filename=filename)
        sheet: worksheet = book["Лист1"]


        art = sheet[f"A{i}"].value

        if art is None:
            break

        try:
            art = int(art)
            price = int(sheet[f"B{i}"].value)
            db.add_info_tovar(art, price, name.from_user.id)
        except:
            # print("Не число или другая ошибка")
            await name.answer(f"Строка {i} не записалась, там ошибка")

        i+=1

async def parse_product_page(nm_id):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://www.wildberries.ru',
        'Referer': 'https://www.wildberries.ru/catalog/13684682/detail.aspx?targetUrl=GP',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    url = f'https://card.wb.ru/cards/detail?spp=38&regions=80,68,64,83,4,38,33,70,82,69,86,30,40,48,1,22,66,31' \
          f'&pricemarginCoeff=1.0&reg=1&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=2,12,7,3,6,22,21,8' \
          f'&sppFixGeo=4&dest=-1059500,-77665,-1099982,-4039467&nm={nm_id}'

    data = requests.get(url, headers=headers).json()
    try:
        sale = data['data']['products'][0]['extended']['clientSale']
    except:
        sale = 0
    return (nm_id, sale)