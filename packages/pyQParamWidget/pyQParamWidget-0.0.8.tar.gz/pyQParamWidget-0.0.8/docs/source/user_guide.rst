===========
User Guide
===========

This package simplifies the construction of a ``QWidget`` for the user to edit a
set of parameters (of a PyQt5 application.)  It provides a single
:ref:`guide.ParameterEditor` screen for editing a set of
:ref:`guide.ParameterItem` objects and a :ref:`guide.ParameterTree`
dialog for editing a hierarchical structure with various sets of parameters.

.. _guide.ParameterItem:

Parameter Items
==========================

An individual *parameter* item has several pieces of information, as described
in the source code documentation, see
:class:`~pyqparamwidget.param_item.ParameterItemBase`. There are different
types, depending on the type of parameter to be edited.  Here is an example of a
*dictionary of Parameter Items*.

.. rubric:: Example dictionary of Parameter Items

.. code-block:: python
    :linenos:

    import pyqparamwidget as qpw
    parms = {
        "title": qpw.ParameterItemText("title", "Suggested title"),
        "color": qpw.ParameterItemChoice(
            "color",
            "",
            choices=["", "red", "green", "blue"],
            tooltip="Pick a color.",
        ),
        "autoscale": qpw.ParameterItemCheckbox(
            "autoscale",
            True,
            tooltip="Otherwise, not autoscale.",
        ),
    }

The Parameter Item types are listed next:

``ParameterItemCheckbox``
------------------------------------

.. code-block:: python

    ParameterItemCheckbox(
        "autoscale", True, tooltip="Otherwise, not autoscale."
        )

``ParameterItemChoice``
------------------------------------

.. code-block:: python

    ParameterItemChoice(
        "color", "",
        choices=["", "red", "green", "blue"],
        tooltip="Pick a color.",
        )

``ParameterItemIndex``
------------------------------------

.. code-block:: python

    ParameterItemIndex(
        "x", 50,
        hi=100,
        lo=0,
        tooltip="Choose a value from the range.",
        )

``ParameterItemText``
------------------------------------

.. code-block:: python

    ParameterItemText("title", "Suggested title", tooltip="Set the title. Be brief.")


.. _guide.ParameterEditor:

Parameter Editor
==================================

For the source code documentation, see
:class:`~pyqparamwidget.param_editor.ParameterEditor`.

.. rubric:: EXAMPLE

First make a dictionary of
:class:`~pyqparamwidget.param_item.ParameterItem` objects.
The keys of the dictionary can be strings or Python objects or
any other structure allowed by Python as dictionary keys.  The
keys, themselves, are not used by ``ParameterEditor``.  They
are only used to identify each of the ``ParameterItem`` objects.

This example defines three objects:

.. code-block:: python
    :linenos:

    parameters = {
        "title": qpw.param_item.ParameterItemText(
            "title",
            "Suggested title",
            tooltip="Set the title. Be brief."
            ),
        "color": qpw.param_item.ParameterItemChoice(
            "color",
            "",
            choices=["", "red", "green", "blue"],
            tooltip="Pick a color.",
        ),
        "autoscale": qpw.param_item.ParameterItemCheckbox(
            "autoscale",
            True,
            tooltip="Otherwise, not autoscale.",
        ),
    }

Next, create the ``ParameterEditor`` object, passing in the ``parent``
object (usually the ``QWidget`` object that will contain this new widget) and
the ``parameters`` dictionary.

.. code-block:: python

    panel = ParameterEditor(parent, parameters)

Finally, add ``panel`` into parent's layout.

.. _guide.ParameterTree:

Parameter Tree
==================================

A hierarchy of parameters can be edited using the
:class:`~pyqparamwidget.param_tree.ParameterTree()` dialog. Here is one example.

.. rubric:: View of a hierarchical parameter dictionary using ParameterTree

.. figure:: _static/qpw.png
   :alt: fig.qpw
   :width: 60%

   View of ``ParameterTree`` dialog.

.. rubric:: Python code to construct the example hierarchical parameter dictionary

.. code-block:: python
    :linenos:

    import pyqparamwidget as qpw

    hierarchy = {
        "applications": {
            "tiled": {
                "server": {
                    "settings_file": qpw.ParameterItemText(
                        label="settings file", value="~/.config/settings.ini"
                    ),
                    "catalog": qpw.ParameterItemText(label="catalog", value="bluesky_data"),
                    "url": qpw.ParameterItemText(label="url", value="http://localhost"),
                },
            },
            "other": {
                "demo": qpw.ParameterItemCheckbox("demo mode?", True),
            },
        },
        "UI": {
            "plotting": {
                "autoplot": qpw.ParameterItemCheckbox(
                    label="autoplot",
                    value=True,
                    tooltip="Plot when the run is selected.",
                ),
                "autoselect": qpw.ParameterItemCheckbox(
                    label="autoselect",
                    value=True,
                    tooltip="Automatically select the signals to plot.",
                ),
                "colors": qpw.ParameterItemChoice(
                    label="colors", value="", choices=["", "r", "b", "g", "k"]
                ),
            },
        },
    }

.. rubric::  Python code to display the hierarchy in a ParameterTree dialog

.. code-block:: python
    :linenos:

    dialog = qpw.ParameterTree(None, parameters=hierarchy)
    # dialog.show()  # modeless: does not block
    dialog.exec()  # modal: blocks
    # Show the final values of the parameters, once the dialog is closed.
    print(f"{dialog.values()=}")
