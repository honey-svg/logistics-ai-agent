from app.utils.trim import trim_history
from app.agent.prompts import SYSTEM_PROMPT
from app.llm.client import generate_response

class ConversationManager:
    def __init__(self, memory):
        self.memory = memory

    def build_messages(self, user_input):
        recent = trim_history(self.memory.get_history())

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Memory Summary: {self.memory.summary}"},
        ]

        messages.extend(recent)
        messages.append({"role": "user", "content": user_input})

        return messages

    def chat(self, user_input):
        self.memory.add_message("user", user_input)

        messages = self.build_messages(user_input)
        response = generate_response(messages)

        self.memory.add_message("assistant", response)

        return response
