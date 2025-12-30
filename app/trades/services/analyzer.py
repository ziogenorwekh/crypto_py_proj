import asyncio

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.trades.models import Trade
from app.trades.services.notifier import TelegramNotifier


class TradeAnalyzer:
    @staticmethod
    async def get_stats(db: AsyncSession, symbol: str):
        query = select(Trade).where(Trade.symbol == symbol).order_by(Trade.timestamp.desc()).limit(100)
        result = await db.execute(query)
        trades = result.scalars().all()

        if not trades: return None

        df = pd.DataFrame([
            {"price": t.price, "amount": t.amount, "side": t.side, "ts": t.timestamp} for t in trades
        ])
        df = df.sort_values("ts")

        # 1. 이평선 계산 (윈도우 값 확인해라!)
        df['ma7'] = df['price'].rolling(window=7).mean()
        df['ma20'] = df['price'].rolling(window=20).mean()

        if len(df) < 20:
            return {"message": "shortage datas (need at least 20)"}

        # 2. 크로스 로직용 변수 추출
        curr_ma7 = df['ma7'].iloc[-1]
        curr_ma20 = df['ma20'].iloc[-1]
        prev_ma7 = df['ma7'].iloc[-2]
        prev_ma20 = df['ma20'].iloc[-2]

        # 3. 골든/데드 크로스 판별
        status = "NORMAL"
        if (prev_ma7 <= prev_ma20) and (curr_ma7 > curr_ma20):
            status = "GOLDEN Cross"
            print(f"🚀 {symbol} Golden Cross!")
            message = f"🚀 *{symbol} 골든크로스 발생!*\n현재가: {df['price'].iloc[-1]:,.0f}원\nMA7이 MA20을 뚫었습니다!"
            asyncio.create_task(TelegramNotifier.send_message(message))
            print(f"successful sending message")
        elif (prev_ma7 >= prev_ma20) and (curr_ma7 < curr_ma20): # 오타 수정됨
            status = "DEAD Cross"
            print(f"💀 {symbol} Dead Cross!")

        # 4. 결과 정리
        latest_ma7 = float(curr_ma7) if pd.notnull(curr_ma7) else None

        return {
            "symbol": symbol,
            "current_price": float(df["price"].iloc[-1]),
            "avg_price": float(df["price"].mean()),
            "max_price": float(df["price"].max()),
            "min_price": float(df["price"].min()),
            "total_volume": float(df["amount"].sum()),
            "buy_count": int(len(df[df["side"] == "BID"])),
            "sell_count": int(len(df[df["side"] == "ASK"])),
            "ma7": latest_ma7,
            "status": status
        }