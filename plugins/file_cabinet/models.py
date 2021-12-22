from upd.models import RBaseModel

from sqlalchemy import Column, Integer, String, Text, Sequence, ForeignKey, Date, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref, aliased

class Drawer(RBaseModel):
    __tablename__ = 'file_cabinet__drawer'

    name = Column(String)
    description = Column(Text)


class Variable(RBaseModel):
    __tablename__ = 'file_cabinet__variable'

    drawer = relationship(Drawer, order_by='Drawer.id', backref='variables', cascade='all, delete, delete-orphan')
