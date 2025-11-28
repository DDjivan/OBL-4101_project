#!/usr/bin/env python



from numpy import arange, abs, log10
from numpy.fft import fft, fftshift
from scipy.signal import spectrogram

# import matplotlib
# matplotlib.use('QTAgg')

from matplotlib.pyplot import (
    figure, plot, subplot, title, pcolormesh,
    xlabel, ylabel, xlim, ylim,
    tight_layout, grid,
    axes, axis,
    show
    )

try:
    from .custom_signal import CustomSignalObj
except ImportError:
    try:
        from custom_signal import CustomSignalObj
    except Exception as e:
        print(e)



##----------------------------------------------------------------------------##

def show_custom_matplotlib_window(s0: CustomSignalObj) -> None:

    # pour le spectrogramme
    dégradés = [
        'viridis',  # celui par défaut
        'plasma',
        'cividis',
        'inferno',
        'magma',
        'Blues',
        'Greens',
        'Reds',
        ]

    ###### Courbes
    min_length1 = min(len(s0.t), len(s0.y))
    s0.t = s0.t[:min_length1]
    s0.y = s0.y[:min_length1]



    s0_f = arange(s0.N) * s0.Fs / s0.N
    s0_f = s0_f - s0.Fs / 2

    s0_fft = abs(fftshift(fft(s0.y)))

    s0_f_s, s0_t_s, s0_Sxx = spectrogram(
        s0.y, s0.Fs, nperseg=128, noverlap=120, nfft=128
        )

    s0_Sxx_log = 10*log10(s0_Sxx)



    min_length2 = min(len(s0_f), len(s0_fft))
    s0_f = s0_f[:min_length2]
    s0_fft = s0_fft[:min_length2]



    ###### Tracés
    fig1 = figure(figsize=(10,9), num="Visualiseur matplotlib :)")
    grid(False)
    fig1.gca().axis('off')

    ### En haut
    axes1 = subplot(311)
    grid(False)
    title("Signal original")
    plot(s0.t, s0.y, color="#42b883")
    xlabel("Temps en s")
    ylabel("Amplitude")
    # axes1.axis('off')

    ### Au milieu
    axes2 = subplot(312)
    grid(False)
    title("Transformée de Fourier")
    plot(s0_f, s0_fft, color="#d57db8")
    xlabel("Fréquence en Hz")
    ylabel("Amplitude")
    # axes2.axis('off')

    ### En bas
    axes3 = subplot(313)
    title("Spectrogramme")
    pcolormesh(s0_t_s, s0_f_s, s0_Sxx_log, shading="nearest", cmap=dégradés[1])
    xlabel("Temps en s")
    ylabel("Fréquence en Hz")
    ylim(0, s0.Fs / 2)
    # axes3.axis('off')



    ###### Affichage
    tight_layout()
    # show()
    show(block=False)
    # `False` pour éviter le message suivant :
    # QCoreApplication::exec: The event loop is already running

    return

##----------------------------------------------------------------------------##

if __name__ == "__main__":
    fichier1 = "../code_matlab_fichiers_audio/Diner.wav"
    fichier2 = "../code_matlab_fichiers_audio/Extrait.wav"
    fichier3 = "../code_matlab_fichiers_audio/Halleluia.wav"

    audio1 = CustomSignalObj(fichier1)
    audio2 = CustomSignalObj(fichier2)

    show_custom_matplotlib_window(audio1)
