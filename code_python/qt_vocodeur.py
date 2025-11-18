#!/usr/bin/env python



# Fichier : `qt_vocodeur.py`
# 2/4



import numpy as np
from scipy.io import wavfile
from scipy.signal import stft

import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QGraphicsProxyWidget
from PyQt6.QtGui import QKeySequence, QShortcut
import pyqtgraph as pg



##----------------------------------------------------------------------------##

fichier1 = 'media/Diner.wav'
fichier2 = 'media/Extrait.wav'
fichier3 = 'media/Halleluia.wav'

Fs, y = wavfile.read(fichier2)

if y.ndim > 1:
    y = y[:, 0]

# y = y.astype(float)

N = len(y)
t = np.arange(N) / Fs



##----------------------------------------------------------------------------##

# Lancer l'application Qt
app = QtWidgets.QApplication([])

# Créer la fenêtre
win = pg.GraphicsLayoutWidget(title="Vocodeur viewer", size=(1000, 700))
win.setBackground('w')  # Couleur du fond
win.setWindowTitle("Bonjour je fais des tests")
win.show()

# Raccourci pour quitter
quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), win)
quit_shortcut.activated.connect(app.quit)

# button_layout = QtWidgets.QVBoxLayout()

# export_btn = QtWidgets.QPushButton("Export Plot")
# button_layout.addWidget(export_btn)

# button_widget = QtWidgets.QWidget()
# button_widget.setLayout(button_layout)

# proxy = QGraphicsProxyWidget()
# proxy.setWidget(button_widget)
# win.addItem(proxy, row=0, col=1)  # Add the proxy to the layout

# def export_plot():
#     exporter = pg.exporters.ImageExporter(p1.scene())
#     exporter.export('waveform_plot.png')  # Change to 'waveform_plot.svg' for SVG

# export_btn.clicked.connect(export_plot)



##----------------------------------------------------------------------------##

# Tracé du signal original
p1 = win.addPlot(row=0, col=0, title="Signal original")
p1.plot(t, y, pen=pg.mkPen('b', width=0.6)) # 'c' pour cyan, 'm' pour magenta…
# on peut aussi mettre genre ça "#E49ECB"
p1.setLabel('bottom', 'Time', units='s')

# Calcul TFD / FFT
Y = np.fft.fft(y)
f_fft = np.fft.fftshift(np.fft.fftfreq(N, 1 / Fs))
Y_shifted = np.fft.fftshift(Y)

# Afficher TFD
p2 = win.addPlot(row=1, col=0, title="TFFD")
p2.plot(f_fft, np.abs(Y_shifted), pen=pg.mkPen('r', width=0.6))
p2.setLabel('bottom', 'Frequency', units='Hz')
p2.setLabel('left', 'Magnitude')

# Calculer STFT / spectrogramme
f, tt, Z = stft(y, fs=Fs, nperseg=512, noverlap=480, nfft=512)
Sxx = np.abs(Z)
S_db = 20 * np.log10(Sxx + 1e-12)

# Afficher spectrogramme (en créant un ImageItem)
p3 = win.addPlot(row=2, col=0, title="Spectrogramme")
img = pg.ImageItem(S_db)
p3.addItem(img)
img.setPos(tt[0], f[0])  # Image starting position
p3.setLimits(xMin=tt[0], xMax=tt[-1], yMin=f[0], yMax=f[-1])
p3.setAspectLocked(False)
p3.setLabel('left', 'Frequency', units='Hz')
p3.setLabel('bottom', 'Time', units='s')

# color scale
if False:
    hist = pg.HistogramLUTItem()
    hist.setImageItem(img)
    win.addItem(hist, row=2, col=1)

p1.setTitle('Waveform', color='#E49ECB')  # Title color to black
p1.getAxis('left').setPen('#E49ECB')  # Set left Y-axis color to black
p1.getAxis('bottom').setPen('#E49ECB')  # Set bottom X-axis color to black



##----------------------------------------------------------------------------##

# Boucle
sys.exit(app.exec())
