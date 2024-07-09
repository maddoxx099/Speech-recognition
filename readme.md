# Real-Time Speech Recognition and Translation

This project uses Vosk for speech recognition and Google Translate for real-time translation. The application captures audio from a microphone, transcribes it using the Vosk model, and translates the transcribed text to Hindi using the Google Translate API. The GUI is built using PyQt5.

## Features

- Real-time speech recognition
- Real-time translation from English to Hindi
- User-friendly GUI with start and stop buttons
- Displays original and translated text in real-time

## Requirements

- Python 3.6+
- PyAudio
- Vosk
- Googletrans
- PyQt5

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/speech-recognition-translation.git
   cd speech-recognition-translation

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt

4. **Download the Vosk model:**

    Download a Vosk model from Vosk Models and extract it. Update the MODEL_PATH in recognition.py to the path of the downloaded model.

## Running the Application

1.	**Run the application:**
    python gui.py

2. **Use the GUI:**

- Click the Start button to begin recording and transcribing.
- Click the Stop button to stop recording.
- The original transcript will appear in the left text box.
- The translated text will appear in the right text box.


