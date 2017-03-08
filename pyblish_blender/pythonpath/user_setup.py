def setup_pyblish_blender():
    try:
        __import__("pyblish_blender")

    except ImportError:
        import traceback
        print("pyblish-blender: Could not load integration: {exc}".format(
              exc=traceback.format_exc())
             )
    else:
        import pyblish_blender
        pyblish_blender.setup()


def register():
    setup_pyblish_blender()


if __name__ == '__main__':
    register()
