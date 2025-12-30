import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.trades.models import Trade


class TradeAnalyzer:
    @staticmethod
    async def get_stats(db: AsyncSession, symbol: str):
        query = select(Trade).where(Trade.symbol == symbol).order_by(Trade.timestamp.desc()).limit(100)
        result = await db.execute(query)
        trades = result.scalars().all()

        if not trades:
            return None

        df = pd.DataFrame([
            {"price": t.price, "amount": t.amount, "side": t.side, "ts": t.timestamp} for t in trades
        ])

        stats = {
            "symbol": symbol,
            "avg_price": float(df["price"].mean()),  # average price
            "max_price": float(df["price"].max()), # max price
            "min_price": float(df["price"].min()),
            "total_volume": float(df["amount"].sum()),
            "buy_amount": int(len(df[df["side"] == "BID"])),
            "sell_amount": int(len(df[df["side"] == "ASK"]))
        }
        return stats
