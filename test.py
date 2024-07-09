import pyaudio
import vosk
import json
import queue
import sys
import threading
from googletrans import Translator

FRAME_RATE = 16000
BUFFER_SIZE = 8000
CHANNELS = 1

MODEL_PATH = "vosk-model-en-in-0.5"

# Load the Vosk model
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, FRAME_RATE)

# Create a queue to hold audio data
audio_queue = queue.Queue()

# Flag to stop the recording
stop_recording = threading.Event()

# Initialize the translator
translator = Translator()


# Function to capture audio data
def capture_audio(stream):
    while not stop_recording.is_set():
        data = stream.read(BUFFER_SIZE, exception_on_overflow=False)
        audio_queue.put(data)


def speech_recognition():
    print("Press 'q' and then Enter to stop recording...")

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=FRAME_RATE,
                    input=True,
                    frames_per_buffer=BUFFER_SIZE)

    # Start a thread to capture audio data
    threading.Thread(target=capture_audio, args=(stream,), daemon=True).start()

    while not stop_recording.is_set():
        # Retrieve and process audio data from the queue
        while not audio_queue.empty():
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result)["text"]
                print(f"Recognized: {text}", flush=True)

                if text:  # Ensure text is not empty
                    try:
                        translated = translator.translate(text, src='en', dest='hi')
                        if translated and translated.text:
                            print(f"Translated: {translated.text}", flush=True)
                    except Exception as e:
                        print(f"Translation error: {e}", flush=True)

    stream.stop_stream()
    stream.close()
    p.terminate()


def listen_for_key_press():
    while True:
        if input().strip().lower() == 'q':
            stop_recording.set()
            break


if __name__ == "__main__":
    print("Starting real-time speech recognition and translation...")
    threading.Thread(target=listen_for_key_press, daemon=True).start()
    speech_recognition()
    print("Recording stopped.")
