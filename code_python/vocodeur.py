##-------------------------Bibioteque-----------------------------------##
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy.io import wavfile
# On garde spectrogram pour l'affichage si besoin, mais pas pour le traitement


import matplotlib
matplotlib.use("qtagg")
import matplotlib.pyplot as plt
from scipy import signal



##---------------------Lecture fichier-------------------------------------##

fichier1 = 'media/Diner.wav'
fichier2 = 'media/Extrait.wav'
fichier3 = 'media/Halleluia.wav'


Fs, y = wavfile.read(fichier2)

if y.ndim > 1:
    y = y[:, 0]




##---------------------Effet-------------------------------------##



def robotize(e, Fs, f_p):
    #Pour robotiser une voix on a besoin de faire de la modulation de signal (source https://emastered.com/fr/blog/what-is-a-vocoder)
    
    #modulation de signal c'est le produit du singal entrant par une sinusoide appelé la porteuse (source cours de mrs loiseau 🫠)
    
    # creation de la porteuse 
    t = np.arange(len(e)) / Fs
    u_p = np.sin(2 * np.pi * f_p * t)

    
    # retour du signal modulé
    return u_p * e





def pitch_et_tampo(e, Fs, k):
    
    f_e = np.fft.fftshift(np.fft.fftfreq(len(e), 1/Fs)) # crer l'abcisse pour la fft(grille des frequence et la met dans le bon ordre )
    
    f_s = np.fft.fftshift(np.fft.fftfreq(int(len(e)/k), 1/Fs)) # crer l'abcisse pour la fft(grille des frequence et la met dans le bon ordre )

    e_fft = np.fft.fftshift(np.fft.fft(e)) # crer les ordonée pour la fft de e 
    
    #on fait ca differement car interp() ne marche que sur des array de flottant or les complexe sont represnté differement en memeoire 
    s_fft_reel = np.interp(f_s, k*f_e, e_fft.real, left=0, right=0)#etire les reel (une ordonné qui etait en abssisse x passera en x * k)
    s_fft_imag = np.interp(f_s, k*f_e, e_fft.imag, left=0, right=0)#pareille pour les imaginaire 
    
    s_fft = s_fft_reel + 1j * s_fft_imag #on recombine les deux 
    s = np.fft.ifft(np.fft.ifftshift(s_fft)).real #on fait la transformé de fourier inverse (on pense à reinversé et à prendre que les reel car il y a des residut complexe)
    
    return s





def tempo_sans_peach(e,Fs,k):

    #Entre
    Fen = 2048 #taille de la fenetre
    Pas_e = 512 #pas de la fenetre 
    
    
    
    _, _, e_stft = signal.stft(y, nperseg=Fen, noverlap=Fen - Pas_e) #calcule la TFCT à partir du signal d'entré (c'est l'equivalent de TFCT.m) 
    
    """
    Plus de detaille sur e_stft : c'est une matrice de array ou soit k et i quelquonque :
        -e_stft[:, j] Donne une colone de la matrice qui represente une fenetre de la TFCT (precisement la jéme) de durée Fen
        -e_stft[i,:] Donne une ligne de la matrice qui represente pour frequence i l'evolution de sa valeur complexe associé par la TFT au cours du temps 
        -e_stft[j,i] Donne le nombre complexe associé à une frequence i de la jéme fft 
    """

   
    #Sortie
    Pas_s = int(Pas_e / k) #pas de la fenetre de sortie 
   
    _, s = signal.istft(e_stft, nperseg=Fen, noverlap=Fen - Pas_s) #si o < i alors quan on recolera les fenetre de maniere plus courte et donc le signal final sera plus court et inversement pour i>o
    
    return s





def pitch_sans_tampo(e,Fs, k):
    
    e = pitch_et_tampo(e,Fs,k) #version etirement
    #e = signal.resample(e, n_new) (version zero pading)
    
    s = tempo(e,Fs, 1/k)# On applique l'inverse du facteur pour retrouver la durée d'origine.
    
    
    return s









##---------------------Ecrire dans le fichier de sortie-------------------------------------##




# 1. Convertir en float
y = y.astype(float) 


# --- Effet 1 : Robot (Utilise np.sin) ---
#y_robot = robotize(y, Fs, 150)

# --- Effet 2 : Chipmunk (Pitch aigu) ---
#y_robot = shift_pitch(y, Fs, 1.5)
y_robot = effet_side(y,Fs,1.5)

# --- Effet 3 : Ralenti (Tempo lent, voix normale) ---
#y_robot = stretch_tempo(y, Fs, factor=1.5)


# 3. Sauvegarde
output_filename = 'audio_robotise.wav'
max_val = np.iinfo(np.int16).max

if np.max(np.abs(y_robot)) == 0:
    print("⚠️ Signal vide !")
    y_final = np.zeros(len(y_robot), dtype=np.int16)
else:
    # Normalisation
    y_final = (y_robot / np.max(np.abs(y_robot)) * max_val * 0.9).astype(np.int16)

wavfile.write(output_filename, Fs, y_final)
print(f"\n✅ Terminé : {output_filename}")













##---------------------Poubelle-------------------------------------##








def effet_side(e, Fs, k):
    
    f = np.fft.fftshift(np.fft.fftfreq(len(e), 1/Fs)) # crer l'abcisse pour la fft(grille des frequence et la met dans le bon ordre )
    

    e_fft = np.fft.fftshift(np.fft.fft(e)) # crer les ordonée pour la fft de e 
    
    #on fait ca differement car interp() ne marche que sur des array de flottant or les complexe sont represnté differement en memeoire 
    s_fft_reel = np.interp(f, f , e_fft.real, left=0, right=0)#etire les reel (une ordonné qui etait en abssisse x passera en x * k)
    s_fft_imag = np.interp(f , f *k, e_fft.imag, left=0, right=0)#pareille pour les imaginaire 
    
    s_fft = s_fft_reel + 1j * s_fft_imag #on recombine les deux 
    s = np.fft.ifft(np.fft.ifftshift(s_fft)).real #on fait la transformé de fourier inverse (on pense à reinversé et à prendre que les reel car il y a des residut complexe)
    
    return s



def shift_pitch2(e, Fs, k):
    
    f = np.fft.fftshift(np.fft.fftfreq(len(e), 1/Fs)) # crer l'abcisse pour la fft(grille des frequence et la met dans le bon ordre )
    

    e_fft = np.fft.fftshift(np.fft.fft(e)) # crer les ordonée pour la fft de e 
    
    #on fait ca differement car interp() ne marche que sur des array de flottant or les complexe sont represnté differement en memeoire 
    s_fft_reel = np.interp(f, f * k , e_fft.real, left=0, right=0)#etire les reel (une ordonné qui etait en abssisse x passera en x * k)
    s_fft_imag = np.interp(f , f * k, e_fft.imag, left=0, right=0)#pareille pour les imaginaire 
    
    s_fft = s_fft_reel + 1j * s_fft_imag #on recombine les deux 
    s = np.fft.ifft(np.fft.ifftshift(s_fft)).real #on fait la transformé de fourier inverse (on pense à reinversé et à prendre que les reel car il y a des residut complexe)
    
    return s


def phase_vocoder_bizzare(y, speed_factor):
    
    # Etape 1 : calcule de la Transformée de Fourier à court terme (TFCT)
    n_fft = 2048 #taille de la fenetre
    hop_length_in = 512 #pas de la fenetre 
    
    hop_length_out = int(hop_length_in / speed_factor) #pas de la fenetre de sortie | si o < i alors quan on recolera les fenetre de maniere plus courte et donc le signal final sera plus court et inversement pour i>o
    
    f, t, Zxx = signal.stft(y, nperseg=n_fft, noverlap=n_fft-hop_length_in) #calcule la TFCT à partir du signal d'entré (c'est l'equivalent de TFCT.m) 
    

    """
    detaille sur Zxx : c'est une matrice de array ou soit k et i quelquonque
        -Zxx[:, i] Donne une colone de la matrice qui represente une fenetre de la TFCT (precisement la iéme) de durée n_fft
        -Zxx[k,:] Donne une ligne de la matrice qui represente pour frequence l'evolution de sa valeur complexe associé par la TFT au cours du temps 
        -Zxx[k,i] Donne le nombre complexe associé à une frequence k de la iéme fft 
    """

   
    
    #Etape 2 : modification du signal (manipulation de la phase)
    #à rajouter et corriger si on veut ameliorer le code mais ca ne sert à rien pour l'instant 
    
    phase = np.angle(Zxx) # Matrice au meme format que Zxx mais avec des reel represnetant la phase à la place des nombre complexe 


    phase_diff = np.diff(phase, axis=1)


    phase_diff = np.concatenate((phase[:, 0].reshape(-1, 1), phase_diff), axis=1)
    
    # On "déplie" la phase pour éviter les sauts de 2*pi
    # (Note: une implémentation pro complète serait plus complexe ici, 
    # mais celle-ci fonctionne pour des facteurs raisonnables)
    
    # Reconstruction de la nouvelle phase
    # On accumule la phase avec le nouveau rythme
    phase_acc = np.cumsum(phase_diff, axis=1)
    
    # On recrée le signal complexe avec la magnitude originale mais la nouvelle phase
    Zxx_new = np.abs(Zxx) * np.exp(1j * phase_acc)
    

    # 3. Synthèse (ISTFT) : On recolle les morceaux avec le nouveau saut
    _, y_stretched = signal.istft(Zxx_new, nperseg=n_fft, noverlap=n_fft-hop_length_out)
    
    return y_stretched