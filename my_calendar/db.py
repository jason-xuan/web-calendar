from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .modules import Base


engine = create_engine('mysql+mysqlconnector://wustl_inst:wustl_pass@ec2-52-14-93-16.us-east-2.compute.amazonaws.com:3306/calendar', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from .modules import User, Event, Tag
    Base.metadata.create_all(bind=engine)
