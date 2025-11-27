from scipy.io import wavfile
from numpy import arange, ndarray

from os.path import isfile


##----------------------------------------------------------------------------##

class CustomSignalObj():
    def __init__(self, nom_fichier: str):

        if not isfile(nom_fichier):
            notfound: str = f"Erreur `{nom_fichier}` : Fichier inexistant."
            raise FileNotFoundError(notfound)
            return

        try:
            audio = wavfile.read(nom_fichier)
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
