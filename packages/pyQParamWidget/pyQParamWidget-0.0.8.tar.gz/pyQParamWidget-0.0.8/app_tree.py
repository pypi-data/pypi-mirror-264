"""
Demonstrate the ParameterTree widget.
"""

import sys

from PyQt5 import QtWidgets

import pyqparamwidget as qpw

sampler = {
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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("before")
        dialog = qpw.ParameterTree(None, parameters=sampler)
        # dialog.show()  # modeless: does not block
        dialog.exec()  # modal: blocks
        # Show the final values of the parameters.
        print("after")
        print(f"{dialog.values()=}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
