#!/usr/bin/env python



import sys

from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,

    QVBoxLayout,

    QGraphicsProxyWidget,
    )

from PySide6.QtGui import QAction, QKeySequence, QShortcut, QIcon

import pyqtgraph as pg

from .custom_signal import CustomSignalObj



##----------------------------------------------------------------------------##

class CustomGraphWindowAbstract(QMainWindow):
    def __init__(self):
        super().__init__()

        close_icon = QIcon.fromTheme("window-close")

        ##--------------------------------------------------------------------##
        ###### Paramètres fenêtres
        self.setWindowTitle(f"Visualiseur personnalisé :)")
        self.setGeometry(0, 0, 1000, 500)



        ##--------------------------------------------------------------------##
        ###### En haut
        # Menu
        self.the_menu = self.menuBar()
        self.the_menu.setVisible(True)

        file_menu = self.the_menu.addMenu("&Fichier")

        close_action = QAction(close_icon, "Fermer", self)
        close_action.setShortcut(QKeySequence("Ctrl+W"))
        close_action.triggered.connect(self.close)
        self.addAction(close_action)
        file_menu.addAction(close_action)



        ##--------------------------------------------------------------------##
        ###### Au centre
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.graph_widget = pg.GraphicsLayoutWidget()#(title="A")
        self.graph_widget.setBackground('w')

        # …

        layout.addWidget(self.graph_widget)



        ##--------------------------------------------------------------------##
        return

class CustomGraphWindow1(CustomGraphWindowAbstract):
    def __init__(self, s0: CustomSignalObj):
        super().__init__()

        # wg = widget graph
        wg = self.graph_widget.addPlot(row=0, col=0, )#title="jsp")

        wg.setTitle(f"Signal de `{s0.nom}`", color='#E49ECB')
        min_l0 = min(len(s0.t), len(s0.y))
        wg.plot(s0.t[:min_l0], s0.y[:min_l0], pen=pg.mkPen('b', width=0.6))
        wg.setLabel('bottom', 'Time', units='s')
        wg.getAxis('left').setPen('#E49ECB')
        wg.getAxis('bottom').setPen('#E49ECB')

        ##--------------------------------------------------------------------##
        return


class CustomGraphWindow2(CustomGraphWindowAbstract):
    def __init__(self, s1: CustomSignalObj, s2: CustomSignalObj):
        super().__init__()

        # wg = widget graph
        wg = self.graph_widget.addPlot(row=0, col=0)

        wg.setTitle(f"`{s1.nom}` (cyan) et `{s2.nom}` (rouge)", color='#E49ECB')
        min_l1 = min(len(s1.t), len(s1.y))
        wg.plot(s1.t[:min_l1], s1.y[:min_l1], pen=pg.mkPen('c', width=0.6))
        min_l2 = min(len(s2.t), len(s2.y))
        wg.plot(s2.t[:min_l2], s2.y[:min_l2], pen=pg.mkPen('r', width=0.6))

        wg.setLabel('bottom', 'Time', units='s')
        wg.getAxis('left').setPen('#E49ECB')
        wg.getAxis('bottom').setPen('#E49ECB')

        ##--------------------------------------------------------------------##
        return


##----------------------------------------------------------------------------##

if __name__ == '__main__':
    fichier1 = '../code_matlab_fichiers_audio/Diner.wav'
    fichier2 = '../code_matlab_fichiers_audio/Extrait.wav'
    fichier3 = '../code_matlab_fichiers_audio/Halleluia.wav'

    audio2 = CustomSignalObj(fichier2)
    audio1 = CustomSignalObj(fichier1)

    # Create the Qt Application
    app = QApplication([])

    # Create and show the window
    # our_window1 = CustomGraphWindow(audio2)
    our_window1 = CustomGraphWindow1(audio2)
    our_window2 = CustomGraphWindow2(audio2, audio1)
    our_window1.show()
    our_window2.show()

    sys.exit(app.exec())
