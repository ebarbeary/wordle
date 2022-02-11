from .WordleBot import WordleBot
import random

class Random(WordleBot):
    """Random is a hardmode strategy that guesses uniformly randomly between possible words."""
    bot_name = "RandomBot"

    def guess(self) -> str:
        self.update_dictionary()
        rand_idx = random.randint(0, len(self.dictionary)-1)
        return self.dictionary.index[rand_idx]