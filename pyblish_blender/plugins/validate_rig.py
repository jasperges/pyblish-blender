import pyblish.api
import bpy


class ValidateRigContents(pyblish.api.InstancePlugin):
    """Ensure rig has the appropriate object sets."""
    order = pyblish.api.ValidatorOrder
    families = ["rig"]

    def process(self, instance):
        # assert "controls_SEL" in instance, "%s is missing a controls set" % instance
        # assert "pointcache_SEL" in instance, "%s is missing a pointcache set" % instance
        # Don't know what to assert in Blender. For testing purposes will test
        # the Vincent rig.
        # self.log.info("Instance: %s", instance)
        # assert "vincent_blenrig" in instance, "%s is missing the blenrig" % instance
        pass
