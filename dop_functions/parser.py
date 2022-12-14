import requests

# Получаем адрес типа https://basket-01.wb.ru/
def get_basket(article):
    # //basket-05.wb.ru/vol981/part98157/98157706/images/big/1.jpg
    vol = int(article / 100000)
    part = int(article / 1000)
    if 0 <= vol <= 143:
        basket = f'https://basket-01.wb.ru/vol{vol}/part{part}/{article}'
    elif 144 <= vol <= 287:
        basket = f'https://basket-02.wb.ru/vol{vol}/part{part}/{article}'
    elif 288 <= vol <= 431:
        basket = f'https://basket-03.wb.ru/vol{vol}/part{part}/{article}'
    elif 432 <= vol <= 719:
        basket = f'https://basket-04.wb.ru/vol{vol}/part{part}/{article}'
    elif 720 <= vol <= 1007:
        basket = f'https://basket-05.wb.ru/vol{vol}/part{part}/{article}'
    elif 1008 <= vol <= 1061:
        basket = f'https://basket-06.wb.ru/vol{vol}/part{part}/{article}'
    elif 1062 <= vol <= 1115:
        basket = f'https://basket-07.wb.ru/vol{vol}/part{part}/{article}'
    elif 1116 <= vol <= 1169:
        basket = f'https://basket-08.wb.ru/vol{vol}/part{part}/{article}'
    elif 1170 <= vol <= 1313:
        basket = f'https://basket-09.wb.ru/vol{vol}/part{part}/{article}'
    elif 1314 <= vol <= 1601:
        basket = f'https://basket-10.wb.ru/vol{vol}/part{part}/{article}'
    else:
        basket = f'https://basket-11.wb.ru/vol{vol}/part{part}/{article}'

    return basket


# Собираем карточку товара
async def parse(article):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'origin': 'https://www.wildberries.ru',
        'referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search={query}&xsearch=true',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.159 Safari/537.36',
    }
    path = get_basket(article)
    # Картинка
    img = f'{path}/images/big/1.jpg'

    url = f'https://card.wb.ru/cards/detail?spp=34&regions=80,64,83,4,38,33,70,82,69,68,86,75,30,40,48,1,22,66,31,71' \
          f'&pricemarginCoeff=1.0&reg=1&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=12,3,18,15,21' \
          f'&sppFixGeo=4&dest=-1029256,-102269,-2162196,-1257484&nm={article}'
    data = requests.get(url, headers=headers).json()

    title = data['data']['products'][0]['name']

    price = str(int(data['data']['products'][0]['priceU'] / 100))

    product_url = f'https://www.wildberries.ru/catalog/{article}/detail.aspx'

    # Цена со скидкой
    try:
        sale = int(data['data']['products'][0]['extended']['basicPriceU'] / 100)
    except:
        sale = int(data['data']['products'][0]['salePriceU'] / 100)

    # Цена со скидкой постоянного покупателя
    try:
        client_sale = str(int(data['data']['products'][0]['extended']['clientSale']))  # Если есть скидка СПП %
        sale_spp = str(int(data['data']['products'][0]['extended']['clientPriceU'] / 100))
    except:
        client_sale = 0
        sale_spp = 0

    return [img, price, sale, client_sale, sale_spp, title, product_url]
