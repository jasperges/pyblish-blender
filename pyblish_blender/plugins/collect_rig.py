import pyblish.api
import bpy


class CollectRig(pyblish.api.ContextPlugin):
    """Discover and collect available rigs into the context."""
    order = pyblish.api.CollectorOrder

    def process(self, context):
        for obj in bpy.data.objects:
            if obj.type != 'ARMATURE':
                continue

            name = obj.name
            instance = context.create_instance(name, family="rig")

            # Collect associated nodes
            members = set()
            groups = obj.users_group
            for group in groups:
                members = members.union(group.objects)
            # self.log.info("Members: %s", members)
            instance[:] = members
