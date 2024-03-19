from interpreter import OpenInterpreter
from interpreter.terminal_interface.utils.count_tokens import (
    count_messages_tokens,
    count_tokens,
)

interpreter = OpenInterpreter()

from dotenv import load_dotenv
import os

load_dotenv()

interpreter.llm.api_key = os.environ.get("API_KEY_ANTHROPIC")

interpreter.llm.model = (
    "claude-3-haiku-20240307"  # Tells OI to send messages in OpenAI's format
)
interpreter.system_message += """
Run shell commands with -y so the user doesn't have to confirm them.
"""

interpreter.chat("open safari app and go to google.com using apple script")
