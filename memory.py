class Memory:
    def __init__(self):
        self.history = []
        self.summary = ""

    def add_message(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

    def get_history(self):
        return self.history

    def get_recent(self, k=8):
        return self.history[-k:]

    def update_summary(self, summary_text):
        self.summary = summary_text
