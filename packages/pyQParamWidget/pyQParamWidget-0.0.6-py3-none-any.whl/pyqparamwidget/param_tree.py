"""
Parameter Tree: dialog for hierachy of user-editable application parameters.

.. autosummary::

   ~ParameterTree
"""

from uuid import uuid4

from PyQt5 import QtWidgets

from .param_editor import ParameterEditor
from .param_item import ParameterItemBase
from .utils import unsaved_changes_alert_dialog


class ParameterTree(QtWidgets.QDialog):
    """
    Edit a hierachy of parameters in a scrollable QTreeWidget.

    PARAMETERS

    - parameters (dict): Dictionary of :ref:`guide.ParameterItem`.
    - headings ([str]): table headings
      (Only for diagnostic purposes, use ``headings=["heading", "uid"]``.)
    """

    ui_file = "param_tree.ui"

    def __init__(self, parent, parameters={}, headings=["heading"], **kwargs):
        from .utils import myLoadUi

        self.parent = parent
        self.parameters = parameters

        super().__init__(parent, **kwargs)
        myLoadUi(self.ui_file, baseinstance=self)
        self.setup(headings)

    def setup(self, headings):
        self.tree.setColumnCount(len(headings))
        self.tree.setHeaderLabels(headings)
        self.tree.setSortingEnabled(True)
        self.splitter.setStretchFactor(1, 1)  # only self.pane (the editor)
        self.item_xref = {}  # connect subtree item with ParmsDict
        self.last_item = None  # to reset item selection if needed

        def build_subtree(parent, subparms):
            if not self.isParmsDict(subparms):
                for k, v in subparms.items():
                    uid = str(uuid4())
                    self.item_xref[uid] = v if self.isParmsDict(v) else None
                    item = QtWidgets.QTreeWidgetItem(parent, [k, uid])
                    build_subtree(item, v)

        build_subtree(self.tree, self.parameters)
        self.tree.itemSelectionChanged.connect(self.select)

    def closeEvent(self, event):
        """Do not allow dialog to be closed if editor has unresolved changes."""
        if self.dirty():
            unsaved_changes_alert_dialog(self)
            event.ignore()
        else:
            event.accept()

    def dirty(self):
        """Any unaccepted changes in the editor pane?"""
        try:
            return self.pane.dirty()
        except AttributeError:
            return False

    def isParmsDict(self, obj):
        """Is 'obj' a dictionary of Parameter Items?"""
        if isinstance(obj, dict):
            for v in obj.values():
                if not isinstance(v, ParameterItemBase):
                    return False
            return True
        return False

    def select(self):
        """User selected an item from the tree."""
        item = self.tree.currentItem()
        uid = item.text(1)
        parameters = self.item_xref.get(uid)
        if parameters is not None:
            if item == self.last_item:
                return
            if self.last_item is None:
                self.last_item = item

            if self.dirty():
                unsaved_changes_alert_dialog(self)
                self.tree.setCurrentItem(self.last_item)
            else:
                new_editor = ParameterEditor(self, parameters)
                self.splitter.replaceWidget(1, new_editor)
                self.pane = new_editor
                self.last_item = item

    def values(self):
        """Return a dictionary with all the parameter values."""

        def sub_dict(parms):
            result = {}
            for k, v in parms.items():
                if isinstance(v, ParameterItemBase):
                    value = v.value
                else:
                    value = sub_dict(v)
                result[k] = value
            return result

        return sub_dict(self.parameters)


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
