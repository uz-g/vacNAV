from interpreter import interpreter
from dotenv import load_dotenv
import os
load_dotenv()

interpreter.llm.api_key = os.environ.get("API_KEY")

interpreter.llm.model = "openai/gpt-3.5-turbo" # Tells OI to send messages in OpenAI's format

interpreter.chat("tunr the system to light mode")