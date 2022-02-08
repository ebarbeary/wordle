import pandas as pd
import WordleBot as WordleBot

class FrequencyBot(WordleBot):
    welcome_message =   "*********************************************\n* Welcome to the interactive Wordle Solver! *\n*********************************************\n"
    instructions = "To enter results use: \'b\' for black, \'y\' for yellow, \'g\' for green or \'q\' to quit\n"
    end_program = False
    bot_name = "FrequencyBot"

    def __init__(self, dict_path='unigram_freq.csv') -> None:
        wordle_words = {}
        with open("wordle_dictionary.txt", 'r') as file:
            for line in file.readlines():
                wordle_words[line.strip().upper()] = 1

        five_letter_words = []
        with open(dict_path, 'r') as file:
            for line in file.readlines():
                line = line.strip().split(',')
                word = line[0].upper()
                if len(word) == 5 and word in wordle_words:
                    tokenized = [char for char in word]
                    tokenized.insert(0, word)
                    tokenized.insert(1, int(line[1]))
                    five_letter_words.append(tokenized)
        
        self.df = pd.DataFrame(five_letter_words, columns=['word', 'frequency', '0', '1', '2', '3', '4'])
        self.df = self.df.set_index("word")          
        self.letter_counts = self.get_counts(self.df.drop('frequency', axis=1))
        self.known_letters = []

    def __str__(self):
        string = ""
        for column in self.letter_counts:
            string += str(column) + "\n"
        string += str(self.known_letters)
        return string

    def get_counts(self, df : pd.DataFrame) -> list:
        letter_counts = []
        for column in list(df.columns.values):
            counts = dict(df[column].value_counts())
            letter_counts.append(counts)
        return letter_counts
    
    def play(self) -> None:
        print(self.welcome_message)      
        for attempt in range(1, 6):
            print("*** Attempt {} ***".format(attempt))
            guess = self.guess()
            for idx, char in enumerate(guess):
                user_input = input("What was the result for letter {}? (position {})\n".format(char, idx+1))
                while user_input not in {'b', 'y', 'g', 'q'}:
                    print("Invalid input")
                    print(self.instructions)
                    user_input = input("What was the result for letter {}? (position {})\n".format(char, idx+1))
                self.parse_input(user_input, char, idx)
                if self.end_program:
                    return

    def guess(self) -> str:   
        view = self.df
        for idx, counts in enumerate(self.letter_counts):
            view = view[view[str(idx)].isin(counts)]
        words = set(view.index)
        impossible_guesses = []
        for guess in words:
            for known_letter in self.known_letters:
                if known_letter not in guess:
                    impossible_guesses.append(guess)
                    break
        view = view.drop(index=impossible_guesses)

        possible_guesses = view["frequency"]
        print("There are {} possible words".format(len(possible_guesses)))
        # print("The top 10 are: \n{}\n".format(str(possible_guesses[:10])))

        self.letter_counts = self.get_counts(view.drop("frequency", axis=1))
        max_letter = ""
        max_letter_freq = 0
        for position in range(5):
            if len(self.letter_counts[position]) == 1:
                continue
            freq = max(self.letter_counts.values())
            if freq > max_letter_freq:
                max_letter_freq = freq
                max_letter = max(self.letter_counts[position], key=self.letter_counts[position].get)
                max_pos = str(position)
        
        view = view[view[position]]

        while(True):
            for word in view.index:
                answer = input("Would you like to try {}? (y/n/custom)\n".format(word))
                if answer == 'y':
                    return word
                elif answer == 'custom':
                    return input("Which custom word would you like to try?\n").upper()
            print("Run out of suggestions, trying again...")

        

    def parse_input(self, user_input : str, char : str, idx : int) -> None:
        if user_input == 'q':
            self.end_program = True
        elif user_input == 'g':
            self.green(char, idx)
        elif user_input == 'y':
            self.yellow(char, idx)
        elif user_input == 'b':
            self.black(char)
        return
    

def main():
    session = WordleBot()
    session.play()

if __name__ == "__main__":
    main()