from aiogram.types import *
from pars import *

TypeBoard = ReplyKeyboardMarkup(resize_keyboard=True)
w1 = KeyboardButton(text='Автобус')
w2 = KeyboardButton(text='Тролейбус')
w3 = KeyboardButton(text='Трамвай')
w4 = KeyboardButton(text='Назад')
TypeBoard.add(w1, w2, w3)
TypeBoard.add(w4)




Menuboard = ReplyKeyboardMarkup(resize_keyboard=True)
m1 = KeyboardButton(text="Где автобус?")
m2 = KeyboardButton(text='Время прибытия на остановку')
m3 = KeyboardButton(text='В разработке')
Menuboard.add(m1)
Menuboard.add(m2)
Menuboard.add(m3)


def To_accept(key):
    stops = get_bus_route(headers, key)
    text1 = f'Остановки от {stops[0][0]}'
    text2 = f'Остановки от {stops[1][0]}'

    InLineBoardStopBus = InlineKeyboardMarkup(row_width=2)

    bs1 = InlineKeyboardButton(text=f'{text1}', callback_data=f'BusStops/0/{key}')
    bs2 = InlineKeyboardButton(text=f'{text2}', callback_data=f'BusStops/1/{key}')

    InLineBoardStopBus.add(bs1, bs2)

    return InLineBoardStopBus


def update(key, rot):

    InLineUpdate = InlineKeyboardMarkup(row_width=2)

    update1 = InlineKeyboardButton(text=f'Обновить ⟳', callback_data=f'update/{rot}/{key}')

    InLineUpdate.add(update1)

    return InLineUpdate



def TimeBusSide(url):
    sides = get_side(url)
    url = str(url).split('/')
    SideBoard = InlineKeyboardMarkup(row_width=2)
    if sides != 0:

        try:
            side1 = InlineKeyboardButton(text=f'В сторону {sides[0]}', callback_data=f'side.0.{url[-2]}/')

        except:
            side1 = InlineKeyboardButton(text=f'Нет остановки', callback_data=f'side.0.{url[-2]}/')

        try:
            side2 = InlineKeyboardButton(text=f'В сторону {sides[1]}', callback_data=f'side.2.{url[-2]}/')
        except:
            side2 = InlineKeyboardButton(text=f'Нет остановки', callback_data=f'side.2.{url[-2]}/')
        SideBoard.add(side1, side2)

        return SideBoard

    else:
        return 0




def TimeBusSideUpdate(url, side):
    sides = get_side(url)
    url = str(url).split('/')
    UpdateSide = InlineKeyboardMarkup(row_width=2)

    upS = InlineKeyboardButton(text=f'Обновить ⟳', callback_data=f'side.{side}.{url[-2]}/')

    UpdateSide.add(upS)

    return UpdateSide


def StopsBoard(NameStops):
    StopspadKeyboard = InlineKeyboardMarkup(row_width=1)
    Name = str(NameStops).split('/')

    for i in range(len(Name)-1):
        StopspadKeyboard.add(InlineKeyboardButton(text=f'{Name[i]}', callback_data=f'Numpad/{i+1}'))




    return StopspadKeyboard


Break = ReplyKeyboardMarkup(resize_keyboard=True)
Br1 = KeyboardButton(text="Назад")
Break.add(Br1)