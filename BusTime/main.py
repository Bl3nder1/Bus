import time
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from cfg import *
from pars import *
from ClassObj import *
from keyboard import *
from Global import *
from aiogram.dispatcher.filters import Text
from aiogram.types import InputMediaPhoto, InputMediaVideo
import asyncio
from typing import List

storage = MemoryStorage()
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
async def on_startup(_):
    print("Bot starting")





@dp.message_handler(commands=["start"])
async def echo(message: types.Message):
    await message.answer(text="Привет, я Бот BusTime!\n"
                              "Выбери то что тебя интересует!",
                         reply_markup = Menuboard)




@dp.message_handler(text= 'Где автобус?')
async def echo(message: types.Message):
    await message.answer(text="Здесь ты сможешь узнать откуда и до куда ездит тот или инной маршрут"
                              " а так же количество автобусов на маршруте!\n"
                              "Выбери интересующий тебя вид траспорта",
                         reply_markup=TypeBoard)
    await BusT.next()

@dp.message_handler(state=BusT.typeBus)
async def BusTT(message: types.Message, state: FSMContext):
    text = message.text
    if text == "Назад":
        await state.finish()
        await message.answer('Okay',
                             reply_markup=Menuboard)
    else:
        kay_user1 = ""
        if text == 'Автобус':
            kay_user1 += 'bus'
        elif text == 'Тролейбус':
            kay_user1 += 'trolleybus'
        else:
            kay_user1 += 'tramway'

        await message.answer(text=f"Отлично! Вы выбрали {text}\n"
                                  "Введите номер маршрута",
                             reply_markup=ReplyKeyboardRemove())
        BusT.typeBus = kay_user1
        await BusT.next()

@dp.message_handler(state=BusT.num)
async def BusTT(message: types.Message, state: FSMContext):
    text = message.text
    kay_user1 = BusT.typeBus
    if text == 'Назад':
        await state.finish()
        await message.answer(text="Okay",
                             reply_markup=Menuboard)
    else:
        kay_user2 = kay_user1
        kay_user2 += f"-{text}"

        with open("Bus_Time.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            main()
            for key in data:
                if key == kay_user2:
                    with open("Bus_Time.json", "r", encoding="utf-8") as f:
                        data = json.load(f)

                        user_data = data.get(kay_user2, {})

                        article_title = user_data.get('article_title', 'Неизвестно')
                        Number = user_data.get('Number', 'Неизвестно')
                        BusLine = user_data.get('BusLine', 'Неизвестно')

                        if kay_user2.split('-')[0] == 'bus':
                            txt = 'Автобусов'
                        elif kay_user2.split('-')[0] == 'trolleybus':
                            txt = 'Тролейбусов'
                        else:
                            txt = 'Трамваев'

                        get_bus_route(headers, kay_user2)

                        await message.reply(f"Маршрут №{Number}\n{article_title}\n"
                                            f"{txt} на маршруте: {BusLine}",
                                            reply_markup=To_accept(kay_user2))

                    await state.finish()
                    await message.answer(text="Выбери то что тебя интересует!",
                                         reply_markup=Menuboard)
                    break

            else:
                await message.answer(text=f"Увы, такого маршрута нет!\n"
                                          f"Попробуйте ввести другой номер маршрута или нажмите "
                                          f"'Назад'",
                                     reply_markup=Break)






@dp.callback_query_handler(Text(startswith='BusStops'))
async def editTsk(call: types.CallbackQuery, state: FSMContext):
    cd = call.data.split('/')

    stops = get_bus_route(headers, cd[-1])
    text = ''

    for e in stops[int(cd[-2])]:
        text += f'{e}\n\n'




    await call.message.answer(text=f'{text}',
                                reply_markup=update(cd[-1], cd[-2]))



@dp.callback_query_handler(Text(startswith='update'))
async def update_stops(call: types.CallbackQuery, state: FSMContext):
    c = 0
    while c <= 30:
        cd = call.data.split('/')

        stops = get_bus_route(headers, cd[-1])

        current_index = int(cd[-2])

        if current_index < len(stops):
            text = ''
            for e in stops[current_index]:
                text += f'{e}\n\n'





            if c == 30:
                try:
                    await call.message.edit_text(text=f'{text}',
                                                    reply_markup=update(cd[-1], current_index))
                except:
                    pass
            else:
                try:
                    await call.message.edit_text(text=f'{text}')
                except:
                    pass
        if c == 0:
            no_updates_message = await call.message.answer(text='Список обновляется каждые 10 секунд в течении 5 минут')
        if c == 1:
            await no_updates_message.delete()



        await asyncio.sleep(10)
        print("update")
        c += 1












@dp.message_handler(text= 'Время прибытия на остановку')
async def echo(message: types.Message):
    await message.answer(text="Узнайте, какие автобусы скоро приедут на остановку, которая вам нужна\n"
                              "Введите название остановки",
                         reply_markup=Break)
    await BusWhStop.next()

@dp.message_handler(state=BusWhStop.typeStop)
async def BusTT(message: types.Message, state: FSMContext):
    stops = message.text
    if stops == 'Назад':
        await state.finish()
        await message.answer('Okay', reply_markup=Menuboard)
    else:
        lis = Nearest_bus(stops)
        txtBoard = ''
        txt = ''
        for e in range(len(lis)):
            txtBoard += f'{lis[e]}/'
        try:
            if 0 < len(lis) <= 4:
                await message.answer(text=f"По вашему запросу найдено {len(lis)} остановки\n\n"
                                          f"Какая именно остановка?",
                                     reply_markup=StopsBoard(txtBoard))

                await BusWhStop.next()
            else:
                await message.answer(text="Введите более точное название остановки")
        except:
            await message.answer(text="Введите более точное название остановки")

        BusWhStop.typeStop = lis



@dp.callback_query_handler(Text(startswith='Numpad'), state=BusWhStop.numStop)
async def update_stops(call: types.CallbackQuery, state: FSMContext):
    cd = call.data.split('/')
    numS = cd[-1]
    lis = BusWhStop.typeStop
    if 0 < int(numS) <= (len(lis)+1):
        numS = int(numS)
        name = lis[numS-1]

        url = get_url_busstop(name)

        try:
            await call.message.answer(text=f'Остановка {name}',
                                reply_markup=TimeBusSide(url))
        except:
            await call.message.answer(text=f'Ошибка сайта!',
                                      reply_markup=Menuboard)


        await state.finish()
    else:
        await call.message.answer(text='Введите правильную цифру')






@dp.callback_query_handler(Text(startswith='side'))
async def update_stops(call: types.CallbackQuery, state: FSMContext):
    cd = call.data.split('.')
    url = 'https://ru.busti.me//krasnoyarsk/stop/'+cd[-1]

    TimeBus = get_bus_url(url) # Получаем данные из парсера

    try:
        current_index = int(cd[-2]) # Индекс блока, с которого начинается вывод
        Time = TimeBus[current_index]
        Bus = TimeBus[current_index + 1]

        txt = (f'Остановка ""'
               f'\nВремя | Маршруты\n')
        for i in range(len(Time)):
            txt += f'{Time[i]}     {Bus[i]}\n'

        # Обновляем текст сообщения
        await call.message.edit_text(text=f'{txt}',
                                      reply_markup=TimeBusSideUpdate(url, current_index))
    except:
        pass



@dp.message_handler(text= 'Назад')
async def echo(message: types.Message):
    await message.answer('Okay', reply_markup=Menuboard)










if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)




