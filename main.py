# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys


import requests
import pymodbus.client.tcp
import pymodbus.client.serial
import pymodbus.constants
import pymodbus.payload


from PySide2.QtGui import QGuiApplication
from PySide2.QtCore import QObject, Slot, Signal
from PySide2.QtQml import QQmlApplicationEngine
import PySide2.QtMultimedia
from src.backend import BackendManager

if __name__ == "__main__":
    os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backManager = BackendManager(app)
    engine.rootContext().setContextProperty("backend", backManager)
    engine.quit.connect(app.quit)

    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())