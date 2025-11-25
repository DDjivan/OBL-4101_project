#!/usr/bin/env python



import sys

from PySide6.QtGui import QAction, QKeySequence

from PySide6.QtWidgets import QMainWindow

from PySide6.QtWidgets import QApplication#, QDialog, QLineEdit
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide6.QtWidgets import QPushButton, QWidget, QInputDialog
from PySide6.QtWidgets import QFileDialog




##----------------------------------------------------------------------------##

def test001() -> None:
    print("Test 001 !")
    return



##----------------------------------------------------------------------------##

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        ##--------------------------------------------------------------------##
        ### Paramètres fenêtres
        self.setWindowTitle("TITRE FENÊTRE")

        # Dimensions
        geometry = self.screen().availableGeometry()
        # self.setFixedSize(geometry.width() * 0.8, geometry.height() * 0.7)
        # self.resize(geometry.width() * 0.8, geometry.height() * 0.7)
        self.resize(1280, 800)
        self.resize(400, 300)



        ##--------------------------------------------------------------------##
        ### En haut
        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("FICHIER")

        # Exit QAction
        exit_action = QAction("QUITTER", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(exit_action)



        ##--------------------------------------------------------------------##
        ### En bas
        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("MESSAGE D'INFORMATION")



        ##--------------------------------------------------------------------##
        ### Au centre
        button_bar = QHBoxLayout()

        btn_1 = QPushButton("BOUTON 1")
        btn_1.clicked.connect(test001)
        button_bar.addWidget(btn_1)

        btn_2 = QPushButton("BOUTON 2")
        btn_2.clicked.connect(self.test002)
        button_bar.addWidget(btn_2)

        btn_3 = QPushButton("BOUTON 3")
        # btn_3.clicked.connect(self._remove_selected_items)
        button_bar.addWidget(btn_3)

        self.btn_4 = QPushButton("BOUTON 4")
        self.btn_4.setCheckable(True)
        # self.btn_4.toggled.connect(self.…)
        button_bar.addWidget(self.btn_4)

        self.btn_5 = QPushButton("BOUTON 5")
        # self.btn_5.clicked.connect(self._capture_sequence)
        self.btn_5.setEnabled(False)
        button_bar.addWidget(self.btn_5)

        # self.btn_6_toggle = QPushButton("Hide Log")
        # self.btn_6_toggle.setCheckable(True)
        # self.btn_6_toggle.toggled.connect(self._toggle_log_visibility)
        # button_bar.addWidget(self.btn_6_toggle)

        input_1 = QInputDialog()
        button_bar.addWidget(input_1)

        input_2 = QFileDialog()
        button_bar.addWidget(input_2)









        button_bar.addStretch(1)

        layout = QVBoxLayout()
        # layout.addWidget(self.status_label)
        # layout.addWidget(self.drop_list)
        layout.addLayout(button_bar)
        # self.log_label = QLabel("Application Log")
        # layout.addWidget(self.log_label)
        # layout.addWidget(self.log_output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)



        ##--------------------------------------------------------------------##
        return

    def test002(self) -> None:
        print("Test 002 !")
        return



##----------------------------------------------------------------------------##

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication([])
    # Create and show the window
    our_window = MainWindow()
    our_window.show()
    # Run the main Qt loop
    sys.exit(app.exec())
