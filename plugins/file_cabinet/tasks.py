from .tool import tool

@tool.init_task
def test(tool):
    print('im here')
    pass
