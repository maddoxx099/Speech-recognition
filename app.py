import tkinter as tk
from tkinter import scrolledtext, ttk
import pyaudio
import vosk
import json
import queue
import threading
from googletrans import Translator

# Constants
FRAME_RATE = 16000
BUFFER_SIZE = 8000
CHANNELS = 1
MODEL_PATH = "vosk-model-en-in-0.5"

# Initialize Vosk model and recognizer
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, FRAME_RATE)

# Initialize translator
translator = Translator()

# Queue for audio data
audio_queue = queue.Queue()

# Event to stop recording
stop_recording = threading.Event()


# Function to capture audio data
def capture_audio(stream):
    while not stop_recording.is_set():
        data = stream.read(BUFFER_SIZE, exception_on_overflow=False)
        audio_queue.put(data)


# Function for speech recognition and translation
def speech_recognition(original_text_box, translated_text_box):
    def process_audio():
        while not stop_recording.is_set():
            while not audio_queue.empty():
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    text = json.loads(result)["text"]
                    original_text_box.insert(tk.END, text + "\n")

                    if text:
                        try:
                            translated = translator.translate(text, src='en', dest='hi')
                            if translated and translated.text:
                                translated_text_box.insert(tk.END, translated.text + "\n")
                        except Exception as e:
                            print(f"Translation error: {e}")

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=FRAME_RATE,
                    input=True,
                    frames_per_buffer=BUFFER_SIZE)

    # Start capturing audio in a separate thread
    threading.Thread(target=capture_audio, args=(stream,), daemon=True).start()

    # Process audio in the main thread
    process_audio()

    # Close audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()


# GUI setup function
def create_gui():
    # Create main window
    window = tk.Tk()
    window.title("Real-time Speech Recognition and Translation")

    # Create text boxes
    original_text_box = scrolledtext.ScrolledText(window, width=40, height=10, wrap=tk.WORD)
    original_text_box.grid(row=0, column=0, padx=10, pady=10)

    translated_text_box = scrolledtext.ScrolledText(window, width=40, height=10, wrap=tk.WORD)
    translated_text_box.grid(row=0, column=1, padx=10, pady=10)

    # Create buttons
    start_button = ttk.Button(window, text="Start", command=lambda: threading.Thread(target=speech_recognition, args=(
    original_text_box, translated_text_box)).start())
    start_button.grid(row=1, column=0, padx=10, pady=10)

    stop_button = ttk.Button(window, text="Stop", command=stop_recording.set)
    stop_button.grid(row=1, column=1, padx=10, pady=10)

    # Start GUI main loop
    window.mainloop()


if __name__ == "__main__":
    create_gui()
