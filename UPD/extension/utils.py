import sys
# def get_tools():
#     manager = PluginManager()
#     manager.setPluginPlaces(["plugins/file_cabinet"])
#     manager.collectPlugins()

#     return [plugin.plugin_object for plugin in manager.getAllPlugins()]

def get_tools():
    import importlib
    tools = ['file_cabinet', 'us', 'automator', 'main']
    tool_installation_dir1 = 'C:/Users/User/UPD/plugins'
    tool_installation_dir2 = '/Users/mac/UPD/plugins'
    sys.path.append(tool_installation_dir1)
    sys.path.append(tool_installation_dir2)
    tool_instances = []
    auto_load_modules = ['tasks', 'ui', 'models', 'renderers']
    for tool in tools:
        tool_instances.append(importlib.import_module('.'.join([tool, 'tool'])).tool)
        for module in auto_load_modules:
            try:
                importlib.import_module('.'.join([tool, module]))
            except:
                pass
    return tool_instances
