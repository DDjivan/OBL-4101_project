#!/usr/bin/env python



import sys

from PySide6.QtWidgets import QApplication

from pyqt_code.prototype_v3 import CustomMainWindow
from code_python.vocodeur import tempo_sans_pitch, pitch_sans_tampo



##----------------------------------------------------------------------------##

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication([])

    # Create and show the window
    our_window = CustomMainWindow()
    our_window.show()


    ###### INITIALISATION
    chemin1: str = "code_matlab_fichiers_audio/"
    fichiers1: list[str] = [
        'Diner.wav',
        'Extrait.wav',
        'Halleluia.wav',
    ]
    our_window.add_files(chemin1+f for f in fichiers1)
    our_window.add_files(fichiers1)

    our_window.speed_algorithm = tempo_sans_pitch
    our_window.pitch_algorithm = pitch_sans_tampo

    # Run the main Qt loop
    sys.exit(app.exec())
