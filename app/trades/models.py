from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String(20), index=True, nullable=True)

    price = Column(Float, nullable=False)

    amount = Column(Float, nullable=False)

    side = Column(String(10))

    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Trade(symbol={self.symbol}, price={self.price}, side={self.side})>"
