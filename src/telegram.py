import httpx
from src.config import BOT_TOKEN, CHAT_ID


async def send_by_telegram(text: str):
    url_req = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    async with httpx.AsyncClient() as client:
        await client.post(url=url_req, json={"chat_id": CHAT_ID, "text": text})
