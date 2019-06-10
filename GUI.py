# -*- coding: utf-8 -*-

from ui.MainWindow import MainWindow
from PyQt5 import QtWidgets

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())