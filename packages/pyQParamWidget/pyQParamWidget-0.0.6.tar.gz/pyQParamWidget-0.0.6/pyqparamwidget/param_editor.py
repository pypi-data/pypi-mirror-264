"""
Parameter Editor: dialog for user-editable application parameters.

.. autosummary::

   ~ParameterEditor
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .qpw_widgets import QPW_CheckBox
from .qpw_widgets import QPW_Choice
from .qpw_widgets import QPW_Index
from .qpw_widgets import QPW_Text
from .utils import unsaved_changes_alert_dialog


class ParameterEditor(QtWidgets.QWidget):
    """
    Edit a set of parameters in a scrollable QWidget.

    * Caller should not close this window if
      ``ParameterEditor.dirty()``
      returns 'True'.

    * Before closing this window:

      * User must ``Accept`` or ``Reset`` any changes (which sets ``dirty=False``).
      * Verify: ``ParameterEditor.dirty() == True``
      * Get values: ``results = ParameterEditor.widgetValues()``

    PARAMETERS

    - parent (object): QWidget parent
    - parameters (dict): Dictionary of ParameterItemBase objects,
      keys are defined by the caller.

    ..  autosummary::

        ~changedValues
        ~dirty
        ~do_accept
        ~do_reset
        ~setDirty
        ~widgetValues
    """

    ui_file = "param_editor.ui"

    def __init__(self, parent, parameters={}):
        from .utils import myLoadUi

        self.parent = parent
        self.parameters = parameters

        super().__init__(parent)
        myLoadUi(self.ui_file, baseinstance=self)
        self.setup()
        self.setDirty(False)  # unsaved changes if True

    def setup(self):
        self.editors = {}
        for k, pitem in self.parameters.items():
            editor = pitem.widget_class(self, parameter=pitem)

            def checkIfDirty(_v):  # _v (new value) ignored here
                """If dirty, then widget value(s) are not as provided."""
                dirty = len(self.changedValues()) > 0
                self.setDirty(dirty)

            if pitem.tooltip != "":
                editor.setToolTip(pitem.tooltip)

            if isinstance(editor, QPW_CheckBox):
                editor.setTristate(on=False)
                editor.setCheckState(2 if pitem.value else 0)
                editor.stateChanged.connect(checkIfDirty)
            elif isinstance(editor, QPW_Choice):
                editor.addItems(pitem.choices)
                editor.setCurrentText(str(pitem.value))
                editor.currentTextChanged.connect(checkIfDirty)
            elif isinstance(editor, QPW_Index):
                editor.setRange(pitem.lo, pitem.hi)
                editor.setValue(pitem.value)
                editor.valueChanged.connect(checkIfDirty)
            elif isinstance(editor, QPW_Text):
                editor.setText(str(pitem.value))
                editor.textChanged.connect(checkIfDirty)
            else:
                raise TypeError(
                    f"Unexpected editor widget: {editor.__class__.__name__}"
                )

            label = QtWidgets.QLabel(self, text=pitem.label)
            self.form_layout.addRow(label, editor)
            self.editors[k] = editor

        self.do_reset()  # sets editor widgets to supplied values
        self.btn_reset.clicked.connect(self.do_reset)
        self.btn_accept.clicked.connect(self.do_accept)

    def changedValues(self):
        """
        Return dictionary with only the changed values.

        .. note:: Result is always empty dictionary when
           ``dirty==True``.  Use :meth:`~pyqparamwidget.param_editor.ParameterEditor.widgetValues()` to get the final values.
        """
        return {
            k: editor.qpw_get()
            for k, editor in self.editors.items()
            if editor.qpw_isChanged()
        }

    def closeEvent(self, event):
        """Do not allow editor to be closed if there are unresolved changes."""
        if self.dirty():
            unsaved_changes_alert_dialog(self)
            event.ignore()
        else:
            event.accept()

    @QtCore.pyqtSlot()
    def do_reset(self):
        """Update widget values from original values and clear dirty flag."""
        # print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")
        for k, editor in self.editors.items():
            editor.qpw_set(self.parameters[k].value)
        self.setDirty(False)

    @QtCore.pyqtSlot()
    def do_accept(self):
        """
        Update original values from widget values and clear dirty flag.
        """
        # print(f"{self.__class__.__name__}.{sys._getframe().f_code.co_name}()")
        for k, v in self.changedValues().items():
            parm = self.parameters[k]
            parm.value = v  # update
        self.setDirty(False)

    def dirty(self) -> bool:
        """Have values been changed?"""
        return self._dirty

    def setDirty(self, dirty: bool):
        """
        Set the dirty (values have changed) flag.  Make it visible.
        """
        self._dirty = dirty
        self.btn_accept.setEnabled(dirty)
        self.btn_reset.setEnabled(dirty)

    def widgetValues(self):
        """Return a dictionary of all widget values."""
        return {k: editor.qpw_get() for k, editor in self.editors.items()}


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
