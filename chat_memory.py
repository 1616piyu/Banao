

class ChatMemory:
    """
    Maintains conversation history using a sliding window.
    """
    def __init__(self, max_turns=5):
        self.max_turns = max_turns
        self.history = []

    def add(self, user, bot):
        """
        Add a new user-bot exchange to memory.
        """
        self.history.append(f"User: {user}\nBot: {bot}")
        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def get_context(self):
        """
        Returns conversation history as context string.
        """
        return "\n".join(self.history)
