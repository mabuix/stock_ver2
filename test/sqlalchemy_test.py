import sqlalchemy as sa

# SQLAlchemyバージョン出力.
print(sa.__version__)

# ローカルのmysql stock_ver2データベースに接続.
# echo=Trueでロギング設定.
conn = sa.create_engine("mysql://root:@localhost/stock_ver2", echo=True)

rows = conn.execute('''
select * from stock_app_fundamentals_data limit 10;
''')

for row in rows:
    print(row)


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Fundamental(Base):
    __tablename__ = 'stock_app_fundamentals_data'

    code = Column(Integer, primary_key=True)
    name = Column(String)
    market_capitalization = Column(Integer)
    outstanding_shares = Column(Integer)

    def __repr__(self):
        return "<Fundamental(code='%s',name='%s',market_capitalization='%s',outstanding_shares='%s')>"%(
            self.code,self.name,self.market_capitalization,self.outstanding_shares
        )


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=conn)
session = Session()

query = session.query(Fundamental).filter(Fundamental.code.in_(['1435', '3267', '3547']))
fundamental_list = []
for fundamental in query.all():
    print('------------')
    print(fundamental.code)
    print(fundamental.name)
    print(fundamental.market_capitalization)
    print(fundamental.outstanding_shares)
    print('------------')
    fundamental_list.append(fundamental)

print(fundamental_list[0].code)