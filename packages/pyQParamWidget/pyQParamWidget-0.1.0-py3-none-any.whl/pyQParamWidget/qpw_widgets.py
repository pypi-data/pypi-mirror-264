"""
Constants

.. autosummary::

   ~UNDEFINED_VALUE
   ~QPW_CheckBox
   ~QPW_Choice
   ~QPW_SpinBox
   ~QPW_Mixin
   ~QPW_Text

.. note:: The ``QPW_`` prefix: pyQParamWidget

:see: https://www.pythonguis.com/tutorials/pyqt-dialogs/
"""

from PyQt5 import QtWidgets

UNDEFINED_VALUE = object
"""For comparison with user input, avoids comparison with an explicit value."""


class QPW_Mixin:
    """
    Mixin class for all QPW widgets.

    .. autosummary::

       ~qpw_get
       ~qpw_isChanged
       ~qpw_set
       ~qpw_setup
    """

    parameters = UNDEFINED_VALUE
    """ParameterItemBase object (passed by parent)."""

    original_type = UNDEFINED_VALUE
    """Python object type to cast widget values."""

    def __init__(self, *args, parameter=None, **kwargs):
        self.parameter = parameter
        self.original_type = type(parameter.value)
        super().__init__(*args, **kwargs)

    def qpw_isChanged(self):
        """Is the widget value different than the original?"""
        return self.qpw_get() != self.parameter.value

    def qpw_get(self):
        """Return the value from the widget."""
        raise NotImplementedError("Define in the subclass.")

    def qpw_set(self, value):  # noqa
        """Set the widget's value."""
        raise NotImplementedError("Define in the subclass.")

    def qpw_setup(self, pitem, slot):  # noqa
        """
        Widget-specific setup details.

        PARAMETERS

        - pitem (obj): ParameterItem instance
        - slot (obj): Function (Qt slot) to call when widget value changes.
          Connect signal and slot in a subclass as needed since each widget
          class has a different name for the signal to be used.
        """
        if pitem.tooltip != "":
            self.setToolTip(pitem.tooltip)
        self.qpw_set(pitem.value)


class QPW_CheckBox(QPW_Mixin, QtWidgets.QCheckBox):
    """
    Widget type for checkbox or boolean parameter.

    .. autosummary::

       ~qpw_get
       ~qpw_isChanged
       ~qpw_set
       ~qpw_setup
    """

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.checkState())

    def qpw_set(self, value):
        """Set the widget's value."""
        self.setCheckState(2 if value else 0)

    def qpw_setup(self, pitem, slot):
        self.setTristate(on=False)
        self.stateChanged.connect(slot)
        super().qpw_setup(pitem, slot)


class QPW_Choice(QPW_Mixin, QtWidgets.QComboBox):
    """
    Widget type for picking from a list.

    .. autosummary::

       ~qpw_get
       ~qpw_isChanged
       ~qpw_set
       ~qpw_setup
    """

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.currentText())

    def qpw_set(self, value):
        """Set the widget's value."""
        self.setCurrentText(str(value))

    def qpw_setup(self, pitem, slot):
        self.addItems(pitem.choices)
        self.currentTextChanged.connect(slot)
        super().qpw_setup(pitem, slot)


class QPW_SpinBox(QPW_Mixin, QtWidgets.QSpinBox):
    """
    Widget type for adjusting a number between limits.

    .. autosummary::

       ~qpw_get
       ~qpw_isChanged
       ~qpw_set
       ~qpw_setup
    """

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.value())

    def qpw_set(self, value):
        """Set the widget's value."""
        self.setValue(value)

    def qpw_setup(self, pitem, slot):
        self.setRange(pitem.lo, pitem.hi)
        self.valueChanged.connect(slot)
        super().qpw_setup(pitem, slot)


class QPW_Text(QPW_Mixin, QtWidgets.QLineEdit):
    """
    Widget type for editing as text.

    .. autosummary::

       ~qpw_get
       ~qpw_isChanged
       ~qpw_set
       ~qpw_setup
    """

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.text())

    def qpw_set(self, value):
        """Set the widget's value."""
        self.setText(str(value))

    def qpw_setup(self, pitem, slot):
        self.textChanged.connect(slot)
        super().qpw_setup(pitem, slot)


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
