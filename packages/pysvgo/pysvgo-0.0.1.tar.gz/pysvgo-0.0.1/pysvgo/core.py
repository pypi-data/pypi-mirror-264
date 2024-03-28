# core.py
import importlib


class PySvgO:
    # We are going to receive a list of plugins as parameter
    def __init__(self, plugins=None):
        # Checking if plugin were sent
        if plugins is None:
            # If no plugin were set we use our default in a list to loop over
            self._plugins = [importlib.import_module('default', ".").Plugin()]
        else:  # create a list of plugins
            # Import the module and initialise it at the same time; plugin is list member, module name
            self._plugins = [importlib.import_module(plugin, ".").Plugin() for plugin in plugins]

    def run(self):
        print("Starting my application")
        print("-" * 10)
        print("This is my core system")

        # plugins are going to be processed
        for plugin in self._plugins:
            plugin.process(5, 3)

        print("-" * 10)
        print("Ending my application")
        print()
