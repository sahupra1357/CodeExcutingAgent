from typing import Dict, List


class ChatMessages:
    def __init__(self, developer_prompt: str):
        self.messages: List[Dict[str, str]] = []
        self.add_system_message(developer_prompt)
    
    def add_system_message(self, content: str):
        self.messages.append({"role": "developer", "content": content})

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})

    def get_messages(self) -> List[Dict[str, str]]:
        return self.messages