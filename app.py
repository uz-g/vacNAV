import ollama
import whisper
import torch
import speech_recognition as sr
import torchaudio
import pyttsx3
import pyaudio
import pyautogui
import sys
import string
import struct
import time
import traceback
from datetime import datetime
import pvporcupine
import pyaudio
import pywifi
from playsound import playsound


# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
# using index of 0 for now: sr.Microphone(device_index=0)


def checkForHotword(text):
    """Checks if the user wants to exit the program."""
    if text.lower() == "exit" or text.lower() == "cancel" or text.lower() == "quit":
        print("Exiting app...")
        sys.exit()
    if text.lower() == "nav":
        break
    time.sleep(999999999)


def recordAndTranscribe():
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

        print("You said:", text)
        # if the text is = to exit or cancel or quit (not case sensitive) then exit the program
        checkForHotword(text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return None


def sendToAi(prompt):
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


# Main program loop
while True:
    prompt = recordAndTranscribe()
    sendToAi(prompt)
