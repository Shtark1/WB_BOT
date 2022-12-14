from telegram_bot.utils import StatesSaveProducts

# СООБЩЕНИЯ ОТ БОТА
first_stat_message = "Приветствую Вас, "
second_stat_message = "Приветствую вас снова, "

help_message = """ ЛЮБУЮ ИНФОРМАЦИЮ """

subscription_description_message = """ ЛЮБАЯ ИНФОРМАЦИЯ О ПОДПИСКИ """
cancellation_message = """ НАДПИСЬ ЕСЛИ НАЖАЛ ОТМЕНА """
subscription_buy_message =  "Вам выдана подписка!!!"
no_subscription_message = "Купите подписку, для возможности мониторинга цен!!!"
there_is_subscription_message = """Выберите функцию
    Добавить товар для мониторинга цены
    Посмотреть мои товары"""
add_product_message = """ Добавить один товар, нужно вписать артикул товара
Пример: 349358493
Добавить несколько товаров, нужно отроавить Exel документ в котором в столбце A находятся артиклы"""
max_products_sub_message = "По вашей подписке добавлено максимальное количество товаров!!"
add_products_one_message = "Впиши артикул:"
add_products_more_message = "Отправь Exel файл"
there_is_product_message = "Товар добавлен!!!"
update_price_products_message = "Такой товар есть!"
ne_tot_products_message = "Товар не добавлен!!!"
no_such_product_message = "Такого товара нет (("
there_is_exel_message = "Это Exel файл!"
not_exel_message = "Это не Exel файл!"
message_instead_of_file = "Нужно отправить Exel файл, а не сообщение("
no_added_products_messsage = "Нет добавленных товаров"
delete_product_message = "✔️ - оставить товар\n✖️ - удалить товар \n ❌ DEL ❌ - удалить все товары из списка"
delete_all_product_message = "Всё DELETE"

unknown_command_message = "Неизвестная команда пиши /start или /help"

MESSAGES = {
    "start": first_stat_message,
    "second_start": second_stat_message,

    "help": help_message,

    "subscription_description": subscription_description_message,
    "cancellation": cancellation_message,
    "subscription_buy": subscription_buy_message,
    "no_subscription": no_subscription_message,
    "there_is_subscription": there_is_subscription_message,
    "add_product": add_product_message,
    "max_products_sub": max_products_sub_message,
    "add_products_one_message": add_products_one_message,
    "add_products_more_message": add_products_more_message,
    "there_is_product": there_is_product_message,
    "update_price_products": update_price_products_message,
    "ne_tot_products": ne_tot_products_message,
    "no_such_product": no_such_product_message,
    "there_is_exel": there_is_exel_message,
    "not_exel": not_exel_message,
    "message_instead_of_file": message_instead_of_file,
    "no_added_products": no_added_products_messsage,
    "delete_product": delete_product_message,
    "delete_all_product": delete_all_product_message,

    "unknown_command": unknown_command_message,
}

# СООБЩЕНИЯ ПРИ ОПЛАТЕ
name_subscription_1 = ""
name_subscription_2 = ""
name_subscription_3 = ""
name_subscription_4 = ""
price_1 = ''
price_2 = ''
price_3 = ''
price_4 = ''

title_message = "Заголовок"
description_message = "Описание подписки"

MESSAGES_PAY = {
    "name_subscription_1": name_subscription_1,
    "name_subscription_2": name_subscription_2,
    "name_subscription_3": name_subscription_3,
    "name_subscription_4": name_subscription_4,
    "price_1": price_1,
    "price_2": price_2,
    "price_3": price_3,
    "price_4": price_4,

    "title": title_message,
    "description": description_message,
}