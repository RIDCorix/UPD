from upd.models import RBaseModel

from sqlalchemy import Column, Integer, String, Text, Sequence, ForeignKey, Date, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref, aliased

from peewee import *

from .tool import tool

@tool.model
class Drawer(RBaseModel):
    name = CharField(default='')


@tool.model
class Variable(RBaseModel):
    name = CharField(default='')
    drawer = ForeignKeyField(Drawer, related_name='variables')
