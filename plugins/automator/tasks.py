from .tool import tool

@tool.init_task
def test(tool, **kwargs):
    print('im here')
    pass
