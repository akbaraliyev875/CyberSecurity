import asyncio
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "8663489236:AAHWoq7Z2H4V6lN41qSQSRZuuSCm9XofxNc"
# VirusTotal dan bepul API kalit olishingiz mumkin
VT_API_KEY = "553b60d1c14acaa0a870c66c41701c09e3bd31ac4204dccd7fe85e57eb916dc6" 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Parol mustahkamligini tekshirish funksiyasi
def check_password(password):
    score = 0
    if len(password) >= 8: score += 1
    if re.search("[a-z]", password) and re.search("[A-Z]", password): score += 1
    if re.search("[0-9]", password): score += 1
    if re.search("[@#$%^&+=]", password): score += 1
    
    levels = {0: "⚠️ Juda zaif", 1: "🟠 Zaif", 2: "🟡 O'rtacha", 3: "🟢 Yaxshi", 4: "🔥 Mukammal"}
    return levels.get(score, "Noma'lum")

@dp.message(Command("start"))
async def start_command(message: types.Message):
    text = (
        f"Salom, {message.from_user.first_name}! Men sizning kiber-himoyachingizman. 🛡\n\n"
        "Nimalar qila olaman:\n"
        "1️⃣ Parol yuboring — uni mustahkamligini tekshiraman.\n"
        "2️⃣ Havola (link) yuboring — u xavfli emasligini ko'rib chiqaman.\n"
        "3️⃣ Shubhali xabarlarni tahlil qilishga yordam beraman."
    )
    await message.answer(text)

@dp.message()
async def analyze_message(message: types.Message):
    user_input = message.text

    # Agar havola bo'lsa
    if "http" in user_input or "." in user_input:
        await message.reply("🔍 Havola tahlil qilinmoqda... Iltimos, shaxsiy ma'lumotlaringizni kiritishga shoshilmang!")
        # Bu yerga keyinchalik VirusTotal API ulaymiz
        await message.answer("ℹ️ Maslahat: Agar sayt sizdan kutilmaganda login yoki karta raqamini so'rasa, bu firibgarlik bo'lishi mumkin.")
    
    # Agar parol bo'lishi mumkin bo'lgan matn bo'lsa
    elif len(user_input) > 0:
        result = check_password(user_input)
        await message.reply(f"🔐 Parol tahlili:\n\nHolati: <b>{result}</b>\n\n"
                           f"💡 Maslahat: Hech qachon bir xil parolni hamma joyda ishlatmang!", parse_mode="HTML")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
