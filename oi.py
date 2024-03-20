from interpreter import OpenInterpreter
from dotenv import load_dotenv
from interpreter.terminal_interface.utils.count_tokens import (
    count_messages_tokens,
    count_tokens,
)
import os
import whisper
import speech_recognition as sr


model = whisper.load_model("base")
load_dotenv()

interpreter = OpenInterpreter()
interpreter.llm.api_key = os.environ.get("API_KEY_ANTHROPIC")

interpreter.llm.model = (
    "claude-3-opus-20240229"  # Tells OI to send messages in OpenAI's format
)
interpreter.system_message += """
Run shell commands with -y so the user doesn't have to confirm them.
"""

interpreter.system_message += """
when opening a website, do it in the default browser using apple script: open location _
"""

whisperModel = whisper.load_model("base")


def recordAndTranscribe(audio):
    speechRecognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speechRecognizer.pause_threshold = 5
        speechRecognizer.adjust_for_ambient_noise(source)
        print("\nAsk your question")
        try:
            audio = speechRecognizer.listen(source, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Sorry, I didn't hear anything. Please try again.")
            return None
    try:
        recognizedText = whisperModel.transcribe(audio)
        if (
            "exit" in recognizedText.lower()
            or "quit" in recognizedText.lower()
            or "goodbye" in recognizedText.lower()
            or "bye" in recognizedText.lower()
        ):
            print("bye!")
            sys.exit()
        print("You said:", recognizedText)
        return recognizedText
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return None
    
def chatWithInterpreter(prompt):
    """Send a message to the interpreter and returns the response."""
    if prompt:
        response = interpreter.chat(prompt)
    
chatWithInterpreter("open wikipedia to the chinggis khan page")