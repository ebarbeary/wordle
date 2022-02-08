from WordleBot import WordleBot
import pandas as pd
import random

class RandomStartBot(WordleBot):
    bot_name = "LetterCountBot"

    def guess(self) -> str:
        dictlen = len(self.dictionary)
        self.update_dictionary()
        
        # If update made no difference, must be round 1, guess randomly
        if len(self.dictionary) == dictlen:
            rand_idx = random.randint(0, len(self.dictionary)-1)
            return self.dictionary.index[rand_idx]
        view = self.dictionary

        # Select most frequently occuring letter from all positions
        mode, mode_pos, mode_freq = self.modal_letter(self.letter_counts)
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
            mode, mode_pos, mode_freq = self.modal_letter(updated_counts)
            if mode == "":
                break
            # Check a the reduced letter-count to make sure a word exists with the letter in position y
            while mode not in reduced_counts[mode_pos]:
            # If not: go back and pick the next most freq-occurring again and repeat until a word with it does exist
                updated_counts[mode_pos][mode] = 0
                mode, mode_pos, mode_freq = self.modal_letter(updated_counts)
                if mode == "":
                    break

        # Repeat the last step until a word is selected
        # Choose this word as the guess
        guess = view.index[0] 
        if self.verbose:
            print(f"Guessing \'{guess}\'")
        return guess


    def modal_letter(self, letter_counts) -> tuple:
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

def main():
    player = RandomStartBot(verbose=True)
    player.guess()

if __name__ == "__main__":
    main()