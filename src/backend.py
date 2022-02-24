import os
from pathlib import Path
import sys
import json
from PySide2.QtCore import QObject, Slot, Signal


class BackendManager(QObject):
    def __init__(self):
        QObject.__init__(self)

    # SIGNALS
    getSpirals = Signal(str)

    # SLOTS
    @Slot()
    def callSpirals(self):
        spiralDesign = {
            "Rows": 4,
            "Cols": 5,
            "RelatedSpirals": [1,5,10,11]
        }
        self.getSpirals.emit(json.dumps(spiralDesign))
