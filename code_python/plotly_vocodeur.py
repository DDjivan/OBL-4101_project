#!/usr/bin/env python



# Fichier : `plotly_vocodeur.py`
# 0/4



import numpy as np
from scipy.io import wavfile
from scipy.signal import spectrogram

import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import plotly.offline as pyo



##----------------------------------------------------------------------------##

fichier1 = 'media/Diner.wav'
fichier2 = 'media/Extrait.wav'
fichier3 = 'media/Halleluia.wav'

Fs, y = wavfile.read(fichier2)

if y.ndim > 1:
    y = y[:, 0]

# Prepare time and frequency arrays
N = len(y)
t = np.arange(N) / Fs

# Calculate FFT
Y = np.fft.fft(y)
f_fft = np.fft.fftshift(np.fft.fftfreq(N, 1/Fs))
Y_shifted = np.fft.fftshift(Y)

# Calculate spectrogram
f_s, t_s, Sxx = spectrogram(y, Fs, nperseg=128, noverlap=120, nfft=128)

# Create subplots
fig = make_subplots(rows=3, cols=1,
                    subplot_titles=("Original Signal", "FFT", "Spectrogram"))

# Original Signal
fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Original Signal', line=dict(color='blue')),
              row=1, col=1)

# Frequency Domain Representation (FFT)
fig.add_trace(go.Scatter(x=f_fft, y=np.abs(Y_shifted), name='FFT', line=dict(color='red')),
              row=2, col=1)

# Spectrogram
fig.add_trace(go.Heatmap(
    z=10 * np.log10(Sxx + 1e-12),  # Adding a small value to avoid log(0)
    x=t_s,
    y=f_s,
    colorscale='Viridis',
    colorbar=dict(title='Intensity [dB]'),
    name='Spectrogram Plot'
), row=3, col=1)

# Update layout for the figure
fig.update_layout(
    title='Audio Signal Analysis',
    height=800,
    showlegend=False,
)

# Update the y-axes for each subplot
fig['layout']['yaxis']['title'] = 'Amplitude'
fig['layout']['yaxis2']['title'] = 'Magnitude'
fig['layout']['yaxis3']['title'] = 'Frequency [Hz]'

# Display the figure
fig.show()
# pyo.plot(fig, filename='audio_signal_analysis.html', auto_open=True)
