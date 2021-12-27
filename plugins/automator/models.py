from upd.models import RBaseModel

from sqlalchemy import Column, Integer, String, Text, Sequence, ForeignKey, Date, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref, aliased

from peewee import *

from .tool import tool

@tool.model
class Script(RBaseModel):
    name = CharField(default='')


@tool.model
class Stage(RBaseModel):
    type = CharField(default='')
    script = ForeignKeyField(Script, related_name='stages')
