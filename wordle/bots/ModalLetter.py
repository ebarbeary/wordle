from .WordleBot import WordleBot

class ModalLetter(WordleBot):
    """ModalLetter is a hardmode strategy the optimises the chance of each letter in the guess being green.

    It calculates the most frequent letters in each position and guesses the word with the most frequently occurring letters.
    It prioritises new letters and will avoid guessing words with two of the same letter to better narrow down results.
    It guesses according to Wordle 'hardmode' rules instead of the standard rules.
    """
    bot_name = "LetterCountBot"

    def guess(self) -> str:   
        self.update_dictionary()
        view = self.dictionary

        # Select most frequently occuring letter from all positions
        mode, mode_pos, mode_freq = self.__modal_letter(self.letter_counts)
        updated_counts = [count.copy() for count in self.letter_counts]
        while mode != "":
            # Filter dictionary by words with max occuring letter at position x
            view = view[view[str(mode_pos)] == mode]
            for pos, counts in enumerate(updated_counts):
                if mode in updated_counts[pos]:
                    # Where possible, avoid choosing repeated letter
                    updated_counts[pos][mode] = 1
            updated_counts[mode_pos] = {mode : mode_freq}
            reduced_counts = self.get_counts(view)
            
            # Select next most-freq occuring letter in original word list
            mode, mode_pos, mode_freq = self.__modal_letter(updated_counts)
            if mode == "":
                break
            # Check a the reduced letter-count to make sure a word exists with the letter in position y
            while mode not in reduced_counts[mode_pos]:
            # If not: go back and pick the next most freq-occurring again and repeat until a word with it does exist
                updated_counts[mode_pos][mode] = 0
                mode, mode_pos, mode_freq = self.__modal_letter(updated_counts)
                if mode == "":
                    break

        # Repeat the last step until a word is selected
        # Choose this word as the guess
        guess = view.index[0] 
        if self.verbose:
            print(f"Guessing \'{guess}\'")
        return guess


    def __modal_letter(self, letter_counts : list) -> tuple:
        if self.verbose:
            print("Getting model letter from:")
            for count in letter_counts:
                print(count)
        mode = ""
        mode_freq = 0
        mode_pos  = -1

        for pos, counts in enumerate(letter_counts):
            # len = 1 means a letter has already been chosen for that position
            if len(counts) == 1:
                continue
            max_letter = max(counts, key=counts.get)
            letter_freq = counts[max_letter]
            if letter_freq > mode_freq:
                mode_freq = letter_freq
                mode = max_letter
                mode_pos = pos
        if self.verbose:
            print(f"Found modal letter \'{mode}\' at position \'{mode_pos}\'")
        return (mode, mode_pos, mode_freq)