import sqlalchemy
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker, Session


CONNECTION_STR = "mssql+pyodbc://user:password@127.0.0.1/testDB?driver=SQL+Server"

# create db
Base = declarative_base()
class Transaction(Base):
    __tablename__ = 'Transactions'

    id = Column(Integer, primary_key=True)
    fromAddr = Column(String)
    Destination = Column(String)
    Amount = Column(Float)
    Module = Column(String)
    Method = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        str = f"Transaction(fromAddr='{self.fromAddr}', Destination='{self.Destination}',\
              Amount='{self.Amount}', Module='{self.Module}, Method={self.Method}, 'created_at={self.created_at}')"
        return str

# write data to db
def writeData(data):
    
    engine = create_engine(CONNECTION_STR)
    if not database_exists(engine.url):
        create_database(engine.url)  

    Session = sessionmaker(engine)
    session = Session()
    new_trx = Transaction(

        fromAddr = data['Signature'],
        Destination = data['Dest'],
        Amount = data['Amount'],
        Module = data['Pallet'],
        Method = data['Call'],
    )

    session.add(new_trx)
    print(f'\nExecuting add query:\n', new_trx)
    session.commit()


# some testing + table creation

'''
trx = Transaction(fromAddr=1, Destination=2011, Amount=1000000, Module='Balances', Method='Transfer')
engine = create_engine(CONNECTION_STR)
if not database_exists(engine.url):
    create_database(engine.url)
Base.metadata.create_all(engine)

Session = sessionmaker(engine)
with Session.begin() as session:
    session.add(trx)
    trxs = session.query(Transaction).all()
    print(trxs)
'''
