from upd.models import RBaseModel

from sqlalchemy import Column, Integer, String, Text, Sequence, ForeignKey, Date, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref, aliased

from peewee import *

from .tool import tool

@tool.model
class Project(RBaseModel):
    name = CharField(default='')

    @property
    def graph(self):
        return self.graphs.get()

    @graph.setter
    def graph(self, account_obj):
        account_obj.person = self
        account_obj.save(only=[Graph.grp])

@tool.model
class Graph(RBaseModel):
    pass

class HasGraph(RBaseModel):
    project = ForeignKeyField(Project, related_name='nodes')


@tool.model
class Node(RBaseModel):
    name = CharField(default='')
    description = CharField(default='')

    x = FloatField(default=0)
    y = FloatField(default=0)

    graph = ForeignKeyField(Graph, related_name='nodes')

    @property
    def position(self):
        return (self.x, self.y)

@tool.model
class Connection(RBaseModel):
    key = CharField(default='')
    type = CharField(default='')
    from_node = ForeignKeyField(Node, related_name='to_relations')
    to_node = ForeignKeyField(Node, related_name='from_relations')

    removed = BooleanField(default=False)
