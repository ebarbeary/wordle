import pandas as pd
from pathlib import Path

class WordleBot(object):
    bot_name = "WordleBot"

    def __init__(self, dict_path=Path('wordle_dictionary.txt'), verbose=False) -> None:
        self.five_letter_words = []
        with open(dict_path, 'r') as file:
            for line in file.readlines():
                word = line.strip().upper()
                if len(word) == 5:
                    tokenized = [char for char in word]
                    tokenized.insert(0, word)
                    self.five_letter_words.append(tokenized)
        
        self.dictionary = pd.DataFrame(self.five_letter_words, columns=['word', '0', '1', '2', '3', '4'])
        self.dictionary = self.dictionary.set_index("word")          
        self.letter_counts = self.get_counts(self.dictionary)
        self.known_letters = set(())
        self.verbose = verbose
    
    def get_counts(self, df : pd.DataFrame) -> list:
        letter_counts = []
        for column in list(df.columns.values):
            counts = dict(df[column].value_counts())
            letter_counts.append(counts)
        return letter_counts

    def guess(self) -> str:
        self.update_dictionary()
        guess = self.dictionary.index[0]
        if self.verbose:
            print(f"Guessing: \'{guess}\' (the first word in the dictionary)")
        return guess

    def update_dictionary(self) -> None:
        if self.verbose:
            print("Updating Dictionary")
            print(f"Dictionary entries before update: {len(self.dictionary.index)}")
        
        for idx, counts in enumerate(self.letter_counts):
            self.dictionary = self.dictionary[self.dictionary[str(idx)].isin(counts)]
        words = set(self.dictionary.index)
        impossible_guesses = []
        for guess in words:
            for known_letter in self.known_letters:
                if known_letter not in guess:
                    impossible_guesses.append(guess)
                    break
        self.dictionary = self.dictionary.drop(index=impossible_guesses)

        if self.verbose:
            print(f"Dicitonary entries after update: {len(self.dictionary.index)}\n")
        self.letter_counts = self.get_counts(self.dictionary)

    def black(self, char : str) -> None:
        if self.verbose:
            print(f"(Black) Removing \'{char}\' as a possible letter from each position")
        for idx in range(len(self.letter_counts)):
            self.letter_counts[idx].pop(char, None)

    def yellow(self, char : str, position : int) -> None:
        if self.verbose:
            print(f"(Yellow) Removing \'{char}\' as a possible letter from position {position}")
        self.letter_counts[position].pop(char, None)
        self.known_letters.add(char)
        if self.verbose:
            print(f"(Yellow) known_letters after update: {self.known_letters}")

    def green(self, char : str, position : int) -> None:
        if self.verbose:
            print(f"(Green) Setting \'{char}\' as the only possible character at position {position}")
        self.letter_counts[position] = {char : 1}
    
    def reset(self):
        self.dictionary = pd.DataFrame(self.five_letter_words, columns=['word', '0', '1', '2', '3', '4'])
        self.dictionary = self.dictionary.set_index("word")          
        self.letter_counts = self.get_counts(self.dictionary)
        self.known_letters = set(())
