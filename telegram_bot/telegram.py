import logging
import os
import time
import re

from aiogram import Bot
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, ContentTypes
from aiogram import types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types.message import ContentType


from telegram_bot.utils import StatesSaveProducts
from content_text.messages import MESSAGES, MESSAGES_PAY
from telegram_bot.KeyboardButton import BUTTON_TYPES

from cfg.cfg import TOKEN, YOOPAYMENT
from cfg.database import Database
from dop_functions.time_function import time_sub_day, days_to_secons, doc_exel, parse_product_page


db = Database('cfg/database')

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())


# ===================================================
# =============== Стандартные команды ===============
# ===================================================
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
        await message.answer(f"{MESSAGES['start']} {message.from_user.first_name}", reply_markup=BUTTON_TYPES["BTN_HOME"])
    else:
        await message.answer(f"{MESSAGES['second_start']} {message.from_user.first_name}", reply_markup=BUTTON_TYPES["BTN_HOME"])



@dp.message_handler(commands=['help'])
async def help_command(message: Message):
    await message.answer(MESSAGES['help'])


# ===================================================
# ===================== Buttons =====================
# ===================================================
@dp.message_handler(lambda message: message.text.lower() == 'профиль')
async def profile_info(message: Message):
    user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
    if not user_sub:
        user_sub = "Подписки нет!!!"

    await message.answer(f"Ваш ник: {message.from_user.username} \n Подписка: {user_sub}")


@dp.message_handler(lambda message: message.text.lower() == 'подписка')
async def types_of_subscriptions(message: Message):
    await message.answer(MESSAGES["subscription_description"], reply_markup=BUTTON_TYPES["BTN_SUBSCRIPTIONS_PRICE"])


@dp.message_handler(lambda message: message.text.lower() == 'товары')
async def product_btn(message: Message):
    if db.get_sub_status(message.from_user.id):
        await bot.send_message(message.from_user.id, MESSAGES["there_is_subscription"], reply_markup=BUTTON_TYPES["BTN_ADD_VIEWS"])
    else:
        await bot.send_message(message.from_user.id, MESSAGES["no_subscription"])


# ===================================================
# ================= Покупка подписки ================
# ===================================================
@dp.callback_query_handler(lambda c: c.data == "1" or c.data == "2" or c.data == "3" or c.data == "4")
async def buy_subscriptions(callback: CallbackQuery):
    label = "Описание"
    amount = "Цена"
    payload = ""

    if callback.data == "1":
        label = "Месяц"
        amount = 15000
        payload = "month_sub"
    if callback.data == "2":
        label = "2 Месяцa"
        amount = 30000
        payload = "month_sub_2"
    if callback.data == "3":
        label = "3 Месяцев"
        amount = 45000
        payload = "month_sub_3"
    if callback.data == "4":
        label = "6 Месяцев"
        amount = 90000
        payload = "month_sub_6"

    PRICE = types.LabeledPrice(label=label, amount=amount)
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=MESSAGES_PAY["title"],
        description=MESSAGES_PAY["description"],
        provider_token=YOOPAYMENT,
        currency='RUB',
        prices=[PRICE],
        start_parameter='time-machine-example',
        payload=payload,
    )

@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)



@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: Message):

    user_sub_proverka = time_sub_day(db.get_time_sub(message.from_user.id))
    if user_sub_proverka == False:
        user_sub = 0
    else:
        user_sub = int(db.get_time_sub(message.from_user.id)) - time.time()

    days_sub_buy = 0

    if message.successful_payment.invoice_payload == "month_sub":
        days_sub_buy = 30
    if message.successful_payment.invoice_payload == "month_sub_2":
        days_sub_buy = 60
    if message.successful_payment.invoice_payload == "month_sub_3":
        days_sub_buy = 90
    if message.successful_payment.invoice_payload == "month_sub_6":
        days_sub_buy = 180

    time_sub = int(time.time()) + days_to_secons(days_sub_buy) + user_sub
    db.set_time_sub(message.from_user.id, time_sub)

    await bot.send_message(message.from_user.id, MESSAGES["subscription_buy"])



# ===================================================
# ================= Добавление Товара ===============
# ===================================================
@dp.callback_query_handler(lambda c: c.data == "add_products")
async def type_of_add(callback: CallbackQuery):
    await callback.message.edit_text(MESSAGES["add_product"])
    await callback.message.edit_reply_markup(reply_markup=BUTTON_TYPES["BTN_ADD_PRODUCTS"])


# ================= Добавление одного ===============
@dp.callback_query_handler(lambda c: c.data == "add_products_one")
async def data_add_one(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(MESSAGES["add_products_one_message"])

    state = dp.current_state(user=callback.from_user.id)
    await state.set_state(StatesSaveProducts.all()[1])



@dp.message_handler(state=StatesSaveProducts.STATE_ADD_ONE)
async def add_one(message: Message):
    try:
        art = int(re.sub(r" \d+", "", message.text))
        price = int(re.sub(r'\d+ ', '', message.text))

        db.add_info_tovar(art, price, message.from_user.id)
        # Здесь добавь функцию получения цены
        #
        await message.answer(f'{MESSAGES["there_is_product"]} ', reply_markup=BUTTON_TYPES["BTN_HOME"])

    except:
        await message.answer(MESSAGES["no_such_product"], reply_markup=BUTTON_TYPES["BTN_HOME"])

    state = dp.current_state(user=message.from_user.id)
    await state.reset_state(with_data=False)


# ================= Добавление Нескольких ===============
@dp.callback_query_handler(lambda c: c.data == "add_products_more")
async def file_add_more(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(MESSAGES["add_products_more_message"])

    state = dp.current_state(user=callback.from_user.id)
    await state.set_state(StatesSaveProducts.all()[0])


@dp.message_handler(content_types=ContentTypes.DOCUMENT, state=StatesSaveProducts.STATE_ADD_MORE)
async def add_more(message: Message):
    if ".xlsx" in message.document.file_name:
        if document := message.document:
            await document.download(
                destination_file=f"file/{message.from_user.id}.xlsx",
            )

        await doc_exel(message)

        await message.answer(MESSAGES["there_is_exel"], reply_markup=BUTTON_TYPES["BTN_HOME"])
        os.remove(f"file/{message.from_user.id}.xlsx")

    else:
        await message.answer(MESSAGES["not_exel"],  reply_markup=BUTTON_TYPES["BTN_HOME"])

    state = dp.current_state(user=message.from_user.id)
    await state.reset_state(with_data=False)



# ===================================================
# ================== Просмотр Товара ================
# ===================================================
@dp.callback_query_handler(lambda c: c.data == "views_products")
async def views_products(callback: CallbackQuery):
    await callback.message.delete()
    get_tovat_art_price = db.get_add_tovar(callback.from_user.id)

    if not get_tovat_art_price:
        await callback.message.answer(MESSAGES["no_added_products"])

    else:
        for art_price in get_tovat_art_price:
            art_price_message = re.sub(r'\(', 'Артикул: ', str(art_price))
            art_price_message = re.sub(r', ', '\nЦена: ', str(art_price_message))
            art_price_message = re.sub(r'\)', '', str(art_price_message))

            await callback.message.answer(art_price_message, reply_markup=BUTTON_TYPES["BTN_VIEWS_PRODUCTS"])

        await callback.message.answer(MESSAGES["delete_product"], reply_markup=BUTTON_TYPES["BTN_DELETE_ALL_PRODUCTS"])

    await callback.answer()

# ================== Оставить Товар ================
@dp.callback_query_handler(lambda c: c.data == "save_products")
async def save_products(callback: CallbackQuery):
    await callback.message.edit_reply_markup()

# ================== Удалить Товар ================
@dp.callback_query_handler(lambda c: c.data == "delete_products")
async def delete_products(callback: CallbackQuery):
    art_price = re.sub(r'[Артикул: Цена: ]', '', str(callback.message.text))
    art = re.sub(r'\n\d+', '', art_price)
    price = re.sub(r'\d+\n', '', art_price)

    await callback.message.edit_reply_markup()
    await callback.message.edit_text(f"Товар удалён:\n{callback.message.text}")
    db.delete_tovar(art, price, callback.from_user.id)

    await callback.answer()

# ==================== Удалить Все Товар ==================
@dp.callback_query_handler(lambda c: c.data == "delete_all_products")
async def delete_all_products(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(MESSAGES["delete_all_product"])
    db.delete_all_tovar(callback.from_user.id)
    await callback.answer()


# ===================== Кнопка отмены =====================
@dp.callback_query_handler(lambda c: c.data == 'cancellation')
async def cancellation_inline(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(MESSAGES["cancellation"])

    await callback.answer()

# ===================== Неизвестная команда =====================
@dp.message_handler()
async def unknown_command(message: Message):
    await message.answer(MESSAGES["unknown_command"])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def start():
    executor.start_polling(dp, on_shutdown=shutdown)