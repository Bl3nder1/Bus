from aiogram.dispatcher.filters.state import State, StatesGroup



class BusT(StatesGroup):
    typeBus = State()
    num = State()


class BusWhStop(StatesGroup):
    typeStop = State()
    numStop = State()


