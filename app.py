import ollama
import whisper
import speech_recognition as sr
import pyaudio
import string
import time
from datetime import datetime
import os
import sys
import pyautogui
import subprocess
import webbrowser
import validators
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from interpreter import interpreter

# Load the .env
from dotenv import load_dotenv
load_dotenv()

interpreter.llm.api_key = os.environ.get("API_KEY")
wakeWord = "assist"
defaultBrowser = "Arc"

interpreter.llm.model = "openai/gpt-3.5-turbo" # Tells OI to send messages in OpenAI's format


def record_and_transcribe():
    """Records audio from the microphone and returns the transcribed text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 5
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("\nAsk your question")  # print new line then speak
        try:
            audio = recognizer.listen(source, phrase_time_limit=5)  # Wait for input
        except sr.WaitTimeoutError:
            print("Sorry, I didn't hear anything. Please try again.")
            return None  # Indicate no audio received

    try:
        # Perform speech recognition
        text = recognizer.recognize_google(audio)
        if (
            "exit" in text.lower()
            or "quit" in text.lower()
            or "goodbye" in text.lower()
            or "bye" in text.lower()
        ):
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
        print(prompt)
        interpreter.chat(prompt)
        print("done")
        



# Function to check if the user pressed the activation key combination
def activation_callback():
    prompt = record_and_transcribe()
    assistant_action(prompt)


def open_app(app_name=defaultBrowser):
    """Opens the specified app.

    Args:
        app_name (string): the name of the app to open
    """
    subprocess.call(["open", "-a", app_name])


def open_website(website):
    """Opens the specified website in the default mac browser.

    Args:
        website (string): the URL of the website to open
    """


    results = []
    for result in search(website, num=10, stop=10, pause=1, safe="on", lang="en", country='us'):
        results.append(result)
        
    link = results[0].splitlines()
    webbrowser.open_new_tab(link[0])
    print(results)

    


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
            if (
                "exit" in lowerCaseWakeWord
                or "quit" in lowerCaseWakeWord
                or "goodbye" in lowerCaseWakeWord
                or "bye" in lowerCaseWakeWord
            ):
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

def assistant_action(prompt):
    """Perform the action based on the user's prompt.

    Args:
        prompt (string): the user's prompt
    """
   
    if prompt:
        if "open" in prompt:
            if not open_app(prompt.replace("open", "").strip()):
                open_website(prompt.replace("open", "").strip())
        elif "search" in prompt:
            prompt = prompt.replace("search", "")
            open_website(prompt)
        else:
            send_to_ai(prompt)

# send_to_ai(record_and_transcribe())


# interpreter.system_message += """
# Run shell commands with -y so the user doesn't have to confirm them.
# """


interpreter.chat("set system theme to dark mode")

