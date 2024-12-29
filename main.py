import sys
from pathlib import Path
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    engine.load(Path(__file__).parent / "qml/Main.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)