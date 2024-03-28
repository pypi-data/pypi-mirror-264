"""
Utility functions.

..  autosummary::

    ~myLoadUi
    ~unsaved_changes_alert_dialog
"""

import pathlib

from PyQt5 import QtWidgets

ROOT_PATH = pathlib.Path(__file__).parent


def myLoadUi(ui_file, baseinstance=None, **kw):
    """
    Load a ``.ui`` file for use in building a GUI.
    """
    from PyQt5 import uic

    if isinstance(ui_file, str):
        ui_file = ROOT_PATH / ui_file

    return uic.loadUi(ui_file, baseinstance=baseinstance, **kw)


def unsaved_changes_alert_dialog(parent):
    """Pop-up alert dialog."""
    QtWidgets.QMessageBox.warning(
        parent, "Alert!", "Editor has changes.  Must Accept or Reset first."
    )


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
