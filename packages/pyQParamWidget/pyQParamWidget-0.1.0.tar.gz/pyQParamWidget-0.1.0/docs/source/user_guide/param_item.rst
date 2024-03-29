.. _guide.ParameterItem:

Parameter Items
===============

An individual *parameter* item has several pieces of information, as described
in the source code documentation, see
:class:`~pyQParamWidget.param_item.ParameterItemBase`. There are different
types, depending on the type of parameter to be edited.  Here is an example of a
*dictionary of Parameter Items*.

.. rubric:: Example dictionary of Parameter Items

.. code-block:: python
    :linenos:

    import pyQParamWidget as qpw
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

ParameterItemCheckbox
------------------------------------

``ParameterItemCheckbox`` uses a ``QCheckBox`` widget to edit a boolean parameter.

.. code-block:: python

    ParameterItemCheckbox(
        "autoscale", True, tooltip="Otherwise, not autoscale."
        )

.. rubric:: Example widget to edit a ParameterItemCheckbox.

.. figure:: ../_static/ParameterItemCheckbox.png
   :width: 40%

   Example widget to edit a ``ParameterItemCheckbox``.

ParameterItemChoice
------------------------------------

``ParameterItemChoice`` uses a ``QComboBox`` widget to select a value from a list of choices.

.. code-block:: python

    ParameterItemChoice(
        "color", "",
        choices=["", "red", "green", "blue"],
        tooltip="Pick a color.",
        )

.. rubric:: Example widget to edit a ParameterItemChoice.

.. figure:: ../_static/ParameterItemChoice.png
   :width: 40%

   Example widget to edit a ``ParameterItemChoice``.  Drop-down
   menu is selected to show the list of choices.

ParameterItemSpinBox
------------------------------------

``ParameterItemSpinBox`` uses a ``QSpinBox`` widget to select a value within limits of ``lo`` and ``hi``.

.. code-block:: python

    ParameterItemSpinBox(
        "x", 50,
        hi=100,
        lo=0,
        tooltip="Choose a value from the range.",
        )

.. rubric:: Example widget to edit a ParameterItemSpinBox.

.. figure:: ../_static/ParameterItemSpinBox.png
   :width: 40%

   Example widget to edit a ``ParameterItemSpinBox``.

ParameterItemText
------------------------------------

``ParameterItemText`` uses a ``QLineEdit`` widget to edit a value as text.

.. code-block:: python

    ParameterItemText("title", "Suggested title", tooltip="Set the title. Be brief.")

.. rubric:: Example widget to edit a ParameterItemText.

.. figure:: ../_static/ParameterItemText.png
   :width: 40%

   Example widget to edit a ``ParameterItemText``. The tooltip is also shown.
