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
    sys.path.append("C:/Users/User/UPD/plugins")
    return [importlib.import_module('.'.join([tool, 'tool'])).tool for tool in tools]

        