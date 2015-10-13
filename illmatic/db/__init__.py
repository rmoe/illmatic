from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://illmatic:zaq123@localhost/illmatic', convert_unicode=True)
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=True,
                                 bind=engine))
Base = declarative_base()
Base.query = db.query_property()


def init_db():
    import illmatic.db.models
    Base.metadata.create_all(bind=engine)


def drop_db():
    import illmatic.db.models
    Base.metadata.drop_all(bind=engine)
