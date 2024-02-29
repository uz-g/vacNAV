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



# Transcribe the prompt audio
result = model.transcribe("whatIsATree.wav", fp16=False)

# print(result)

# Extract the prompt from the result
prompt = result['text']


# Give the prompt to the model
stream = ollama.chat(
    model="mistral",
    messages=[{'role': 'user', 'content': prompt}],
    stream=True,
)

# Print the response
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)

