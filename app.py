import ollama
import whisper
import speech_recognition as sr
import pyaudio
import string
import time
from datetime import datetime
import os
import sys
wakeWord = "assist"


def record_and_transcribe():
    """Records audio from the microphone and returns the transcribed text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 5
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("\nAsk your question")  # print new line then speak
        try:
            audio = recognizer.listen(source, phrase_time_limit=3)  # Wait for input
        except sr.WaitTimeoutError:
            print("Sorry, I didn't hear anything. Please try again.")
            return None  # Indicate no audio received

    try:
        # Perform speech recognition
        text = recognizer.recognize_google(audio)
        if "exit" in text.lower() or "quit" in text.lower() or "goodbye" in text.lower() or "bye" in text.lower():
            print("bye!")
            sys.exit()
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return None


def send_to_ai(prompt):
    """Sends the prompt to AI and prints the responses."""
    if prompt:
        stream = ollama.chat(
            model="stablelm-zephyr",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        for chunk in stream:
            response = chunk["message"]["content"]
            print(response, end="", flush=True)


# Function to check if the user pressed the activation key combination
def activation_callback():
    prompt = record_and_transcribe()
    send_to_ai(prompt)


def detect_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"\nListening for wake word '{wakeWord}'...")
        audio = recognizer.listen(
            source, phrase_time_limit=3
        )  # Listen for up to 3 seconds

    try:
        detectedText = recognizer.recognize_google(audio, show_all=False)
        print(f"Debug: detected text = {detectedText}")
        lowerCaseWakeWord = detectedText.lower()
        
        
        if wakeWord in lowerCaseWakeWord:
            print("Wake word detected!")
            return True
        else:
            if "exit" in lowerCaseWakeWord or "quit" in lowerCaseWakeWord or "goodbye" in lowerCaseWakeWord or "bye" in lowerCaseWakeWord:
                print("Goodbye!")
                sys.exit()
            return False
    except sr.UnknownValueError:
        print("No audio detected")
        return False
    except sr.RequestError as error:
        print(
            f"Could not request results from Google Speech Recognition service; {error}"
        )
        return False


while (
    True
):  # detect the wake word then activate the assistant, run it twice before detecting again
    if detect_wake_word():
        print("Assistant activated!")
        activation_callback()
        activation_callback()
    else:
        print(f"debug: '{wakeWord}' not detected")
        continue
