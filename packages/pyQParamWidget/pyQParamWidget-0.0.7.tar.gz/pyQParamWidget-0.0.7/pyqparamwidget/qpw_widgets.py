"""
Constants

.. autosummary::

   ~UNDEFINED_VALUE
   ~QPW_CheckBox
   ~QPW_Choice
   ~QPW_Index
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


class QPW_CheckBox(QPW_Mixin, QtWidgets.QCheckBox):
    """
    Widget type for checkbox or boolean parameter.

    .. autosummary::

       ~qpw_get
       ~qpw_isChanged
       ~qpw_set
    """

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.checkState())

    def qpw_set(self, value):
        """Set the widget's value."""
        self.setCheckState(2 if value else 0)


class QPW_Choice(QPW_Mixin, QtWidgets.QComboBox):
    """
    Widget type for picking from a list.

    .. autosummary::

       ~qpw_get
       ~qpw_isChanged
       ~qpw_set
    """

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.currentText())

    def qpw_set(self, value):
        """Set the widget's value."""
        self.setCurrentText(str(value))


class QPW_Index(QPW_Mixin, QtWidgets.QSpinBox):
    """
    Widget type for adjusting a number between limits.

    .. autosummary::

       ~qpw_get
       ~qpw_isChanged
       ~qpw_set
    """

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.value())

    def qpw_set(self, value):
        """Set the widget's value."""
        self.setValue(value)


class QPW_Text(QPW_Mixin, QtWidgets.QLineEdit):
    """
    Widget type for editing as text.

    .. autosummary::

       ~qpw_get
       ~qpw_isChanged
       ~qpw_set
    """

    def qpw_get(self):
        """Return the value from the widget."""
        return self.original_type(self.text())

    def qpw_set(self, value):
        """Set the widget's value."""
        self.setText(str(value))


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
