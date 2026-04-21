from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

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
after_taste_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👩‍🍳 Получить рецепт", callback_data="get_recipe")],
        [InlineKeyboardButton(text="🔁 Подобрать другой вкус", callback_data="restart_taste")]
    ]
)

# Кнопка возврата
back_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="back_to_menu")]
    ]
)
