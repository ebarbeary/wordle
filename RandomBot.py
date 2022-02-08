from WordleBot import WordleBot
import random

class RandomBot(WordleBot):
    bot_name = "LetterCountBot"

    def guess(self) -> str:
        self.update_dictionary()
        rand_idx = random.randint(0, len(self.dictionary)-1)
        return self.dictionary.index[rand_idx]


def main():
    player = RandomBot(verbose=True)
    player.guess()

if __name__ == "__main__":
    main()