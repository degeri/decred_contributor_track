
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker # scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    'mysql+pymysql://user:password@localhost/contributors?charset=utf8',
    connect_args = {
        'port': 3306
    },
    echo='debug',
    echo_pool=True
)

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

