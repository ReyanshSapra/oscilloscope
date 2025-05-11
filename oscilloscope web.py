import streamlit as st
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import threading
import time

samplerate = 44100
duration = 0.1
channels = 1
device_index = 2

audio_data_queue = []
is_running = True

def audio_capture_loop():
    global audio_data_queue, is_running
    try:
        while is_running:
            audio_chunk = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=channels, blocking=True, device=device_index)
            audio_data_queue.append(audio_chunk[:, 0])
            if len(audio_data_queue) > 10:
                audio_data_queue.pop(0)
    except sd.PortAudioError as e:
        st.error(f"Error capturing audio: {e}")
        is_running = False

audio_thread = threading.Thread(target=audio_capture_loop)
audio_thread.start()

st.title("Audio Oscilloscope")
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_ylim(-1, 1)
ax.grid(True)

time_data = np.arange(0, duration, 1/samplerate)
placeholder = st.empty()

while is_running:
    if audio_data_queue:
        latest_audio = audio_data_queue[-1]
        line.set_xdata(time_data)
        line.set_ydata(latest_audio)
        ax.set_xlim(0, duration)

        ymin = np.min(latest_audio)
        ymax = np.max(latest_audio)
        if not np.isnan(ymin) and not np.isnan(ymax):
            ax.set_ylim(ymin * 1.2, ymax * 1.2)

        placeholder.pyplot(fig)
    time.sleep(0.05)

is_running = False
audio_thread.join()
