from scipy.io.wavfile import (read as wav_read, write as wav_write)
from numpy import arange, ndarray

from os.path import isfile, basename, splitext
from os import getcwd



from numpy import abs, max, zeros, int16, iinfo



##----------------------------------------------------------------------------##

class CustomSignalObj():
    def __init__(self, nom_fichier: str) -> None:

        if not isfile(nom_fichier):
            notfound: str = f"Erreur `{nom_fichier}` : Fichier inexistant."
            raise FileNotFoundError(notfound)
            return

        try:
            audio = wav_read(nom_fichier)
        except Exception as e:
            print(f"Erreur `{nom_fichier}` : {e}")
            return

        self.nom: str = nom_fichier
        self.Fs: int = audio[0]
        self.y: ndarray = audio[1]
        self.N: int = len(self.y)
        self.t: ndarray = arange(self.N) / self.Fs

        if self.y.ndim > 1:
            self.y = self.y[:, 0]

        return


    def normalize(self) -> None:
        max_val = iinfo(int16).max

        if max(abs(self.y)) == 0:
            # Signal vide…
            self.y = zeros(len(self.y), dtype=int16)
        else:
            # Normalisation
            self.y = (self.y/max(abs(self.y))*max_val*0.9).astype(int16)

        return

    def export(self) -> None:
        print("exporting!")
        # working_dir: str = getcwd()

        nom_uniquement, extension = splitext(basename(self.nom))

        self.nom = f"{nom_uniquement}_NEW{extension}"

        self.normalize()

        try:
            wav_write(self.nom, self.Fs, self.y)
        except Exception as e:
            print(f"Erreur : {e}")

        return
