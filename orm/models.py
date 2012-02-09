from sqlalchemy.types import BigInteger
import transaction
from sqlalchemy.schema import Table, ForeignKey, UniqueConstraint

from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, relationship, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class AppUser(Base):
    __tablename__ = 'app_user'
    id = Column(Integer, primary_key=True)
    publisher_id = Column(Integer, nullable=False)
    name = Column(String(25), nullable=False)
    __table_args__ = (UniqueConstraint('publisher_id', 'name', name='app_user_uniq'), {})

    def __init__(self, pub_id, name):
        self.publisher_id = pub_id
        self.name = name

class AppUserBalance(Base):
    __tablename__ = 'app_user_balance'
    id = Column(Integer, primary_key=True)
    app_user_id = Column(BigInteger, ForeignKey('app_user.id'), nullable=False)
    balance = Column(Integer, nullable=False)

    app_user = relationship(AppUser)

    def __init__(self, app_user, balance):
        self.app_user = app_user
        self.balance = balance


association_table = Table('association', Base.metadata,
    Column('parent_id', Integer, ForeignKey('parent.id')),
    Column('child_id', Integer, ForeignKey('child.id'))
)

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    children = relationship("Child",
        secondary=association_table)

    def __init__(self, name):
        self.name = name

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)

    def __init__(self, name):
        self.name = name

    def is_child(self, name):
        return True if self.name == name else False

def populate():
    session = DBSession()

    children = Child("Artem")
    parent = Parent("Alexander")
    parent2 = Parent("Olga")
    parent.children.append(children)

    session.add(children)
    session.add(parent)
    session.add(parent2)


    #app_user = AppUser('AppZap')
    #app_user_balance = AppUserBalance(app_user, 1000)
    #session.add(app_user_balance)

    session.flush()
    transaction.commit()

def initialize_sql(engine):
    #DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError: # pragma: no cover
        transaction.abort()
