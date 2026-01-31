from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)