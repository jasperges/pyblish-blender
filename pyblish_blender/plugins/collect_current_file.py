import os
import pyblish.api
import bpy


class CollectBlenderCurrentFile(pyblish.api.ContextPlugin):
    """Inject the current working file into context"""
    order = pyblish.api.CollectorOrder - 0.5
    label = "Blender Current File"
    hosts = ['blender']
    version = (0, 1, 0)

    def process(self, context):
        """Inject the current working file"""
        current_file = bpy.data.filepath
        context.set_data('currentFile', value=current_file)
        # For backwards compatibility
        context.set_data('current_file', value=current_file)
