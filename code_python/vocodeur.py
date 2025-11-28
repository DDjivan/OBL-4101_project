#!/usr/bin/env python

# -*- coding: utf-8 -*-



import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt



def tracer_frequence_isolee(s_stft, k_idx, Fs, Fen, Pas_s):
    
    """
    Isole une ligne k de la STFT, reconstruit le signal temporel (ISTFT)
    et trace le résultat (l'oscillation temporelle).
    
    :param s_stft: La matrice STFT complète (complexe)
    :param k_idx: L'indice de la fréquence à isoler (0 à N_fft/2)
    :param Fs: Fréquence d'échantillonnage
    :param Fen: Taille de la fenêtre (nperseg)
    :param Pas_s: Le pas de synthèse utilisé (hop_length_out)
    """
    
    # --- 1. ISOLATION (Votre logique) ---
    # Créer une matrice de zéros de la même taille
    stft_filtree = np.zeros_like(s_stft)
    
    # Copier uniquement la ligne demandée
    stft_filtree[k_idx, :] = s_stft[k_idx, :]
    
    # --- 2. RECONSTRUCTION (ISTFT) ---
    # On reconstruit le signal temporel qui ne contient QUE cette fréquence
    # Note: istft retourne (temps, signal), on récupère les deux
    t_out, s_isole = signal.istft(stft_filtree, fs=Fs, nperseg=Fen, noverlap=Fen - Pas_s)
    
    # --- 3. CALCUL DE LA FRÉQUENCE EN HZ (Pour info) ---
    # La STFT a (n_fft // 2) + 1 lignes.
    n_fft = (s_stft.shape[0] - 1) * 2
    freq_hz = k_idx * Fs / n_fft
    
    # --- 4. TRACÉ ---
    plt.figure(figsize=(12, 5))
    
    # On trace le signal
    plt.plot(t_out, s_isole, label=f"Fréquence k={k_idx} (~{freq_hz:.1f} Hz)")
    
    plt.title(f"Signal Temporel Reconstruit - Fréquence isolée {freq_hz:.1f} Hz")
    plt.xlabel("Temps [s]")
    plt.ylabel("Amplitude")
    plt.grid(True, alpha=0.3)
    plt.legend(loc="upper right")
    
    # ZOOM AUTOMATIQUE
    # Comme c'est une haute fréquence, si on affiche 3 secondes, on verra juste un bloc de couleur.
    # On zoome sur les 50 premières millisecondes pour voir la belle sinusoïde.
    #if t_out[-1] > 0.05:
     #   plt.xlim(0, 0.05)
      #  print("🔍 Zoom automatique sur les 0.05 premières secondes pour visualiser l'onde.")
        
    plt.tight_layout()
    plt.show()







##----------------------------------------------------------------------------##
###### Effets

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



def tempo_sans_pitch(e,Fs,k):

    #Entre
    Fen = 2048 #taille de la fenetre
    Pas_e = 512 #pas de la fenetre



    _, _, e_stft = signal.stft(e,fs=Fs, nperseg=Fen, noverlap=Fen - Pas_e) #calcule la TFCT à partir du signal d'entré (c'est l'equivalent de TFCT.m)


    #tracer_frequence_isolee(e_stft, 100, Fs, Fen, Pas_e)
    """
    Plus de detaille sur e_stft : c'est une matrice de array ou soit k et i quelquonque :
        -e_stft[:, j] Donne une colone de la matrice qui represente une fenetre de la TFCT (precisement la jéme) de durée Fen
        -e_stft[i,:] Donne une ligne de la matrice qui represente pour frequence i l'evolution de sa valeur complexe associé par la TFT au cours du temps
        -e_stft[j,i] Donne le nombre complexe associé à une frequence i de la jéme fft
    """


    #Sortie
    Pas_s = int(Pas_e / k) #pas de la fenetre de sortie

    tracer_frequence_isolee(e_stft, 100, Fs, Fen, Pas_s)

    _, s = signal.istft(e_stft, nperseg=Fen, noverlap=Fen - Pas_s) #si o < i alors quan on recolera les fenetre de maniere plus courte et donc le signal final sera plus court et inversement pour i>o

    return s



def tempo_sans_pitch2(e, Fs, k):
    #Entre
    Fen = 2048 #taille de la fenetre
    Pas_e = 512 #pas de la fenetre
    
    
    _, _, e_stft = signal.stft(e, fs=Fs, nperseg=Fen, noverlap=Fen - Pas_e)  #calcule la TFCT à partir du signal d'entré (c'est l'equivalent de TFCT.m)
    
    """
    Plus de detaille sur e_stft : c'est une matrice de array ou soit k et i quelquonque :
        -e_stft[:, j] Donne une colone de la matrice qui represente une fenetre de la TFCT (precisement la jéme) de durée Fen
        -e_stft[i,:] Donne une ligne de la matrice qui represente pour frequence i l'evolution de sa valeur complexe associé par la TFT au cours du temps
        -e_stft[j,i] Donne le nombre complexe associé à une frequence i de la jéme fft
    """

    Pas_s = int(Pas_e / k) #pas de la fenetre de sortie
    

    
    #debut de la correction de tempo_sans_pitch()
    #Separation de l'amplitude et de la phase
    A = np.abs(e_stft)  # retourne un tableau de la forme e_stft mais avec l'amplitude à la place du nombre complexe
    Phi_e = np.angle(e_stft)    # Pareille mais pour la phase
    
    
    Phi_s = np.zeros_like(Phi_e) #crer un tableau de la forme de e_stft rempli de 0
    
    
    Phi_s[:, 0] = Phi_e[:, 0] #on recopie premiere ligne pas de probleme car c'est entre 0, et premie
    phase_acc = Phi_e[:, 0] #variable qui va compter le nombre de tour total de l'onde pour chaque frequence (tableau)
    
    
    freqs_indices = np.arange(e_stft.shape[0]) # crer une liste rempli de 1 à N de taille du nombre de ligne e_stft 
    
    expected_advance = 2 * np.pi * freqs_indices * Pas_e / Fen # Calcule la phase attendue pour chaque temps de 1 à N 
    
    for t in range(1, e_stft.shape[1]):# Parcours sur les colones 
        
        delta_phi = Phi_e[:, t] - Phi_e[:, t-1] # Pour toute les frequence calcule de la differene de phase (on obtient une liste )


        delta_phi = delta_phi - expected_advance # On retire l'avance théorique pour ne garder que le petit décalage (déviation) par rapport au centre de la fréquence


        delta_phi = (delta_phi + np.pi) % (2 * np.pi) - np.pi # On noramlise en metant les difference de phase entre -pi et pi (utile pour les calcule informatique seulement)


        true_freq_advance = expected_advance + delta_phi # On reconstruit la vraie vitesse de rotation (fréquence instantanée) en rajoutant l'avance théorique à la déviation nettoyée


        phase_acc += true_freq_advance * Pas_s / Pas_e # On met à jour le compteur de tour (accumulateur) en adaptant la vitesse au nouveau temps (si on écarte les fenêtres, l'onde doit tourner plus longtemps)


        Phi_s[:, t] = phase_acc # On sauvegarde la nouvelle phase calculée pour cet instant t
        
    
    s_stft = A * np.exp(1j * Phi_s) # recombinaison de la phase et du module 
    
    #tracer_frequence_isolee(s_stft, 100, Fs, Fen, Pas_s)

    _, s = signal.istft(s_stft, fs=Fs, nperseg=Fen, noverlap=Fen - Pas_s)#si o < i alors quan on recolera les fenetre de maniere plus courte et donc le signal final sera plus court et inversement pour i>o

    return s



def pitch_sans_tampo(e,Fs, k):

    s = pitch_et_tampo(e,Fs,k) #version etirement
    #e = signal.resample(e, n_new) (version zero pading)

    s = tempo_sans_pitch2(s,Fs, 1/k)# On applique l'inverse du facteur pour retrouver la durée d'origine.


    return s



def alien(e,Fs, n):
    s = e
    L=[]
    for k in range(-n,n):
        L.append(pitch_sans_tampo(e,Fs,1+k*0.009))
    
    m = len(e)
    for k in range(len(L)):
        if len(L[k])<m:
            m = len(L[k])

    print(m)

    for k in range(m-10):
        S=0.0
        for j in range(len(L)):
            S = S + L[j][k]
        a=S/len(L)
        #print(f"{k} ieme valeure {a}")
        s[k]=a

    
    
    #s = s / len(L)
    #e = signal.resample(e, n_new) (version zero pading)



    return s



def moyenne(e,Fs, n):
    s = e
    for k in range(len(e)):
        S= 0.0
        i=0
        while i<n and i+k<len(e)-1:
            
            i=i+1
            S = S + s[k+i]
            #print(f"k : {k} | i : {i} | S : {S} ")
        if S != 0:
            s[k] = S / i
    return s



##----------------------------------------------------------------------------##

###### Tests

if __name__ == '__main__':
    fichier1 = 'media/Diner.wav'
    fichier2 = 'media/Extrait.wav'
    fichier3 = 'media/Halleluia.wav'

    Fs, y = wavfile.read(fichier2)

    if y.ndim > 1:
        y = y[:, 0]


    y_robot = tempo_sans_pitch2(y,Fs,2)

    # y_robot = tempo_sans_pitch(y,Fs,0.5)
    # y_robot = tempo_sans_pitch2(y,Fs,1.5)

    # 3. Sauvegarde
    output_filename = 'audio_robotise.wav'
    max_val = np.iinfo(np.int16).max

    if np.max(np.abs(y_robot)) == 0:
        print("⚠️ Signal vide !")
        y_final = np.zeros(len(y_robot), dtype=np.int16)
    else:
        # Normalisation
        y_final = (y_robot / np.max(np.abs(y_robot)) * max_val * 0.9).astype(np.int16)

    # Ecrire dans le fichier de sortie
    wavfile.write(output_filename, Fs, y_final)
    print(f"\n✅ Terminé : {output_filename}")



##----------------------------------------------------------------------------##

###### Autre

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

    f, t, e_stft = signal.stft(y, nperseg=n_fft, noverlap=n_fft-hop_length_in) #calcule la TFCT à partir du signal d'entré (c'est l'equivalent de TFCT.m)


    """
    detaille sur e_stft : c'est une matrice de array ou soit k et i quelquonque
        -e_stft[:, i] Donne une colone de la matrice qui represente une fenetre de la TFCT (precisement la iéme) de durée n_fft
        -e_stft[k,:] Donne une ligne de la matrice qui represente pour frequence l'evolution de sa valeur complexe associé par la TFT au cours du temps
        -e_stft[k,i] Donne le nombre complexe associé à une frequence k de la iéme fft
    """



    #Etape 2 : modification du signal (manipulation de la phase)
    #à rajouter et corriger si on veut ameliorer le code mais ca ne sert à rien pour l'instant

    phase = np.angle(e_stft) # Matrice au meme format que e_stft mais avec des reel represnetant la phase à la place des nombre complexe


    phase_diff = np.diff(phase, axis=1)


    phase_diff = np.concatenate((phase[:, 0].reshape(-1, 1), phase_diff), axis=1)

    # On "déplie" la phase pour éviter les sauts de 2*pi
    # (Note: une implémentation pro complète serait plus complexe ici,
    # mais celle-ci fonctionne pour des facteurs raisonnables)

    # Reconstruction de la nouvelle phase
    # On accumule la phase avec le nouveau rythme
    phase_acc = np.cumsum(phase_diff, axis=1)

    # On recrée le signal complexe avec la A originale mais la nouvelle phase
    e_stft_new = np.abs(e_stft) * np.exp(1j * phase_acc)


    # 3. Synthèse (ISTFT) : On recolle les morceaux avec le nouveau saut
    _, y_stretched = signal.istft(e_stft_new, nperseg=n_fft, noverlap=n_fft-hop_length_out)

    return y_stretched



#genere utulise pour debuger 
