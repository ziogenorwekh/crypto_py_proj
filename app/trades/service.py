import json

import websockets
import asyncio

from app.database import AsyncSessionLocal
from app.trades.models import Trade

UPBIT_WS_URL = 'wss://api.upbit.com/websocket/v1'


async def collect_upbit_trades():
    async with websockets.connect(UPBIT_WS_URL) as websocket:
        subscribe_fmt = [
            {"ticket": "test-ticket"},
            {"type": "trade", "codes": ["KRW-BTC", "KRW-ETH"]}
        ]
        await websocket.send(json.dumps(subscribe_fmt))
        while True:
            data = await websocket.recv()
            data_dic = json.loads(data)

            async with AsyncSessionLocal() as session:
                new_trade = Trade(
                    symbol=data_dic.get("code"),
                    price=data_dic.get("trade_price"),
                    amount=data_dic.get("trade_volume"),
                    side=data_dic.get("ask_bid"),
                )
                session.add(new_trade)
                await session.commit()

            print(f"Saved: {data_dic.get('code')} - {data_dic.get('trade_price')}")