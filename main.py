import asyncio

from fastapi import FastAPI
from app.database import engine, Base
# 중요! 여기서 모델을 임포트 안 하면 Base가 어떤 테이블을 만들어야 할지 모름
from app.trades.services.controller import collect_upbit_trades
from app.trades.router import router as trade_router

app = FastAPI()
app.include_router(trade_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created")
    asyncio.create_task(collect_upbit_trades())
    print("start collector")


@app.get("/")
def read_root():
    return {"Hello": "Crypto World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}
