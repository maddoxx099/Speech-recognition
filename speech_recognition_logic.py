import vosk
import pyaudio
import json
import queue
import threading
from googletrans import Translator

FRAME_RATE = 16000
BUFFER_SIZE = 8000
CHANNELS = 1
MODEL_PATH = "vosk-model-en-in-0.5"


class SpeechRecognition:
    def __init__(self):
        self.model = vosk.Model(MODEL_PATH)
        self.recognizer = vosk.KaldiRecognizer(self.model, FRAME_RATE)
        self.translator = Translator()
        self.audio_queue = queue.Queue()
        self.stop_recording = threading.Event()

    def capture_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=CHANNELS,
                        rate=FRAME_RATE,
                        input=True,
                        frames_per_buffer=BUFFER_SIZE)

        while not self.stop_recording.is_set():
            data = stream.read(BUFFER_SIZE, exception_on_overflow=False)
            self.audio_queue.put(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def start_recognition(self, transcript_callback):
        threading.Thread(target=self.capture_audio, daemon=True).start()

        while not self.stop_recording.is_set():
            while not self.audio_queue.empty():
                data = self.audio_queue.get()
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    text = json.loads(result)["text"]
                    if text:
                        translated_text = self.translate_text(text)
                        transcript_callback(text, translated_text)

    def stop_recognition(self):
        self.stop_recording.set()

    def translate_text(self, text):
        try:
            translated = self.translator.translate(text, src='en', dest='hi')
            return translated.text if translated else ""
        except Exception as e:
            print(f"Translation error: {e}")
            return ""


if __name__ == "__main__":
    recognizer = SpeechRecognition()
    recognizer.start_recognition(lambda original, translated: print(f"Original: {original}\nTranslated: {translated}"))
