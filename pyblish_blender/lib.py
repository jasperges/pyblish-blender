# Standard library
import os
import sys
import inspect
import contextlib

# Pyblish libraries
import pyblish
import pyblish.api
import pyblish_qml.api
# import pyblish_lite

# Host libraries
import bpy

# Local libraries
from . import plugins

self = sys.modules[__name__]
self._has_been_setup = False
self._has_menu = False
self._registered_gui = None


class ShowPyblish(bpy.types.Operator):
    """Show the Pyblish UI."""
    bl_idname = "wm.pyblish"
    bl_label = "Pyblish"

    def execute(self, context):
        import pyblish_blender
        pyblish_blender.show()
        return {'FINISHED'}


def setup(menu=True):
    """Setup integration

    Registers Pyblish for Blender plug-ins and appends an item to the File-menu

    Attributes:
        console (bool): Display console with GUI
        port (int, optional): Port from which to start looking for an
            available port to connect with Pyblish QML, default
            provided by Pyblish Integration.

    """

    if self._has_been_setup:
        teardown()

    register_classes()
    register_plugins()
    register_host()
    pyblish.api.register_gui("pyblish_qml")

    if menu:
        add_to_filemenu()
        self._has_menu = True

    self._has_been_setup = True
    print("Pyblish loaded successfully.")


def show():
    """Try showing the most desirable GUI

    This function cycles through the currently registered
    graphical user interfaces, if any, and presents it to
    the user.

    """

    return (_discover_gui() or _show_no_gui)()


def _discover_gui():
    """Return the most desirable of the currently registered GUIs"""

    # Prefer last registered
    guis = reversed(pyblish.api.registered_guis())

    for gui in guis:
        try:
            gui = __import__(gui).show
        except (ImportError, AttributeError):
            continue
        else:
            return gui


def teardown():
    """Remove integration"""
    if not self._has_been_setup:
        return

    deregister_classes()
    deregister_plugins()
    deregister_host()

    if self._has_menu:
        remove_from_filemenu()
        self._has_menu = False

    self._has_been_setup = False
    print("pyblish: Integration torn down successfully")


def register_classes():
    """Register Blender classes."""
    bpy.utils.register_class(ShowPyblish)


def deregister_classes():
    """Unregister Blender classes."""
    bpy.utils.unregister_class(ShowPyblish)


def deregister_plugins():
    # Register accompanying plugins
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.deregister_plugin_path(plugin_path)
    print("pyblish: Deregistered %s" % plugin_path)


def register_host():
    """Register supported hosts"""
    pyblish.api.register_host("blender")


def deregister_host():
    """Register supported hosts"""
    pyblish.api.deregister_host("blender")


def register_plugins():
    # Register accompanying plugins
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.register_plugin_path(plugin_path)
    print("pyblish: Registered %s" % plugin_path)


def pyblish_menu_draw(self, context):
    """Draw the Pyblish entry in the file menu."""
    self.layout.separator()
    self.layout.operator("wm.pyblish")


def add_to_filemenu():
    bpy.types.INFO_MT_file.append(pyblish_menu_draw)


def remove_from_filemenu():
    """Remove Pyblish from file menu"""
    bpy.types.INFO_MT_file.remove(pyblish_menu_draw)


@contextlib.contextmanager
def maintained_selection():
    """Maintain selection during context

    Example:
        >>> with maintained_selection():
        ...     # Modify selection
        ...     bpy.ops.object.select_all(action='SELECT')
        >>> # Selection restored

    """

    previous_selection = [obj for obj in bpy.data.objects if obj.select]
    active_object = bpy.context.scene.objects.active
    try:
        yield
    finally:
        if previous_selection:
            for obj in previous_selection:
                obj.select = True
        else:
            bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = active_object


@contextlib.contextmanager
def maintained_time():
    """Maintain current time during context

    Example:
        >>> with maintained_time():
        ...    bpy.ops.render.opengl(animation=True)
        >>> # Time restored

    """

    current_frame = bpy.context.scene.frame_current
    try:
        yield
    finally:
        bpy.context.scene.frame_set(current_frame)


def _show_no_gui():
    """Popup with information about how to register a new GUI

    In the event of no GUI being registered or available,
    this information dialog will appear to guide the user
    through how to get set up with one.

    """
    # TODO
    return

    messagebox.setWindowTitle("Uh oh")
    messagebox.setText("No registered GUI found.")

    if not pyblish.api.registered_guis():
        messagebox.setInformativeText(
            "In order to show you a GUI, one must first be registered. "
            "Press \"Show details...\" below for information on how to "
            "do that.")

        messagebox.setDetailedText(
            "Pyblish supports one or more graphical user interfaces "
            "to be registered at once, the next acting as a fallback to "
            "the previous."
            "\n"
            "\n"
            "For example, to use Pyblish Lite, first install it:"
            "\n"
            "\n"
            "$ pip install pyblish-lite"
            "\n"
            "\n"
            "Then register it, like so:"
            "\n"
            "\n"
            ">>> import pyblish.api\n"
            ">>> pyblish.api.register_gui(\"pyblish_lite\")"
            "\n"
            "\n"
            "The next time you try running this, Lite will appear."
            "\n"
            "See http://api.pyblish.com/register_gui.html for "
            "more information.")

    else:
        messagebox.setInformativeText(
            "None of the registered graphical user interfaces "
            "could be found."
            "\n"
            "\n"
            "Press \"Show details\" for more information.")

        messagebox.setDetailedText(
            "These interfaces are currently registered."
            "\n"
            "%s" % "\n".join(pyblish.api.registered_guis()))
