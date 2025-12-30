import matplotlib.pyplot as plt
import pandas as pd
import io

from matplotlib import ticker
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

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(df["ts"], df["price"], marker="", linestyle="-", color='#007bff',linewidth=2,label="Price")
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p : format(int(x),',')))
        margin = (df["price"].max() - df["price"].min()) * 0.1
        ax.set_ylim(df["price"].min() - margin, df["price"].max() + margin)

        ax.set_title(f"{symbol} Real-time Price",fontsize=16,pad=20)
        ax.grid(True,linestyle="--", alpha=0.7)
        plt.xticks(rotation=30)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png',dpi=100)
        buf.seek(0)
        plt.close()

        return buf
