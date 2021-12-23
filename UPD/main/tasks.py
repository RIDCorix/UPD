from sqlalchemy import Column, Integer, String, Text, Sequence, ForeignKey, Date, Boolean, create_engine

from extension.utils import get_tools
from upd.models import db
from .tool import tool as UPD
import time

@UPD.init_task
def self_check(tool, *args, **kwargs):
    console = kwargs.get('console')
    console.out('self check')
    console.out('checking version: v1.2.0 (already up to date)')


# @UPD.init_task
def count_one_to_ten(tool, *args, **kwargs):
    console = kwargs.get('console')
    ten =  10
    for i in range(ten):
        console.progress('count one to ten', i, ten)
        time.sleep(0.3)

    console.done()


@UPD.init_task
def initialize_db(tool, *args, **kwargs):
    console = kwargs.get('console')
    console.line('initialize_database')

    total = len(get_tools())
    with console.block() as block:
        for i, tool in enumerate(get_tools()):
            block.progress('creating tables', i, total)
            db.create_tables(tool.models)

    block.done()
