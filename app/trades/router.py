from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from starlette.responses import StreamingResponse

from app.database import get_db
from app.trades.models import Trade
from app.trades.schemas import TradeResponse
from app.trades.services.analyzer import TradeAnalyzer
from app.trades.services.visualizer import TradeVisualizer

router = APIRouter(prefix="/trades", tags=["Trades"])


@router.get("/", response_model=List[TradeResponse])
async def get_trades(
        symbol: str = Query(None, description="코인 심볼 (예: KRW-BTC)"),
        limit: int = Query(10, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
):
    """
    최근 체결 내역을 조회합니다.
    :param symbol:
    :param limit:
    :param db:
    :return:
    """
    query = select(Trade).order_by(Trade.timestamp.desc()).limit(limit)
    if symbol:
        query = query.where(Trade.symbol == symbol)

    result = await db.execute(query)
    trades = result.scalars().all()
    return trades


@router.get("/stats/{symbol}")
async def get_trade_stats(
        symbol: str,
        db: AsyncSession = Depends(get_db)
):
    stats = await TradeAnalyzer.get_stats(db, symbol)
    if not stats:
        return {"message": "No data found for this symbol"}
    return stats


@router.get("/chart/{symbol}")
async def get_trade_chart(symbol: str, db: AsyncSession = Depends(get_db)):
    image_buf = await TradeVisualizer.save_price_chart(db, symbol)
    if not image_buf:
        return {"message": "No data"}

    return StreamingResponse(image_buf, media_type="image/png")
