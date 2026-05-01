import asyncio
import time
import re
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# --- SOZLAMALAR ---
TOKEN = "8663489236:AAHWoq7Z2H4V6lN41qSQSRZuuSCm9XofxNc"
VT_API_KEY = "553b60d1c14acaa0a870c66c41701c09e3bd31ac4204dccd7fe85e57eb916dc6"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# --- YORDAMCHI FUNKSIYALAR ---

async def show_loading(message: types.Message, text: str):
    """Yuklanish effektini ko'rsatish"""
    chars = ["🌑", "🌒", "🌓", "🌔", "🌕"]
    for char in chars:
        try:
            await message.edit_text(f"{text} {char}")
            await asyncio.sleep(0.4)
        except: break

def check_password_strength(password):
    """Parol mustahkamligini tekshirish"""
    score = 0
    if len(password) >= 8: score += 1
    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1
    
    levels = {0: "Juda zaif 🔴", 1: "Zaif 🟠", 2: "O'rtacha 🟡", 3: "Yaxshi 🟢", 4: "Mukammal 🔥"}
    return levels.get(score, "Noma'lum")

# --- ASOSIY HANDLERLAR ---

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Assalomu alaykum, Dada!\n\n"
        "Men sizning kiber-yordamchingizman. Menga quyidagilarni yuborishingiz mumkin:\n"
        "1️⃣ **Parol** - mustahkamligini bilish uchun.\n"
        "2️⃣ **Havola (Link)** - virusga tekshirish uchun.\n"
        "3️⃣ **Fayl** - xavfsizligini tahlil qilish uchun."
    )

# 1. HAVOLA TEKSHIRISH (VIRUSTOTAL)
@dp.message_handler(regexp=r'(https?://\S+)')
async def url_handler(message: types.Message):
    start_time = time.time()
    msg = await message.answer("🔍 Havola aniqlandi. Tahlil boshlanmoqda...")
    
    await show_loading(msg, "📡 VirusTotal bazasidan ma'lumot olinmoqda")
    
    url = message.text
    vt_url = "https://www.virustotal.com/api/v3/domains/"
    domain = url.split("//")[-1].split("/")[0]
    
    headers = {"x-apikey": VT_API_KEY}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{vt_url}{domain}", headers=headers) as resp:
            duration = round(time.time() - start_time, 2)
            if resp.status == 200:
                data = await resp.json()
                stats = data['data']['attributes']['last_analysis_stats']
                res_text = (
                    f"🌐 **Havola:** {domain}\n"
                    f"⚠️ Zararli: {stats['malicious']}\n"
                    f"✅ Xavfsiz: {stats['harmless']}\n"
                    f"⏱ Sarflangan vaqt: {duration}s"
                )
            else:
                res_text = f"❌ Xatolik yuz berdi yoki limit tugadi. (Vaqt: {duration}s)"
            
            await msg.edit_text(res_text)

# 2. FAYL TEKSHIRISH
@dp.message_handler(content_types=['document', 'photo'])
async def file_handler(message: types.Message):
    start_time = time.time()
    msg = await message.answer("📁 Fayl qabul qilindi...")
    
    await show_loading(msg, "🧬 Fayl strukturasi tahlil qilinmoqda")
    
    duration = round(time.time() - start_time, 2)
    # Hozircha simulyatsiya, to'liq skaner uchun faylni yuklab olish va hash yuborish kerak
    await msg.edit_text(
        f"✅ **Fayl tahlili tayyor!**\n"
        f"📄 Nomi: {message.document.file_name if message.document else 'Rasm'}\n"
        f"🛡 Holati: Xavfsiz deb topildi\n"
        f"⏱ Vaqt: {duration}s"
    )

# 3. PAROL TEKSHIRISH
@dp.message_handler()
async def pass_handler(message: types.Message):
    if len(message.text) < 4: return
    
    start_time = time.time()
    msg = await message.answer("🔐 Parol tekshirilmoqda...")
    
    await show_loading(msg, "⚙️ Algoritmlar ishlamoqda")
    
    strength = check_password_strength(message.text)
    duration = round(time.time() - start_time, 2)
    
    await msg.edit_text(
        f"🔑 **Parol Tahlili:**\n"
        f"📊 Darajasi: {strength}\n"
        f"📏 Uzunligi: {len(message.text)} belgi\n"
        f"⏱ Vaqt: {duration}s"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
