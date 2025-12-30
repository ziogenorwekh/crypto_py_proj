import asyncio
from app.trades.services.notifier import TelegramNotifier
from app.config.settings import settings


async def test_bot():
    print("--- 텔레그램 봇 테스트 시작 ---")

    # 1. 설정값 제대로 읽어오는지 확인
    print(f"TOKEN 설정 상태: {'✅ 있음' if settings.TELEGRAM_TOKEN else '❌ 없음'}")
    print(f"CHAT_ID 설정 상태: {'✅ 있음' if settings.TELEGRAM_CHAT_ID else '❌ 없음'}")

    if not settings.TELEGRAM_TOKEN or not settings.TELEGRAM_CHAT_ID:
        print("🚨 에러: .env 파일에 토큰이랑 채팅 ID부터 똑바로 박아라!")
        return

    # 2. 실제 메시지 발송
    print("🚀 메시지 발송 시도 중...")
    test_message = "🔔 *시스템 알림*\n파이썬에서 보낸 테스트 메시지다. 이거 보이면 성공한 거임! ㅋㅋㅋ"

    await TelegramNotifier.send_message(test_message)
    print("--- 테스트 종료 ---")


if __name__ == "__main__":
    # 비동기 함수 실행
    asyncio.run(test_bot())