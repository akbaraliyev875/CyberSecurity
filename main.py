import asyncio
import logging
import re
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Telegram bot token va VirusTotal API kaliti
TOKEN = "8663489236:AAHWoq7Z2H4V6lN41qSQSRZuuSCm9XofxNc"
VT_API_KEY = "553b60d1c14acaa0a870c66c41701c09e3bd31ac4204dccd7fe85e57eb916dc6"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Regex orqali URL ajratish
URL_PATTERN = r"(https?://[^\s]+)"

# Shubhali domenlar ro‘yxati
SUSPICIOUS_DOMAINS = ["login-facebook.com", "secure-paypal.net", "update-account.com"]

async def check_url_with_virustotal(url: str):
    """VirusTotal orqali havolani tekshirish"""
    api_url = "https://www.virustotal.com/api/v3/urls"
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url,
            headers={"x-apikey": VT_API_KEY},
            data={"url": url}) as resp:
            result = await resp.json()
            return result

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🛡 **Kiberxavfsizlik Botiga xush kelibsiz!**\n\n"
        "Men sizga shubhali havolalar va fishing xabarlarini aniqlashda yordam beraman.\n"
        "Tekshirish uchun xabar yoki havolani yuboring."
    )

@dp.message()
async def check_message(message: types.Message):
    urls = re.findall(URL_PATTERN, message.text)
    if not urls:
        await message.answer("❌ Havola topilmadi.")
        return

    response = "🔗 Topilgan havolalar:\n" + "\n".join(urls)

    for url in urls:
        # HTTPS tekshiruvi
        if url.startswith("http://"):
            response += f"\n⚠️ Havola xavfsiz emas (HTTPS yo‘q): {url}"

        # Shubhali domen tekshiruvi
        if any(domain in url for domain in SUSPICIOUS_DOMAINS):
            response += f"\n⚠️ Shubhali havola: {url}"

        # VirusTotal tekshiruvi
        vt_result = await check_url_with_virustotal(url)
        if "data" in vt_result:
            analysis_id = vt_result["data"]["id"]
            response += f"\n🧪 VirusTotal tekshiruvi ID: {analysis_id}"
        else:
            response += f"\n❌ VirusTotal tekshiruvi amalga oshmadi: {url}"

    await message.answer(response)

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
