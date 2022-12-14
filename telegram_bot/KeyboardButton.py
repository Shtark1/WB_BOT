from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# КНОПКИ МЕНЮ
btn_profile = KeyboardButton("Профиль")
btn_subscription = KeyboardButton("Подписка")
btn_products = KeyboardButton("Товары")

# КНОПКИ ПОДПИСКИ
btn_type_of_subscription1 = InlineKeyboardButton(text="Месяц - 150р", callback_data="1")
btn_type_of_subscription2 = InlineKeyboardButton(text="2 Месяцa - 300р", callback_data="2")
btn_type_of_subscription3 = InlineKeyboardButton(text="3 Месяцев - 450р", callback_data="3")
btn_type_of_subscription4 = InlineKeyboardButton(text="6 Месяцев - 900р", callback_data="4")
btn_cancellation = InlineKeyboardButton('✖️ Отмена ✖️', callback_data="cancellation")

# ДОБАВЛЕНИЕ / ПРОСМОТР ТОВАРОВ
btn_add_products = InlineKeyboardButton(text="Добавить товар", callback_data="add_products")
btn_views_produts = InlineKeyboardButton(text="Посмотреть добавленнные", callback_data="views_products")

# ДОБАВЛЕНИЕ ТОВАРА
btn_add_products_one = InlineKeyboardButton(text="Добавить один", callback_data="add_products_one")
btn_add_products_more = InlineKeyboardButton(text="Добавить несколько", callback_data="add_products_more")

# УДАЛИТЬ / ОСТАВИТ ДОБАВЛЕННЫЙ ТОВАР
btn_save_add_products = InlineKeyboardButton(text="✔️", callback_data="save_products")
btn_delete_add_products = InlineKeyboardButton(text="✖️", callback_data="delete_products")

# УДАЛИТЬ ВСЕ ТОВАРЫ
btn_delete_all_products = InlineKeyboardButton(text="❌ DEL ❌", callback_data="delete_all_products")

# ТОТ ТОВАР ИЛИ НЕТ
btn_tot_products = InlineKeyboardButton(text="✔️ Да ✔️", callback_data="tot_products")
btn_ne_tot_products = InlineKeyboardButton(text="✖️ Нет ✖️", callback_data="ne_tot_products")

BUTTON_TYPES = {
    "BTN_HOME": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_profile, btn_subscription).add(btn_products),
    "BTN_SUBSCRIPTIONS_PRICE": InlineKeyboardMarkup().add(btn_type_of_subscription1, btn_type_of_subscription2).add(
        btn_type_of_subscription3, btn_type_of_subscription4).add(btn_cancellation),

    'help': "",
    "BTN_CANCELLATION": InlineKeyboardMarkup().add(btn_cancellation),
    "BTN_ADD_VIEWS": InlineKeyboardMarkup().add(btn_add_products, btn_views_produts).add(btn_cancellation),
    "BTN_ADD_PRODUCTS": InlineKeyboardMarkup().add(btn_add_products_one, btn_add_products_more).add(btn_cancellation),
    "BTN_VIEWS_PRODUCTS": InlineKeyboardMarkup().add(btn_save_add_products, btn_delete_add_products),
    "BTN_DELETE_ALL_PRODUCTS": InlineKeyboardMarkup().add(btn_delete_all_products).add(btn_cancellation),
    "BTN_TOT_OR_NO": InlineKeyboardMarkup().add(btn_tot_products, btn_ne_tot_products),
}