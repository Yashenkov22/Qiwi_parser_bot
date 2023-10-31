from sqlalchemy import insert
from sqlalchemy.orm import Session

from db.models import BankInfo


def add_record(session: Session,
               phone: str,
               name: str):
    with session.begin():
        session.execute(insert(BankInfo).values(phone=phone, 
                                                name=name))
        

def check_record(session: Session,
                 phone: str):
    with session.begin():
        return session.get(BankInfo, phone)