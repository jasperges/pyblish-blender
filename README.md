### ![](https://cloud.githubusercontent.com/assets/2152766/6998101/5c13946c-dbcd-11e4-968b-b357b7c60a06.png)

[![Build Status](https://travis-ci.org/pyblish/pyblish-blender.svg?branch=master)](https://travis-ci.org/pyblish/pyblish-blender)

Pyblish integration for Blender.

<br>
<br>
<br>

### What is included?

A set of common plug-ins and functions shared across other integrations - such as getting the current working file. It also visually integrates Pyblish into the File-menu for easy access.

- Common [plug-ins](https://github.com/pyblish/pyblish-blender/tree/master/pyblish_blender/plugins)
- Common [functionality](https://github.com/pyblish/pyblish-blender/blob/master/pyblish_blender/__init__.py)
- File-menu shortcut

<br>
<br>
<br>

### Installation

pyblish-blender depends on [pyblish-base](https://github.com/pyblish/pyblish-base) and is available via PyPI.

```bash
$ pip install pyblish-blender
```

You may also want to consider a graphical user interface, such as [pyblish-qml](https://github.com/pyblish/pyblish-qml) or [pyblish-lite](https://github.com/pyblish/pyblish-lite).

<br>
<br>
<br>

### Usage

To get started using pyblish-blender, run `setup()` at startup of your application.

```python
# 1. Register your favourite GUI
import pyblish.api
pyblish.api.register_gui("pyblish_qml")

# 2. Set-up Pyblish for blender
import pyblish_blender
pyblish_blender.setup()
```

<br>
<br>
<br>

### Documentation

- [Under the hood](#under-the-hood)
- [Manually show GUI](#manually-show-gui)
- [No menu-item](#no-menu-item)
- [Teardown pyblish-blender](#teardown-pyblish-blender)
- [No GUI](#no-gui)

<br>
<br>
<br>

##### Under the hood

The `setup()` command will:

1. Register `blender` as as a ["host"](http://api.pyblish.com/pages/Plugin.hosts.html) to Pyblish, allowing plug-ins to be filtered accordingly.
2. Append a new menu item, "Publish" to your File-menu
3. Register a minimal set of plug-ins that are common across all integrations.

![image](https://cloud.githubusercontent.com/assets/3788756/24167740/279d5346-0e78-11e7-8f7d-2c524372a911.png)

<br>
<br>
<br>

##### No menu-item

Should you not want a menu-item, pass `menu=False`.

```python
import pyblish_blender
pyblish_blender.setup(menu=False)
```

<br>
<br>
<br>

##### Manually show GUI

The menu-button is set to run `show()`, which you may also manually call yourself, such as from a button.

```python
import pyblish_blender
pyblish_blender.show()
```

<br>
<br>
<br>

##### Teardown pyblish-blender

To get rid of the menu, and completely remove any trace of pyblish-blender from your blender session, run `teardown()`.

```python
import pyblish_blender
pyblish_blender.teardown()
```

This will do the opposite of `setup()` and clean things up for you.

<br>
<br>
<br>

##### No GUI

In the event that no GUI is registered upon running `setup()`, the button will provide the *user* with this information on how they can get up and running on their own.

*This is not implemented yet.*

##### TODO

Turn pyblish-blender into a proper Blender addon.
