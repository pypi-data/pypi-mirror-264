.. _guide.ParameterEditor:

Parameter Editor
==================================

A parameter dictionary can be edited with a
:class:`~pyQParamWidget.param_editor.ParameterEditor()` widget.

.. seealso:: :ref:`guide.ParameterTree`

Here is one example.

.. rubric:: View of a parameter dictionary using ParameterEditor

.. figure:: ../_static/editor.png
   :width: 60%

   View of ``ParameterEditor`` dialog.

.. rubric::  Full Python application to display parameters in a ParameterEditor widget

.. code-block:: python

    """Parameters Editor Demo Application"""
    import sys

    from PyQt5 import QtWidgets
    import pyQParamWidget as qpw

    # build the dictionary
    parameters = {
        "settings_file": qpw.ParameterItemText(
            label="settings file", value="settings.ini"
        ),
        "server": qpw.ParameterItemChoice(
            label="server URL",
            value="http://localhost",
            choices=[
                "http://localhost",
                "http://localhost.localdoman",
                "http://127.0.0.1",
            ],
        ),
        "autoconnect": qpw.ParameterItemCheckbox(
            label="Autoconnect with server?", value=True
        ),
        "catalog": qpw.ParameterItemText(label="catalog", value="my_catalog"),
        "autoopen": qpw.ParameterItemCheckbox(
            label="Auto open catalog?", value=True
        ),
    }

    # Show ParameterEditor in a PyQt application
    app = QtWidgets.QApplication(sys.argv)
    window = qpw.ParameterEditor(None, parameters)
    window.show()
    print(f"{window.values()=}")
    sys.exit(app.exec())

For the source code documentation, see
:class:`~pyQParamWidget.param_editor.ParameterEditor`.

.. rubric:: EXAMPLE

First, make a dictionary of
:class:`~pyQParamWidget.param_item.ParameterItem` objects.
The keys of the dictionary can be strings or Python objects or
any other structure allowed by Python as dictionary keys.  The
keys, themselves, are not used by ``ParameterEditor``.  They
are only used to identify each of the ``ParameterItem`` objects.

This example defines four objects:

.. code-block:: python
    :linenos:

    parameters = {
        "item1": qpw.param_item.ParameterItemText(
            "title",
            "Suggested title",
            tooltip="Set the title. Be brief."
            ),
        "item2": qpw.param_item.ParameterItemChoice(
            "gain scale",
            "10 uA/V",
            choices=["1 mA/V", "10 uA/V", "100 nA/V", "100 nA/V"],
            tooltip="Pick a gain scale.",
        ),
        "item3": qpw.param_item.ParameterItemCheckbox(
            "wait",
            True,
            tooltip="Should wait at each point?",
        ),
        "item4": qpw.param_item.ParameterItemSpinBox(
            "# of points",
            21,
            lo=2, hi=10_000,
            tooltip="How many points to collect?",
        ),
    }

Next, create the ``ParameterEditor`` object, passing in the ``parent``
object (usually the ``QWidget`` object that will contain this new widget) and
the ``parameters`` dictionary.

.. code-block:: python

    editor = ParameterEditor(parent, parameters)

Finally, add ``editor`` into parent's layout.

.. _guide:get-editor-values:

Get the values from the editor widget
-------------------------------------

The widget's :meth:`~pyQParamWidget.param_editor.ParameterEditor.values`
method returns a dictionary with the accepted parameter values.  The dictionary
keys are the same as the parameter dictionary supplied.

.. code-block:: python

    editor = ParameterEditor(parent, parameters)
    # ...user interaction
    results = editor.values()

.. rubric:: EXAMPLE

Using the ``parameters`` dictionary above, and making no changes in the editor window,
``print(results)`` would return:

.. code-block:: python

    {
        "item1": "Suggested title",
        "item2": "10 uA/V",
        "item3": True,
        "item4": 21
    }

Data types
----------

The editor attempts to report the values in the original data type as given in
the dictionary of parameters.

.. _guide:alert:

Accept and Reset buttons
------------------------

The buttons for **Accept** and **Reset** are enabled when the values
in the editor are different than the supplied parameters.

Before the window can be closed, it is necessary to either **Accept** all
changes or **Reset** all widgets to supplied parameters values.

.. rubric:: View of a ParameterEditor widget with changes.

.. figure:: ../_static/has-changes.png
   :width: 60%

   View of ``ParameterEditor`` widget with changes.

This dialog will be shown if the editor window is requested to close while
changes have not been resolved.

.. rubric:: Alert when request to close editor window with unresolved changes.

.. figure:: ../_static/alert.png
   :width: 60%

   Alert message when trying to close ``ParameterWidget`` with changes.

.. rubric:: Accept

When pressed, the **Accept** button *updates the supplied parameters* from the
widgets.

.. rubric:: Reset

When pressed, the **Reset** button *updates the widgets* from the supplied
parameters.
