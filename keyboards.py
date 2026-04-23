from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔮 Подобрать вкус")],
        [KeyboardButton(text="👩‍🍳 Рецепт дня"), KeyboardButton(text="🎮 Играть")],
        [KeyboardButton(text="💧 Трекер воды"), KeyboardButton(text="🌿 Совет дня")]
    ],
    resize_keyboard=True
)

# Меню после подбора вкуса
after_taste_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👩‍🍳 Рецепт дня")],
        [KeyboardButton(text="🔮 Подобрать вкус")],
        [KeyboardButton(text="💧 Трекер воды"), KeyboardButton(text="🌿 Совет дня")]
    ],
    resize_keyboard=True
)
