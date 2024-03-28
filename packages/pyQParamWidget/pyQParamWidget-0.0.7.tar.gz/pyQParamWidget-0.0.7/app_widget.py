"""Parameters Editor Demo"""
import sys

from PyQt5 import QtWidgets

PARMS_FILE = "sampler.yml"
PARMS_FILE = "example.yml"


def read_parameter_specifications(parms_file):
    """Read application parameter specifications from YAML file."""
    import yaml

    import pyqparamwidget as qpw

    editors = {
        "QPW_CheckBox": qpw.ParameterItemCheckbox,
        "QPW_Choice": qpw.ParameterItemChoice,
        "QPW_Index": qpw.ParameterItemIndex,
        "QPW_Text": qpw.ParameterItemText,
    }

    with open(parms_file) as f:
        specs = yaml.load(f.read(), Loader=yaml.Loader)
    parms = {}
    for k, v in specs["parameters"].items():
        widget = editors[v.get("widget", "QPW_Text")]
        if "widget" in v:
            v.pop("widget")

        args = [v["label"], v["value"]]
        kwargs = {kw: v[kw] for kw in "widget choices hi lo tooltip".split() if v.get(kw) is not None}
        parms[k] = widget(*args, **kwargs)

    return parms


def main():
    from pyqparamwidget import ParameterEditor

    parms = read_parameter_specifications(PARMS_FILE)
    app = QtWidgets.QApplication(sys.argv)
    window = ParameterEditor(None, parms)
    window.show()
    print(f"{window.widgetValues()=}")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
