import httpx
from app.config.settings import settings


class TelegramNotifier:
    @classmethod
    async def send_message(cls, text: str):
        token = settings.TELEGRAM_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID

        if not token or not chat_id:
            print(f"error telegram token")
            return

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        async with httpx.AsyncClient() as client:
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown",
            }
            try:
                response = await client.post(url, json=payload, timeout=5.0)  # 타임아웃도 챙겨라
                if response.status_code != 200:
                    print(f"fail to send {response.text}")
                else:
                    print("successful send message")
            except Exception as e:
                print(f"telegram network error: {e}")