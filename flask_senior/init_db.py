from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

mysql_url = "mysql+pymysql://root:930809@localhost/test_db?charset=utf8"
world_url = "mysql+pymysql://root:930809@localhost/world?charset=utf8"

engine = create_engine(mysql_url, echo=True)
# engine = create_engine(mysql_url, echo=True, connect_args={"options": "-c timezone=utc"})
world_engine = create_engine(world_url, echo=True)

# Declare & create Session
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
world_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=world_engine))

# Create SqlAlchemy Base Instance
Base = declarative_base()
Base.query = db_session.query_property()
world_base = declarative_base()
world_base.query = world_session.query_property()

def init_database():
    Base.metadata.create_all(bind=engine)
    
def init_world_database():
    world_base.metadata.create_all(bind=world_engine)