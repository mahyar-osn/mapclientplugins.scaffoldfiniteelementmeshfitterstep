from PySide import QtGui, QtCore

from opencmiss.zinchandlers.scenemanipulation import SceneManipulation

from mapclientplugins.scaffoldfiniteelementmeshfitterstep.handlers.datapointadder import DataPointAdder
from mapclientplugins.scaffoldfiniteelementmeshfitterstep.handlers.datapointadder import DataPointAdder
from mapclientplugins.scaffoldfiniteelementmeshfitterstep.handlers.datapointadder import DataPointAdder

from .ui_scaffoldmeshfitterwidget import Ui_ScaffoldfitterWidget


class ScaffoldMeshFitterWidget(QtGui.QWidget):

    def __init__(self, model, parent=None):
        super(ScaffoldMeshFitterWidget, self).__init__(parent)
        self._ui = Ui_ScaffoldfitterWidget()
        self._ui.setupUi(model.get_shareable_open_gl_widget(), self)
        self._ui.sceneviewer_widget.set_context(model.get_context())

        self._settings = {'view-parameters': {}}

        self._model = model
        self._model.reset()
        self._model.register_time_value_update_callback(self._update_time_value)

