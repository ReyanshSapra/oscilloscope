import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import streamlit as st

samplerate = 44100
duration = 0.1
channels = 1

fig, ax = plt.subplots()
line, = ax.plot([], [])

ax.set_ylim(-1, 1)
ax.grid(True)

time_data = np.arange(0, duration, 1/samplerate)
amplitude_data = np.zeros(int(samplerate * duration))
line.set_data(time_data, amplitude_data)
ax.set_xlim(0, duration)

def update_audio_plot(i):
    global amplitude_data
    try:
        audio_chunk = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, blocking=True, device=2)
        amplitude_data = audio_chunk[:, 0]
        line.set_ydata(amplitude_data)
        return line,
    except sd.PortAudioError as e:
        print(f"Error capturing audio with device 1: {e}")
        return line,

ani = animation.FuncAnimation(fig, update_audio_plot, interval=30, blit=True)
st.pyplot(fig)