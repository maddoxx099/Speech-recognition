import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSignal, QObject
import threading
from speech_recognition_logic import SpeechRecognition


class Communicate(QObject):
    transcript_update = pyqtSignal(str, str)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.recognizer = SpeechRecognition()
        self.communicate = Communicate()  # Instantiate Communicate here
        self.recognizer_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Real-Time Speech Recognition and Translation")
        self.setGeometry(100, 100, 600, 400)

        self.original_textbox = QTextEdit()
        self.translated_textbox = QTextEdit()
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        layout = QVBoxLayout()
        layout.addWidget(self.original_textbox)
        layout.addWidget(self.translated_textbox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.start_button.clicked.connect(self.start_recognition)
        self.stop_button.clicked.connect(self.stop_recognition)

        self.communicate.transcript_update.connect(self.update_transcripts)

    def start_recognition(self):
        self.recognizer_thread = threading.Thread(target=self.recognizer.start_recognition,
                                                  args=(self.transcript_callback,))
        self.recognizer_thread.start()

    def stop_recognition(self):
        if self.recognizer_thread:
            self.recognizer.stop_recognition()
            self.recognizer_thread.join()

    def transcript_callback(self, original_text, translated_text):
        self.communicate.transcript_update.emit(original_text, translated_text)

    def update_transcripts(self, original_text, translated_text):
        self.original_textbox.append(original_text)
        self.translated_textbox.append(translated_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
