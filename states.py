from aiogram.fsm.state import State, StatesGroup


class TasteQuest(StatesGroup):
    """Состояния для подбора вкуса"""
    q1 = State()  # характер в еде
    q2 = State()  # время перекуса
    q3 = State()  # настроение
    q4 = State()  # цвет
