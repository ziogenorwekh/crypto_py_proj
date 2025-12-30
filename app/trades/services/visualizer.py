import matplotlib.pyplot as plt
import pandas as pd
import io
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.trades.models import Trade


class TradeVisualizer:
    @staticmethod
    async def save_price_chart(db: AsyncSession, symbol: str):
        query = select(Trade).where(Trade.symbol == symbol).order_by(Trade.timestamp.desc()).limit(50)
        result = await db.execute(query)
        trades = result.scalars().all()

        if not trades:
            return None

        df = pd.DataFrame([{"price": t.price, "ts": t.timestamp} for t in trades])

        df = df.sort_values("ts")

        plt.figure(figsize=(10, 6))
        plt.plot(df["ts"], df["price"], marker="o", linestyle="-", color='b')
        plt.title(f"{symbol} Price Movement")
        plt.xlabel("Time")
        plt.ylabel("Price (KRW)")
        plt.xticks(rotatiton=45)
        plt.grid(True)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf
