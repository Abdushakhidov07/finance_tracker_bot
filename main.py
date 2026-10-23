from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from dotenv import load_dotenv 
from service import *
from connection import *
import asyncio
import os

load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = Bot(token=token)
dp = Dispatcher()



main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📋 Мои задачи")],
        [KeyboardButton(text="🆘 Помощь")],
    ],
    resize_keyboard=True,
)



@dp.message(CommandStart())
async def start_bot(message: Message):
    if await  get_user_by_id(message.from_user.id):
        await message.answer(f"Hello @{message.from_user.username}", reply_markup=main_kb)
    else:
        user = message.from_user
        await create_user(user.username, user.full_name, user.id)
        await message.answer(f"Hello @{message.from_user.username}", reply_markup=main_kb)



@dp.message(F.text == "🆘 Помощь")
@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(f"Этот телеграм бот имеет толька две команды /help и /start")


@dp.message(Command("/create_goal"))
async def goal_bot_create(message: Message, command:CommandObject):
    data = command.args.split("/")
    status = await create_goal(data[0], "goal", data[1], message.from_user.id)
    if status:
        await message.answer(f"Цель успешно создана!")
    else:
        await message.answer(f"Ошибка при создании!")

@dp.message(Command("/create_credit"))
async def credit_bot_create(message: Message, command:CommandObject):
    data = command.args.split("/")
    status = await create_goal(data[0], "credit", data[1], message.from_user.id)
    if status:
        await message.answer(f"Кредит успешно создана!")
    else:
        await message.answer(f"Ошибка при создании!")

@dp.message(Command("/create_withdraw"))
async def withdraw_bot_create(message: Message, command:CommandObject):
    data = command.args.split("/")
    if data[0] >= await get_balance():
        status = await create_tranzaction(data[0], "withdraw", data[1], message.from_user.id)
        if status:
            await message.answer(f"Денги успешно сняты!")
        else:
            await message.answer(f"Ошибка при снятии!")
    else:
        await message.answer(f"Недостаточно средтств на балансе!")


@dp.message(Command("/create_deposit"))
async def deposit_bot_create(message: Message, command:CommandObject):
    data = command.args.split("/")
    if data[0] > 0 :
        status = await create_tranzaction(data[0], "deposit", data[1], message.from_user.id)
        if status:
            await message.answer(f"Денги успешно сняты!")
        else:
            await message.answer(f"Ошибка при снятии!")
    else:
        await message.answer(f"Недостаточно средтств на балансе!")


        
@dp.message(Command("/profile"))
async def profile(message: Message):
    user = await get_user_by_id(message.from_user.id)
    text = ""
    text+=f"""
Telegram id: {user["telegram_id"]}
Username: {user["username"]}
Full name: {user["full_name"]}
balance: {user["balance"]}
        """
    await message.answer(text)








@dp.message(Command("/history"))
async def show_history(message: Message):
    history = await get_history(message.from_user.id)
    text = ""
    for his in history:
        text+=f"""
History id: {his["tranz_id"]}
Amount: {his["amount"]}
Type: {his["type"]}
Title: {his["title"]}

        """
    await message.answer(text)


@dp.message(Command("/history_deposit"))
async def show_history_deposit(message: Message):
    history = await get_tranz("deposit",message.from_user.id)
    text = ""
    for his in history:
        text+=f"""
History id: {his["tranz_id"]}
Amount: {his["amount"]}
Type: {his["type"]}
Title: {his["title"]}

        """
    await message.answer(text)

@dp.message(Command("/history_withdraw"))
async def show_history_withdraw(message: Message):
    history = await get_tranz("withdraw",message.from_user.id)
    text = ""
    for his in history:
        text+=f"""
History id: {his["tranz_id"]}
Amount: {his["amount"]}
Type: {his["type"]}
Title: {his["title"]}

        """
    await message.answer(text)

@dp.message(Command("/history_goal"))
async def show_history_goal(message: Message):
    history = await get_tranz("goal",message.from_user.id)
    text = ""
    for his in history:
        text+=f"""
History id: {his["tranz_id"]}
Amount: {his["amount"]}
Type: {his["type"]}
Title: {his["title"]}

        """
    await message.answer(text)


@dp.message(Command("/history_credit"))
async def show_history_credit(message: Message):
    history = await get_tranz("credit",message.from_user.id)
    text = ""
    for his in history:
        text+=f"""
History id: {his["tranz_id"]}
Amount: {his["amount"]}
Type: {his["type"]}
Title: {his["title"]}

        """
    await message.answer(text)










async def main():
    await create_table_db()
    print("Bot started")
    await dp.start_polling(bot)
    
    
    
if __name__ == "__main__":
    asyncio.run(main())
