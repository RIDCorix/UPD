from .tool import tool
import time

@tool.init_task
def self_check(self, *args, **kwargs):
    console = kwargs.get('console')
    console.out('self check')
    console.out('checking version: v1.2.0 (already up to date)')


@tool.init_task
def count_one_to_ten(self, *args, **kwargs):
    console = kwargs.get('console')
    ten =  10
    for i in range(ten):
        console.progress('count one to ten', i, ten)
        time.sleep(0.1)

    console.done()


def load_extensions():
    return BUILT_IN_EXTENSIONS
