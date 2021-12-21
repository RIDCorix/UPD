import sys
# def get_tools():
#     manager = PluginManager()
#     manager.setPluginPlaces(["plugins/file_cabinet"])
#     manager.collectPlugins()

#     return [plugin.plugin_object for plugin in manager.getAllPlugins()]

def get_tools():
    import importlib
    tools = ['file_cabinet']
    tool_installation_dir = 'C:/Users/User/UPD/plugins'
    sys.path.append(tool_installation_dir)
    tool_instances = []
    auto_load_modules = ['tasks', 'ui']
    for tool in tools:
        tool_instances.append(importlib.import_module('.'.join([tool, 'tool'])).tool)
        for module in auto_load_modules:
            importlib.import_module('.'.join([tool, module]))
    return tool_instances
