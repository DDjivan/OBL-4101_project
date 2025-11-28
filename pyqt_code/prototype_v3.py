#!/usr/bin/env python



import sys

from PySide6.QtGui import QAction, QKeySequence, QIcon, QShortcut

from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QHBoxLayout, QVBoxLayout,
    QWidget, QTabWidget,
    QPushButton, QInputDialog, QLineEdit,
    QFileDialog,
    QLabel, QComboBox,

    QListWidget, QListWidgetItem,
    QStyle,

    QProgressBar,

    QSlider,
    )

from pathlib import Path

from PySide6.QtCore import (
    Signal,
    Qt,
    QTimer,
    )

from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl

from .graph_library import CustomGraphWindow1, CustomGraphWindow2
from .custom_signal import CustomSignalObj
from .mplgraph_library import show_custom_matplotlib_window



global DEBUG
DEBUG: bool = False



##----------------------------------------------------------------------------##

def placeholder_algorithm(e, Fs: int, k: float):
    if DEBUG: print("placeholder")
    return e

##----------------------------------------------------------------------------##

class DropListCustomWidget(QListWidget):
    files_dropped = Signal(list)

    def __init__(self) -> None:
        super().__init__()
        self.setAcceptDrops(True)
        self.setAlternatingRowColors(True)
        return

    def dragEnterEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
        return

    def dragMoveEvent(self, event) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
        return

    def dropEvent(self, event) -> None:
        if not event.mimeData().hasUrls():
            event.ignore()
            return

        paths: list[str] = []
        for url in event.mimeData().urls():
            local_path = url.toLocalFile()
            if local_path:
                paths.append(local_path)

        if paths:
            self.files_dropped.emit(paths)

        event.acceptProposedAction()
        return



##----------------------------------------------------------------------------##

class CustomMainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        placeholder_icon = QIcon("SVG Godot.svg")
        app_icon = QIcon("app_icon.svg")
        close_icon = QIcon.fromTheme("window-close")
        help_icon = QIcon.fromTheme("help-contents")

        self.speed_algorithm = placeholder_algorithm
        self.pitch_algorithm = placeholder_algorithm
        self.robot_algorithm = placeholder_algorithm
        self.alien_algorithm = placeholder_algorithm
        self.moyen_algorithm = placeholder_algorithm



        ##--------------------------------------------------------------------##
        ###### Paramètres fenêtres
        self.setWindowTitle("QueenVocoder par Djivan & Lilian")
        self.setWindowIcon(app_icon)


        # Dimensions
        # geometry = self.screen().availableGeometry()
        # print(f"{geometry = }")
        self.resize(800, 400)



        ##--------------------------------------------------------------------##
        ###### En haut
        # Menu
        self.the_menu = self.menuBar()
        self.the_menu.setVisible(False)

        file_menu = self.the_menu.addMenu("&Fichier")
        help_menu = self.the_menu.addMenu("Aide")

        toggle_action = QAction(placeholder_icon, "&Menu visible", self)
        toggle_action.setIcon(QIcon.fromTheme("dialog-ok"))
        toggle_action.setShortcut(QKeySequence("Ctrl+Shift+M"))
        toggle_action.triggered.connect(self.toggle_menu_visibility)
        self.addAction(toggle_action)
        file_menu.addAction(toggle_action)

        exit_action = QAction(close_icon, "&Quitter", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.addAction(exit_action)
        file_menu.addAction(exit_action)

        help_action = QAction(help_icon, "À &propos", self)
        # help_action.triggered.connect(FONCTION)
        help_menu.addAction(help_action)



        ##--------------------------------------------------------------------##
        ###### En bas
        # Status Bar
        self.the_status = self.statusBar()
        # self.the_status.showMessage("MESSAGE D'INFORMATION")



        ##--------------------------------------------------------------------##
        ###### Onglet 0

        ### Élément 1
        self.drop_list = DropListCustomWidget()
        self.drop_list.files_dropped.connect(self.handle_dropped_files)

        ### Élément 2
        button_bar = QHBoxLayout()

        add_btn = QPushButton("&Ajouter !")
        add_btn.clicked.connect(self.prompt_for_files)
        del_btn = QPushButton("&Supprimer")
        del_btn.clicked.connect(self.remove_selected_items)
        del_action = QAction("&Quitter", self)

        del_action.setShortcut(QKeySequence("Del"))
        del_action.triggered.connect(self.remove_selected_items)
        self.addAction(del_action)

        button_bar.addWidget(add_btn)
        button_bar.addWidget(del_btn)

        ### Élément 3
        bottom_bar = QHBoxLayout()
        self.switch_btn = QPushButton("É&tape suivante")
        self.switch_btn.clicked.connect(lambda: self.switch_to_tab(1))
        self.switch_btn.setEnabled(False)
        # self.switch_btn.setDisabled(True)
        bottom_bar.addWidget(self.switch_btn)

        ### Container des éléments
        first_tab = QWidget()

        first_layout = QVBoxLayout(first_tab)
        first_layout.addWidget(self.drop_list)
        first_layout.addLayout(button_bar)
        first_layout.addLayout(bottom_bar)



        ###### Onglet 1
        second_tab = QWidget()

        second_layout = QVBoxLayout()
        second_tab.setLayout(second_layout)



        selection_box = QHBoxLayout()
        fichier_indication = QLabel("Fichier d'entrée : ")
        self.fichier_combo = QComboBox(self)
        self.fichier_combo.setPlaceholderText("SÉLECTIONNER UN FICHIER AUDIO")
        selection_box.addWidget(fichier_indication)#, 0, Qt.AlignLeft)
        selection_box.addWidget(self.fichier_combo, 1) # 1 pour stretch

        pitch_box = QHBoxLayout()
        pitch: int = 100
        self.pitch_slider = QSlider(self, pitch)
        self.pitch_slider.setRange(1, 200)
        self.pitch_slider.setValue(pitch)
        self.pitch_slider.setOrientation(Qt.Horizontal)
        self.pitch_slider.valueChanged.connect(
            lambda value: pitch_text.setText(f"Hauteur : {value} %")
            )
        self.pitch_slider.setFixedWidth(400)
        pitch_text = QLabel(f"Hauteur : {self.pitch_slider.value()} %")
        pitch_btn = QPushButton("Réinitialiser")
        pitch_btn.clicked.connect(lambda: self.pitch_slider.setValue(pitch))
        pitch_box.addWidget(pitch_text)
        pitch_box.addWidget(self.pitch_slider)
        pitch_box.addWidget(pitch_btn)

        speed_box = QHBoxLayout()
        speed: int = 100
        self.speed_slider = QSlider(self, speed)
        self.speed_slider.setRange(1, 200)
        self.speed_slider.setValue(speed)
        self.speed_slider.setOrientation(Qt.Horizontal)
        self.speed_slider.valueChanged.connect(
            lambda value: speed_text.setText(f"Vitesse : {value} %")
            )
        self.speed_slider.setFixedWidth(400)
        speed_text = QLabel(f"Vitesse : {self.speed_slider.value()} %")
        speed_btn = QPushButton("Réinitialiser")
        speed_btn.clicked.connect(lambda: self.speed_slider.setValue(speed))
        speed_box.addWidget(speed_text, 0)
        speed_box.addWidget(self.speed_slider, 0)
        speed_box.addWidget(speed_btn, 0)

        # other_box = QHBoxLayout()
        # self.robot_btn = QPushButton("Effet Robot")
        # self.robot_btn.setCheckable(True)
        # self.alien_btn = QPushButton("Effet Alien")
        # self.alien_btn.setCheckable(True)
        # other_box.addWidget(self.robot_btn)
        # other_box.addWidget(self.alien_btn)

        robot_box = QHBoxLayout()
        self.robot: int  = 0
        v_robot_min: int = 0
        v_robot_max: int = 20_000
        self.robot_slider = QSlider(self, self.robot)
        self.robot_slider.setRange(v_robot_min, v_robot_max)
        self.robot_slider.setValue(self.robot)
        self.robot_slider.setOrientation(Qt.Horizontal)
        self.robot_slider.valueChanged.connect(
            lambda value: robot_text.setText(f"Effet Robot : {value} Hz")
            )
        self.robot_slider.setFixedWidth(400)
        robot_text = QLabel(f"Effet Robot : {self.robot_slider.value()} Hz")
        robot_btn = QPushButton("Réinitialiser")
        robot_btn.clicked.connect(lambda:self.robot_slider.setValue(self.robot))
        robot_box.addWidget(robot_text, 0)
        robot_box.addWidget(self.robot_slider, 0)
        robot_box.addWidget(robot_btn, 0)

        alien_box = QHBoxLayout()
        self.alien: int  = 1
        v_alien_min: int = 1
        v_alien_max: int = 10
        self.alien_slider = QSlider(self, self.alien)
        self.alien_slider.setRange(v_alien_min, v_alien_max)
        self.alien_slider.setValue(self.alien)
        self.alien_slider.setOrientation(Qt.Horizontal)
        self.alien_slider.valueChanged.connect(
            lambda value: alien_text.setText(f"Effet Alien : {value} n")
            )
        self.alien_slider.setFixedWidth(400)
        alien_text = QLabel(f"Effet Alien : {self.alien_slider.value()} n")
        alien_btn = QPushButton("Réinitialiser")
        alien_btn.clicked.connect(lambda:self.alien_slider.setValue(self.alien))
        alien_box.addWidget(alien_text, 0)
        alien_box.addWidget(self.alien_slider, 0)
        alien_box.addWidget(alien_btn, 0)

        moyen_box = QHBoxLayout()
        self.moyen: int  = 1
        v_moyen_min: int = 1
        v_moyen_max: int = 200
        self.moyen_slider = QSlider(self, self.moyen)
        self.moyen_slider.setRange(v_moyen_min, v_moyen_max)
        self.moyen_slider.setValue(self.moyen)
        self.moyen_slider.setOrientation(Qt.Horizontal)
        self.moyen_slider.valueChanged.connect(
            lambda value: moyen_text.setText(f"Effet Moyenne : {value} n")
            )
        self.moyen_slider.setFixedWidth(400)
        moyen_text = QLabel(f"Effet Moyenne : {self.moyen_slider.value()} n")
        moyen_btn = QPushButton("Réinitialiser")
        moyen_btn.clicked.connect(lambda:self.moyen_slider.setValue(self.moyen))
        moyen_box.addWidget(moyen_text, 0)
        moyen_box.addWidget(self.moyen_slider, 0)
        moyen_box.addWidget(moyen_btn, 0)





        self.switch_btn2 = QPushButton("&Commencer le calcul")
        self.switch_btn2.clicked.connect(self.start_the_calc)
        self.switch_btn2.setEnabled(False)
        self.fichier_combo.currentIndexChanged.connect(
            lambda: self.switch_btn2.setEnabled(True)
        )



        second_layout.addLayout(selection_box)
        second_layout.addLayout(pitch_box)
        second_layout.addLayout(speed_box)
        # second_layout.addLayout(other_box)
        second_layout.addLayout(robot_box)
        second_layout.addLayout(alien_box)
        second_layout.addLayout(moyen_box)
        second_layout.addWidget(self.switch_btn2, 0, Qt.AlignBottom)

        # .addWidget(container, 0, Qt.AlignHCenter | Qt.AlignVCenter)



        ###### Onglet 2
        third_tab = QWidget()
        third_layout = QVBoxLayout()
        third_tab.setLayout(third_layout)


        self.progress_bar = QProgressBar()

        self.skip_btn = QPushButton("&Skip")
        self.skip_btn.clicked.connect(
            lambda: self.tabs_container.setTabEnabled(3, True)
            )
        self.switch_btn3 = QPushButton("&Voir les résultats")
        self.switch_btn3.clicked.connect(lambda: self.switch_to_tab(3))
        self.switch_btn3.setEnabled(False)



        third_layout.addWidget(self.progress_bar, 0, Qt.AlignVCenter)
        third_layout.addWidget(self.skip_btn, 0, Qt.AlignBottom)
        third_layout.addWidget(self.switch_btn3)#, 0, Qt.AlignBottom)



        ###### Onglet 3
        self.the_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput()
        self.the_player.setAudioOutput(self.audio_output)



        fourth_tab = QWidget()
        fourth_layout = QVBoxLayout()
        fourth_tab.setLayout(fourth_layout)

        self.signal_og = QLabel("Signal original")
        self.signal_og_l = QPushButton("Écouter l'original")
        self.signal_og_l.clicked.connect(
            lambda: self.play_wav(self.s_input.nom)
            )
        self.signal_og_s = QPushButton("Voir l'original")
        self.signal_og_s.clicked.connect(
            self.show_signal_input
            )
        self.signal_og_mpl = QPushButton("Mieux voir l'original")
        self.signal_og_mpl.clicked.connect(
            lambda: show_custom_matplotlib_window(self.s_input)
        )
        self.signal_mo = QLabel("Signal modifié")
        self.signal_mo_l = QPushButton("Écouter le modifié")
        self.signal_mo_l.clicked.connect(
            lambda: self.play_wav(self.s_output.nom)
            )
        self.signal_mo_s = QPushButton("Voir le modifié")
        self.signal_mo_s.clicked.connect(
            self.show_signal_output
            )
        self.signal_mo_mpl = QPushButton("Mieux voir le modifié")
        self.signal_mo_mpl.clicked.connect(
            lambda: show_custom_matplotlib_window(self.s_output)
        )
        self.signal_s = QPushButton("Voir les deux")
        self.signal_s.clicked.connect(self.show_signal_both)


        self.switch_btn4 = QPushButton("&Recommencer")
        self.switch_btn4.clicked.connect(lambda: self.switch_to_tab(1))



        gauche = QVBoxLayout()
        gauche.addWidget(self.signal_og, 0, Qt.AlignHCenter)
        gauche.addWidget(self.signal_og_l)
        gauche.addWidget(self.signal_og_s)
        gauche.addWidget(self.signal_og_mpl)
        droite = QVBoxLayout()
        droite.addWidget(self.signal_mo, 0, Qt.AlignHCenter)
        droite.addWidget(self.signal_mo_l)
        droite.addWidget(self.signal_mo_s)
        droite.addWidget(self.signal_mo_mpl)

        bloc = QHBoxLayout()
        bloc.addLayout(gauche)
        bloc.addLayout(droite)


        fourth_layout.addLayout(bloc)
        fourth_layout.addWidget(self.signal_s)
        fourth_layout.addWidget(self.switch_btn4, 0, Qt.AlignBottom)






        ###### Onglet -1
        text_att = QLabel("Ceci est du texte centré dans le deuxième onglet")
        # text_att.setAlignment(Qt.AlignCenter)


        some_tab = QWidget()
        some_layout = QVBoxLayout()
        # some_layout.addStretch() # push the label to the centre
        some_layout.addWidget(text_att)
        # some_layout.addStretch()
        some_tab.setLayout(some_layout)



        ###### Container de chaque onglet
        self.tabs_container = QTabWidget()

        self.tabs_container.addTab(first_tab, "Fichie&rs audio")
        self.tabs_container.addTab(second_tab, "&Effets audio")
        self.tabs_container.addTab(third_tab, "Chargement")
        self.tabs_container.addTab(fourth_tab, "&Résultat")
        self.tabs_container.addTab(some_tab, "&JSP")

        self.tabs_container.setTabEnabled(1, False)
        self.tabs_container.setTabEnabled(2, False)
        self.tabs_container.setTabEnabled(3, False)
        self.tabs_container.setTabEnabled(4, False)
        self.tabs_container.setTabVisible(4, False)

        self.setCentralWidget(self.tabs_container)



        ##--------------------------------------------------------------------##
        return

    def switch_to_tab(self, number: int) -> None:
        self.tabs_container.setCurrentIndex(number)
        # ou alors :
        # self.tabs.setCurrentWidget(self.second_tab)
        return

    def toggle_menu_visibility(self) -> None:
        is_hidden: bool = self.the_menu.isVisible()
        self.the_menu.setVisible(not is_hidden)
        return



    def contains_path(self, path: Path) -> bool:
        for index in range(self.drop_list.count()):
            existing = self.drop_list.item(index)
            if Path(existing.data(Qt.UserRole)).resolve() == path.resolve():
                return True
        return False

    def update_files(self) -> None:
        n_files: int = self.drop_list.count()

        # for index in range(n_files):
        #     print(self.drop_list.item(index).text())

        if (n_files < 1):
            self.tabs_container.setTabEnabled(1, False)
            self.switch_btn.setEnabled(False)

            return

        self.tabs_container.setTabEnabled(1, True)
        self.switch_btn.setEnabled(True)

        all_items: list[str] = [
            self.drop_list.item(i).text() for i in range(n_files)
            ]
        self.fichier_combo.clear()
        self.switch_btn2.setEnabled(False)
        self.fichier_combo.addItems(all_items)

        return

    def prompt_for_files(self) -> None:
        titre: str = "CHOISIR DES FICHIERS !!"
        types: str = ""
        types: str = "Fichiers audio (*.wav *.mp3)"
        # types: str = "Images (*.jpg *.jpeg *.png *.bmp)"
        path: str = ""
        # path: str = str(Path.home())

        files, _ = QFileDialog.getOpenFileNames(self, titre, path, types)
        if files:
            if DEBUG: print(f"Selected {len(files)} file{'s' if len(files)>=2 else ''}")
            self.add_files(files)
        return

    def handle_dropped_files(self, paths: list[str]) -> None:
        if DEBUG: print(f"Dropped {len(paths)} file{'s' if len(paths)>=2 else ''}")
        self.add_files(paths)

    def add_files(self, paths: list[str]) -> None:
        valid_files: list[str] = []
        for candidate in paths:
            path = Path(candidate)
            if path.is_file():# and path.suffix.lower() in IMAGE_EXTENSIONS:
                if not self.contains_path(path):
                    valid_files.append(path)
            else:
                if DEBUG: print(f"Skipped file: {path}")

        if not valid_files:
            return

        for path in valid_files:
            item = QListWidgetItem(str(path))
            item.setData(Qt.UserRole, str(path))
            item.setToolTip("Hallo ! Je suis le tooltip")
            self.drop_list.addItem(item)

        self.update_files()

        if DEBUG: print(f"+ {len(valid_files)} file{'s' if len(valid_files)>=2 else ''}")
        # self.the_status.showMessage("FICHIERS AJOUTÉS...")
        return

    def remove_selected_items(self) -> None:
        selected_items = self.drop_list.selectedItems()

        if not selected_items:
            return

        for item in selected_items:
            row = self.drop_list.row(item)
            removed_path = item.data(Qt.UserRole) or item.text()
            self.drop_list.takeItem(row)
            if DEBUG: print(f"Removed: {removed_path}")
            if DEBUG: print(f"- 1 file")

        # if self.drop_list.count() == 0:
        #

        self.update_files()
        return



    def start_the_calc(self) -> None:
        self.switch_to_tab(2)
        self.tabs_container.setTabEnabled(2, True)
        self.tabs_container.setTabEnabled(3, False)
        self.switch_btn3.setEnabled(False)

        current_file = self.fichier_combo.currentText()
        self.s_input = CustomSignalObj(current_file)

        self.s_output = CustomSignalObj(current_file)
        # TODO: modify self.s_output here

        # self.speed_algorithm = placeholder_algorithm
        # self.pitch_algorithm = placeholder_algorithm

        if self.speed_slider.value() != 100:
            if DEBUG: print("self.speed_slider.value() != 100")
            self.s_output.y = self.speed_algorithm(
                self.s_output.y,
                self.s_output.Fs,
                self.speed_slider.value()/100
            )

        if self.pitch_slider.value() != 100:
            if DEBUG: print("self.pitch_slider.value() != 100")
            self.s_output.y = self.pitch_algorithm(
                self.s_output.y,
                self.s_output.Fs,
                self.pitch_slider.value()/100
            )

        # if self.robot_btn.isChecked():
        #     self.s_output.y = self.robot_algorithm(
        #         self.s_output.y,
        #         self.s_output.Fs,
        #         150,
        #     )

        # if self.alien_btn.isChecked():
        #     self.s_output.y = self.alien_algorithm(
        #         self.s_output.y,
        #         self.s_output.Fs,
        #         80,
        #     )

        if self.robot_slider.value() != self.robot:
            if DEBUG: print("self.robot_slider.value() != self.robot")
            self.s_output.y = self.robot_algorithm(
                self.s_output.y,
                self.s_output.Fs,
                self.robot_slider.value()
            )

        if self.alien_slider.value() != self.alien:
            if DEBUG: print("self.alien_slider.value() != self.alien")
            self.s_output.y = self.alien_algorithm(
                self.s_output.y,
                self.s_output.Fs,
                self.alien_slider.value()
            )

        if self.moyen_slider.value() != self.moyen:
            if DEBUG: print("self.moyen_slider.value() != self.moyen")
            self.s_output.y = self.moyen_algorithm(
                self.s_output.y,
                self.s_output.Fs,
                self.moyen_slider.value()
            )



        self.s_output.export()

        self.start_loading()
        return

    def start_loading(self) -> None:
        self.valeur_max: int = 10
        # self.intervalle: int = 1000
        self.intervalle: int = 100

        self.progress_bar.setRange(0, self.valeur_max)
        self.progress_bar.setValue(0)

        self.current_value: int = 0

        self.chargement = QTimer()
        self.chargement.timeout.connect(self.update_progress)
        self.chargement.start(self.intervalle) # update toutes les x ms

    def update_progress(self) -> None:
        if self.current_value <= self.valeur_max:
            self.current_value += 1
            self.progress_bar.setValue(self.current_value)

            # self.intervalle = self.intervalle*3/4
            self.intervalle = self.intervalle*4/5
            # self.intervalle = self.intervalle*3/2
            self.chargement.start(self.intervalle)
        else:
            self.chargement.stop()
            self.tabs_container.setTabEnabled(3, True)
            self.switch_btn3.setEnabled(True)
        return



    def play_wav(self, chemin: str) -> None:
        self.wav_url = QUrl.fromLocalFile(Path(chemin).absolute().as_posix())

        if not self.wav_url:
            return

        self.the_player.setSource(self.wav_url)
        self.the_player.play()
        return

    def show_signal_input(self) -> None:
        self.graph_window = CustomGraphWindow1(self.s_input)
        self.graph_window.show()
        return

    def show_signal_output(self) -> None:
        self.graph_window = CustomGraphWindow1(self.s_output)
        self.graph_window.show()
        return

    def show_signal_both(self) -> None:
        self.graph_window = CustomGraphWindow2(self.s_input, self.s_output)
        self.graph_window.show()
        return




##----------------------------------------------------------------------------##

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication([])

    # Create and show the window
    our_window = CustomMainWindow()
    our_window.show()


    ###### INITIALISATION
    chemin1: str = "../code_matlab_fichiers_audio/"
    fichiers1: list[str] = [
        'Diner.wav',
        'Extrait.wav',
        'Halleluia.wav',
    ]
    our_window.add_files(chemin1+f for f in fichiers1)

    # Run the main Qt loop
    DEBUG = True
    sys.exit(app.exec())
