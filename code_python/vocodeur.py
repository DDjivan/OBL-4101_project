#!/usr/bin/env python



# Fichier : `vocodeur.py`
# 3/4
#
# Programme principal réalisant un vocodeur de phase et permettant de :
#
# 1. modifier le tempo (la vitesse de "prononciation")
#    sans modifier le pitch (fréquence fondamentale de la parole)
#
# 2. modifier le pitch sans modifier la vitesse
#
# 3. "robotiser" une voix
#



import numpy as np
from scipy.io import wavfile
from scipy.signal import spectrogram

import matplotlib
matplotlib.use("qtagg")
import matplotlib.pyplot as plt



##----------------------------------------------------------------------------##

fichier1 = 'media/Diner.wav'
fichier2 = 'media/Extrait.wav'
fichier3 = 'media/Halleluia.wav'

Fs, y = wavfile.read(fichier2)

# Remarque : si le signal est en stéréo, ne traiter qu'une seule voie à la fois
if y.ndim > 1:
    y = y[:, 0]



# Courbes
N = len(y)
t = np.arange(N) / Fs
f = np.arange(N) * Fs / N
f = f - Fs / 2


# Tracés
plt.figure(1)

# Tracé du signal original
plt.subplot(311)
plt.plot(t, y)
plt.title('Signal original')

plt.subplot(312)
plt.plot(f, np.abs(np.fft.fftshift(np.fft.fft(y))))

# plt.subplot(313)
# f_s, t_s, Sxx = spectrogram(y, Fs, nperseg=128, noverlap=120, nfft=128)
# plt.pcolormesh(t_s, f_s, 10 * np.log10(Sxx), shading='nearest')
# plt.ylabel('Frequency [Hz]')
# plt.xlabel('Time [sec]')
# plt.title('Spectrogram')
# plt.ylim(0, Fs / 2)

plt.show()
