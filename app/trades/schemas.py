from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TradeBase(BaseModel):
    symbol: str
    price: float
    amount: float
    side: str


class TradeResponse(TradeBase):
    id: int
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
