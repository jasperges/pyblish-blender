import os
from datetime import datetime
import pyblish.api
import bpy


class ExtractRig(pyblish.api.InstancePlugin):
    """Serialise valid rig."""

    order = pyblish.api.ExtractorOrder
    families = ["rig"]
    hosts = ["blender"]

    def process(self, instance):
        context = instance.context
        context.data["currentFile"] = bpy.data.filepath
        dirname = os.path.dirname(context.data["currentFile"])
        # dirname = os.path.dirname(bpy.data.filepath)
        name, family = instance.data["name"], instance.data["family"]
        date = datetime.now().strftime("%Y%m%dT%H%M%SZ")

        # Find a temporary directory with support for publishing multiple times.
        tempdir = os.path.join(dirname, "temp", date, family, name)
        tempfile = os.path.join(tempdir, name + ".blend")

        self.log.info("Exporting %s to %s" % (instance, tempfile))

        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

        # bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            obj.select = False
        for obj in instance:
            obj.select = True
        bpy.ops.wm.save_as_mainfile(filepath=tempfile, copy=True)
        # cmds.select(instance, noExpand=True)  # `instance` a list
        # cmds.file(tempfile,
        #         type="mayaAscii",
        #         exportSelected=True,
        #         constructionHistory=False,
        #         force=True)

        # Store reference for integration
        instance.set_data("tempdir", tempdir)
