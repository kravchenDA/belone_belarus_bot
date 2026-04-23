import random
from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import register_user, save_taste_result, get_user
from keyboards import main_menu, after_taste_menu
from states import TasteQuest

router = Router()

# ==================== СТАРТ ====================

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    register_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )

    welcome_text = (
        "🧃 **Добро пожаловать в BelONE!**\n\n"
        "Я — твой гид в мир здорового перекуса.\n\n"
        "**BelONE — это:**\n"
        "· 🐢 6 часов сытости\n"
        "· 🧠 Энергия для мозга\n"
        "· 🌿 Забота о кишечнике\n"
        "· 🍓 Только натуральное\n"
        "· ❌ Ноль сахара\n\n"
        "👇 Нажми **🔮 Подобрать вкус**"
    )

    await message.answer(welcome_text, reply_markup=main_menu, parse_mode="Markdown")

# ==================== ПОДБОР ВКУСА ====================

@router.message(F.text == "🔮 Подобрать вкус")
async def start_taste_quest(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(TasteQuest.q1)
    await message.answer(
        "🔮 **Вопрос 1 из 4**\n\n"
        "🍬 **Какой у тебя характер в еде?**\n\n"
        "1 — Люблю сладкое и нежное\n"
        "2 — Люблю яркое, сочное\n"
        "3 — Люблю свежее, с кислинкой\n"
        "4 — Люблю пробовать новое\n\n"
        "Напиши **цифру** 1, 2, 3 или 4",
        parse_mode="Markdown"
    )

@router.message(TasteQuest.q1)
async def taste_q1(message: Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4"]:
        await message.answer("Напиши цифру 1, 2, 3 или 4")
        return
    await state.update_data(q1=message.text)
    await state.set_state(TasteQuest.q2)
    await message.answer(
        "⚡ **Вопрос 2 из 4**\n\n"
        "**Когда ты перекусываешь?**\n\n"
        "1 — Утром\n"
        "2 — В школе/на учёбе\n"
        "3 — После тренировки\n"
        "4 — Вечером"
    )

@router.message(TasteQuest.q2)
async def taste_q2(message: Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4"]:
        await message.answer("Напиши цифру 1, 2, 3 или 4")
        return
    await state.update_data(q2=message.text)
    await state.set_state(TasteQuest.q3)
    await message.answer(
        "🌞 **Вопрос 3 из 4**\n\n"
        "**Какое у тебя настроение?**\n\n"
        "1 — Спокойное\n"
        "2 — Бодрое\n"
        "3 — Свежее\n"
        "4 — Весёлое"
    )

@router.message(TasteQuest.q3)
async def taste_q3(message: Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4"]:
        await message.answer("Напиши цифру 1, 2, 3 или 4")
        return
    await state.update_data(q3=message.text)
    await state.set_state(TasteQuest.q4)
    await message.answer(
        "🎨 **Вопрос 4 из 4**\n\n"
        "**Какой цвет тебе ближе?**\n\n"
        "1 — Розовый\n"
        "2 — Оранжевый\n"
        "3 — Фиолетовый\n"
        "4 — Жёлтый"
    )

@router.message(TasteQuest.q4)
async def taste_q4(message: Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4"]:
        await message.answer("Напиши цифру 1, 2, 3 или 4")
        return
    await state.update_data(q4=message.text)

    data = await state.get_data()
    answers = f"{data['q1']}{data['q2']}{data['q3']}{message.text}"
    
    if answers == "1111":
        taste_name = "Клубника 🍓"
        taste_key = "strawberry"
        desc = "✨ **Тебе подходит КЛУБНИКА** — нежная и сладкая"
    elif answers == "2222":
        taste_name = "Манго-персик 🥭"
        taste_key = "mango"
        desc = "☀️ **Тебе подходит МАНГО-ПЕРСИК** — сочный и бодрый"
    elif answers == "3333":
        taste_name = "Ягодный микс 🫐"
        taste_key = "berry"
        desc = "🌿 **Тебе подходит ЯГОДНЫЙ МИКС** — свежий и кисло-сладкий"
    else:
        taste_name = "Клубника + Мята 🌱"
        taste_key = "secret"
        desc = "🎁 **Тебе подходит СЕКРЕТНЫЙ ВКУС** — клубника с мятой"

    save_taste_result(message.from_user.id, taste_key, answers)
    await state.clear()

    await message.answer(f"{desc}\n\nХочешь рецепт? Нажми 👩‍🍳 Рецепт дня", reply_markup=after_taste_menu, parse_mode="Markdown")

# ==================== РЕЦЕПТ ====================

@router.message(F.text == "👩‍🍳 Рецепт дня")
async def send_recipe(message: Message, state: FSMContext):
    await state.clear()
    user = get_user(message.from_user.id)
    last_taste = user[3] if user and user[3] else "strawberry"
    
    recipes = {
        "strawberry": "🍓 **Клубника:** творог 200г + молоко 110мл + клубника 85г + чиа 20г + мёд",
        "mango": "🥭 **Манго:** творог 200г + кокосовое молоко 110мл + манго 85г + чиа 20г + мёд",
        "berry": "🫐 **Ягодный микс:** творог 200г + молоко 110мл + ягоды 85г + чиа 20г + мёд",
        "secret": "🌱 **Клубника+Мята:** клубника 85г + мята + творог 200г + молоко + чиа"
    }
    await message.answer(f"👩‍🍳 **Рецепт BelONE:**\n\n{recipes.get(last_taste, recipes['strawberry'])}", parse_mode="Markdown")

# ==================== ИГРА ====================

@router.message(F.text == "🎮 Играть")
async def play_game(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🎮 **Угадай лишний ингредиент!**\n\n"
        "Какой ингредиент НЕ входит в состав BelONE?\n\n"
        "• Творог\n• Мёд\n• Сахар\n• Клубника\n• Семена чиа\n\n"
        "Напиши ответ 👇"
    )

# ==================== ТРЕКЕР ВОДЫ ====================

user_water = {}

@router.message(F.text == "💧 Трекер воды")
async def water_tracker(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("💧 **Трекер воды**\n\nСколько стаканов воды ты выпил сегодня?\n\nНапиши число:")

# ==================== СОВЕТ ДНЯ ====================

@router.message(F.text == "🌿 Совет дня")
async def daily_tip(message: Message, state: FSMContext):
    await state.clear()
    tips = [
        "💧 Пей воду за 20 минут до еды",
        "🍓 BelONE даёт сытость на 6 часов",
        "🌱 Семена чиа — суперфуд для кишечника",
        "❌ В BelONE нет сахара, только мёд",
        "🏃‍♂️ Выпей BelONE за 30 мин до тренировки"
    ]
    await message.answer(f"🌿 **Совет дня:**\n\n{random.choice(tips)}", parse_mode="Markdown")

# ==================== ОБРАБОТЧИК ОТВЕТОВ ====================

@router.message(F.text, ~StateFilter(TasteQuest))
async def handle_answers(message: Message):
    text = message.text.lower().strip()
    
    # Игра
    if text == "сахар":
        await message.answer("✅ **Правильно!** В BelONE нет сахара! 🎉")
    elif text in ["творог", "мёд", "клубника", "семена чиа", "чиа"]:
        await message.answer("❌ Не угадал! Этот ингредиент **есть** в BelONE.")
    
    # Трекер воды
    elif text.isdigit():
        count = int(text)
        if count < 3:
            await message.answer(f"💧 {count} стакана. Маловато! Норма — 6-8 стаканов.")
        elif 3 <= count <= 5:
            await message.answer(f"💧 {count} стакана. Хорошо, но можно больше!")
        elif count >= 6:
            await message.answer(f"💧 {count} стаканов! Отлично! Ты заботишься о себе 🌟")
