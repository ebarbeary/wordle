from .WordleBot import WordleBot
import random

class Random(WordleBot):
    bot_name = "RandomBot"

    def guess(self) -> str:
        self.update_dictionary()
        rand_idx = random.randint(0, len(self.dictionary)-1)
        return self.dictionary.index[rand_idx]