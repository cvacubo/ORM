import transaction
from sqlalchemy.schema import Table, ForeignKey

from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, relationship, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


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

    session.flush()
    transaction.commit()

def initialize_sql(engine):
    #DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError:
        transaction.abort()
