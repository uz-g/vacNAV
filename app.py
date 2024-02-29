import ollama
import whisper
import torch
import speech_recognition as sr
import torchaudio


# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
# using index of 0 for now: sr.Microphone(device_index=0)
    
    
# Load the model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = whisper.load_model("tiny.en").to(device)



def record_and_transcribe():
    """Records audio from the microphone and returns the transcribed text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak your question:")
        audio = recognizer.listen(source, timeout=3)  # Wait for 3 seconds for input


    try:
        # Perform speech recognition
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None  # Indicate failed transcription

def interact_with_mistral(prompt):
    """Sends the prompt to Mistral AI and prints the responses."""
    if prompt:
        stream = ollama.chat(
            model="mistral", messages=[{'role': 'user', 'content': prompt}], stream=True
        )
        for chunk in stream:
            print(chunk['message']['content'], end='', flush=True)
    else:
        print("No text to send to Mistral AI.")

# Main program loop
while True:
    prompt = record_and_transcribe()
    interact_with_mistral(prompt)
