from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.db_api.db_code import ProductDB


def btn_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    menu = KeyboardButton("Menu")
    basket = KeyboardButton("Buyurtmamni ko'rsat")
    return kb.add(menu, basket)


def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    menu = KeyboardButton("Menu")
    return kb.add(menu)


def btn_somsa_list():
    btns_somsa = ReplyKeyboardMarkup(resize_keyboard=True)
    products = ProductDB().get()
    btns = []
    for product in products:
        btn = KeyboardButton(str(product[0]))
        btns.append(btn)
    return btns_somsa.add(*btns)


def back_basket():
    btns = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back = KeyboardButton("Ortga")
    basket = KeyboardButton("Savatni ko'rsat")
    buy = KeyboardButton("Buyurtmani rasmiylashtirish")
    btns.add(
        back, basket, buy
    )
    return btns


def delivery_or_take_away():
    btns = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back = KeyboardButton("Olib ketish")
    basket = KeyboardButton("Yetkazib berish")
    btns.add(back, basket)
    return btns


def qarsillama_branches():
    btns = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    yunusobod = KeyboardButton("Mega planet filiali")  # 41.36731, 69.29105
    chilonzor = KeyboardButton("Chilonzor filiali")  # 41.273499, 69.204989
    olmazor = KeyboardButton("Olmazor filiali")  # 41.351011, 69.222461
    mirzo_ulugbek = KeyboardButton("Mirzo Ulug'bek filiali")  # 41.282059, 69.213405
    sergili = KeyboardButton("Sergili filiali")  # 41.262612, 69.238439
    yashnaobod = KeyboardButton("Yashnaobod filiali")  # 41.292417, 69.321480
    pushkin = KeyboardButton("Pushkin filiali")  # 41.322021, 69.311374
    chorsu = KeyboardButton("Chorsu filiali")  # 41.313792, 69.291506
    yakkasaroy = KeyboardButton("Yakkasaroy filiali")  # 41.285773, 69.251646
    mirobod = KeyboardButton("Mirobod filiali")  # 41.290151, 69.286974
    uchtepa = KeyboardButton("Uchtepa filiali")  # 41.298430, 69.176075
    urikzor = KeyboardButton("O'rikzor filiali")  # 41.288244, 69.144482
    btns.add(yunusobod, chilonzor, olmazor, mirzo_ulugbek, sergili, yashnaobod, pushkin, chorsu, yakkasaroy, mirobod,
             uchtepa, urikzor)
    return btns


def share_location():
    btns = ReplyKeyboardMarkup(resize_keyboard=True)
    loc = KeyboardButton("Lokatisya yuborish", request_location=True)
    return btns.add(loc)


def share_contact():
    btns = ReplyKeyboardMarkup(resize_keyboard=True)
    contact = KeyboardButton("Telefon nomer yuborish", request_contact=True)
    return btns.add(contact)
