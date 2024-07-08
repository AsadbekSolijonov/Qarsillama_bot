from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_code import ProductDB, OrderDB

order_cb = CallbackData('product', 'product_id', 'count', 'action')
item_cb = CallbackData('product', 'count', 'action')


def plus_minus(product_id, count):
    inline = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='-', callback_data=order_cb.new(product_id=product_id, count=count, action='minus')),
         InlineKeyboardButton(text=str(count),
                              callback_data=order_cb.new(product_id=product_id, count=count, action='count')),
         InlineKeyboardButton(text='+', callback_data=order_cb.new(product_id=product_id, count=count, action='plus'))],
        [InlineKeyboardButton(text="Savatga qo'shish",
                              callback_data=order_cb.new(product_id=product_id, count=count, action='save')), ]
    ])
    return inline


def basket_buttons(user_id):
    products = OrderDB().get_basket(user_id=user_id)
    key_list = []

    for product in products:
        full_btn = []
        btn1 = InlineKeyboardButton(text='-',
                                    callback_data=item_cb.new(count=(product[3], product[2]), action='minus_basket'))
        btn2 = InlineKeyboardButton(text=f'{ProductDB().get(id=product[2])[0][1]}',
                                    callback_data=item_cb.new(count=(product[3], product[2]), action='minus_basket'))
        btn3 = InlineKeyboardButton(text='+',
                                    callback_data=item_cb.new(count=(product[3], product[2]), action='plus_basket'))
        full_btn.append(btn1)
        full_btn.append(btn2)
        full_btn.append(btn3)

        key_list.append(full_btn)

    inline_buttons = InlineKeyboardMarkup( inline_keyboard=key_list)
    return inline_buttons

