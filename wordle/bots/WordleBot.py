from abc import ABC, abstractmethod
import pandas as pd
class WordleBot(ABC):
    """WordleBot is an abstract class containing utility methods for bots to inherit.
    
    Attributes:
        bot_name: The name of the bot for debugging output.
        word_list: The list of words to draw guesses from.
        dictionary: A dataframe of words and their decomposition by letter.
        letter_counts: A dict of counts for how many times a letter appears at each position.
        known_letters: A set of letters that are known to be in the word but not their position.
        verbose: A bool declaring whether to output debugging information.
    """
    
    bot_name = "WordleBot"

    def __init__(self, 
                 dictionary : list, 
                 verbose : bool = False,
    ) -> None:
        """Initialises the bot setting up utility variables for making guesses."""
        self.word_list = []
        for word in dictionary:
            tokenized = [char for char in word]
            tokenized.insert(0, word)
            self.word_list.append(tokenized)
        
        columns = ['word'] + [str(i) for i in range(len(tokenized)-1)]
        self.dictionary = pd.DataFrame(self.word_list, columns=columns)
        self.dictionary = self.dictionary.set_index("word")

        self.letter_counts = self.get_counts(self.dictionary)
        self.known_letters = set(())
        self.verbose = verbose
    
    def get_counts(self, df : pd.DataFrame) -> list:
        """Counts the amount of times each letter appears in each position across a set of words.

        Args:
            df: A dataframe containing words with letters decomposed into columns to be counted.
        
        Returns:
            A dict of counts for how many times a letter appears at each position (for example how many 'A's there are as the first letter in a word).
        """
        letter_counts = []
        for column in list(df.columns.values):
            counts = dict(df[column].value_counts())
            letter_counts.append(counts)
        return letter_counts

    @abstractmethod
    def guess(self) -> str:
        """Based on the information available, the bot will generate a word as its guess."""
        pass

    def update_dictionary(self) -> None:
        """Remove words that are no longer possible guesses based on information in letter_counts and known_words."""
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
        """Removes the given letter from all possible positions.
        
        Args:
            char: The letter recorded as black.
        """
        if self.verbose:
            print(f"(Black) Removing \'{char}\' as a possible letter from each position")
        for idx in range(len(self.letter_counts)):
            self.letter_counts[idx].pop(char, None)

    def yellow(self, char : str, position : int) -> None:
        """Removes the given letter from the position provided and adds it to the known_letters.

        Args:
            char: The letter recorded as yellow.
            position: The position in the word that the letter is in.
        """
        if self.verbose:
            print(f"(Yellow) Removing \'{char}\' as a possible letter from position {position}")
        self.letter_counts[position].pop(char, None)
        self.known_letters.add(char)
        if self.verbose:
            print(f"(Yellow) known_letters after update: {self.known_letters}")

    def green(self, char : str, position : int) -> None:
        """Sets the given letter as the only possible letter at the given position.
        
        Args:
            char: The letter recorded as green.
            position: The position in the word that the letter is in.
        """
        if self.verbose:
            print(f"(Green) Setting \'{char}\' as the only possible character at position {position}")
        self.letter_counts[position] = {char : 1}
    
    def reset(self) -> None:
        """Restores the internal dataframe, letter_counts and known_letters ready for a new round."""
        self.dictionary = pd.DataFrame(self.word_list, columns=['word', '0', '1', '2', '3', '4'])
        self.dictionary = self.dictionary.set_index("word")          
        self.letter_counts = self.get_counts(self.dictionary)
        self.known_letters = set(())
