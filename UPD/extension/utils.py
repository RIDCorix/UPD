from yapsy.PluginManager import PluginManager

def get_tools():
    manager = PluginManager()
    manager.setPluginPlaces(["plugins/file_cabinet"])
    manager.collectPlugins()

    return [plugin.plugin_object for plugin in manager.getAllPlugins()]
