from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String

Base = declarative_base()


class BankInfo(Base):
    __tablename__= 'bank_info'

    phone: Mapped[str] = mapped_column(String(length=12), primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50))