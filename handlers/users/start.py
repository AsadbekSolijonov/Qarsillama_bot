import logging

from loader import dp
from aiogram import types
from magic_filter import F
from aiogram.dispatcher.filters import Regexp
from keyboards.inline.buttons import plus_minus, order_cb, basket_buttons, item_cb
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.buttons import btn_menu, btn_somsa_list, back_basket, delivery_or_take_away, qarsillama_branches, \
    share_location, share_contact, menu
from utils.db_api.db_code import ProductDB, OrderDB, OrderItemDB
from loader import BASE_DIR


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    start_text = (f"Qarsillama botga xush kelibsiz.\n"
                  f"1. Menyuni tanlang.\n"
                  f"2. Nechta kerakligini belgilang.\n"
                  f"3. Xizmat turini tanlang.\n"
                  f"4. Telefon raqamingizni va manzilingizni yuboring.\n"
                  f"5. Kuting albatta sizga qo'ngiroq qilamiz.")
    await message.answer(f"Salom, {message.from_user.full_name}!")
    await message.answer(start_text, reply_markup=btn_menu())


@dp.message_handler(F.text == "Menu")
@dp.message_handler(F.text == "Ortga")
async def menu_handler(message: types.Message):
    products = ProductDB().get()
    text = ""
    for product in products:
        text += f"{product[0]}. {product[1]}  -   {product[2]} so'm\n"
    await message.answer(text, reply_markup=btn_somsa_list())


@dp.message_handler(Regexp(r"^\d+$"))
async def f_name(message: types.Message):
    product_id = message.text
    number = int(message.text)
    image_data = ProductDB().get(id=number)[0][-1]
    image_name = ProductDB().revert_image(image_data, f'{BASE_DIR}/media/somsa.png')
    img_file = open(f'{image_name}', 'rb')
    await message.answer_photo(photo=img_file, caption=f"Somsa",
                               reply_markup=plus_minus(product_id=product_id, count=1))


@dp.callback_query_handler(order_cb.filter(action='minus'))
@dp.callback_query_handler(order_cb.filter(action='plus'))
@dp.callback_query_handler(order_cb.filter(action='count'))
@dp.callback_query_handler(order_cb.filter(action='save'))
async def product_menu(call: types.CallbackQuery, callback_data: dict):
    count = int(callback_data['count'])
    action = callback_data['action']
    chat_id = call.message.chat.id
    product_id = callback_data['product_id']

    if action == "plus":
        count += 1
        await call.message.edit_reply_markup(plus_minus(product_id, count))

    elif action == "minus":
        if count > 1:
            count -= 1
            await call.message.edit_reply_markup(plus_minus(product_id, count))
        else:
            await call.answer('Mahsulotni eng kamida 1 ta sotib olish mumkin.')
    else:
        await call.answer(text=f"{count}")

    if action == 'save':
        await call.message.delete()
        OrderDB().save(user_id=chat_id, product_id=product_id)

        order_id = OrderDB().get(user_id=chat_id, product_id=product_id)[0]
        logging.info(order_id)
        OrderItemDB().save(order_id=order_id, count=count)
        await call.answer(text="Savatga qo'shildi")
        await call.message.answer(f"Savatga qo'shildi {count}", reply_markup=back_basket())
    await call.answer(cache_time=1)


@dp.message_handler(F.text == "Savatni ko'rsat")
async def show_basket(message: types.Message):
    await message.answer("Sizning buyurtmalaringiz!")
    chat_id = message.chat.id
    datas = OrderDB().get_basket(user_id=chat_id)
    products_id = [(data[2], data[3]) for data in datas]
    details = [
        (ProductDB().get(id=product_id)[0][1], product_count, ProductDB().get(id=product_id)[0][2] * product_count) for
        product_id, product_count in products_id]
    text = ""
    for detail in details:
        text += f"{detail[0]}. {detail[1]}x - {detail[2]:,.0f} so'm\n"

    total = sum([detail[2] for detail in details])
    text += f"\nJami:       {total:,.0f} so'm"
    await message.answer(text, reply_markup=basket_buttons(user_id=chat_id))


@dp.callback_query_handler(item_cb.filter(action='minus_basket'))
@dp.callback_query_handler(item_cb.filter(action='plus_basket'))
async def basket_updown(call: types.CallbackQuery, callback_data: dict):
    count = callback_data['count']
    action = callback_data['action']
    count, product_id = int(count[1]), int(count[4])

    if action == 'minus_basket':
        if count >= 1:
            count -= 1
            OrderDB().
        if count == 0:
            pass
        await call.answer(f"Count down: {count}")

    if action == 'plus_basket':
        count += 1
        await call.answer(f"Count up: {count}")
    try:
        chat_id = call.message.chat.id
        datas = OrderDB().get_basket(user_id=chat_id)
        products_id = [(data[2], data[3]) for data in datas]
        details = [
            (ProductDB().get(id=product_id)[0][1], product_count, ProductDB().get(id=product_id)[0][2] * product_count)
            for
            product_id, product_count in products_id]
        text = ""
        for detail in details:
            text += f"{detail[0]}. {detail[1]}x - {detail[2]:,.0f} so'm\n"

        total = sum([detail[2] for detail in details])
        text += f"\nJami:       {total:,.0f} so'm"
        await call.message.edit_text(text, reply_markup=basket_buttons(user_id=chat_id))
    except Exception as e:
        logging.error(e)

    await call.answer(cache_time=60)


@dp.message_handler(F.text == 'Buyurtmani rasmiylashtirish')
async def buyurtmani_rasmiylashtir(message: types.Message):
    await message.answer("Buyurtma rasmiylashtirish uchun xizmat turini tanlang:", reply_markup=delivery_or_take_away())


@dp.message_handler(F.text == "Olib ketish")
async def take_away(message: types.Message):
    await message.answer("O'zingizga eng yaqin bo'lgan filialni tanlang", reply_markup=qarsillama_branches())


@dp.message_handler(text=["Mega planet filiali", "Chilonzor filiali"])
async def filial(message: types.Message):
    if message.text == "Mega planet filiali":
        await message.answer_location(latitude=41.36731, longitude=69.29105)
        await message.answer("Mega Planet filiali manzili shu yerda joylashgan.", reply_markup=btn_menu())
    elif message.text == "Chilonzor filiali":
        await message.answer_location(latitude=41.273499, longitude=69.204989)
        await message.answer("Chilonzor filiali manzili shu yerda joylashgan.", reply_markup=btn_menu())
    await message.answer("Buyurtmangizni shu yerdan olib ketishingiz mumkin.")


@dp.message_handler(F.text == "Yetkazib berish")
async def delivery(message: types.Message):
    await message.answer("Lokatsiya tashlang", reply_markup=share_location())


@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def share_phone_and_save_location(message: types.Message):
    await message.answer("Telefon raqamingizni yuboring!", reply_markup=share_contact())


@dp.message_handler(content_types=types.ContentTypes.CONTACT)
async def give_phone_number(message: types.Message):
    await message.answer(text="Buyurma qabul qilindi.", reply_markup=btn_menu())


@dp.message_handler(text="Buyurtmamni ko'rsat")
async def my_order(message: types.Message):
    order = "data"
    if order:
        await message.answer("Sizning joriy buyurtmangiz:")
        await message.answer("Samsalar\nJami: 13,000 so'm")
    else:
        await message.answer_photo(photo=open("media/taomlar/somsa.jpeg", "rb"),
                                   caption="Sizda hozir joriy buyurtma mavjud emas:\nQarsillama so'msaga hoziroq buyurtma bering",
                                   reply_markup=menu())
