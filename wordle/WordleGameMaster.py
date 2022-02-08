from bots import WordleBot
from tqdm import tqdm
from pathlib import Path

class WordleGameMaster:
    
    def __init__(self, verbose=False) -> None:
        self.verbose = verbose
        return
    
    def play(self, word : str, player : WordleBot, attempt_limit=20) -> tuple:
        word = word.upper()
        if self.verbose:
            print(f"Begin game with word: \'{word}\' using player: \'{player.bot_name}\'\n")
        stats = []
        for attempt in range(1, attempt_limit):
            if self.verbose:
                print(f"***Attempt {attempt}***")
            
            guess = player.guess()
           
            attempt_stats = []
            for position, char in enumerate(guess):
                if char == word[position]:
                    player.green(char, position)
                    attempt_stats.append('g')
                elif char in word:
                    player.yellow(char, position)
                    attempt_stats.append('y')
                else:
                    player.black(char)
                    attempt_stats.append('b')            
            if self.verbose:
                print(f"Results for guess {attempt}: \'{guess}\'\n{attempt_stats}\n")
            stats.append(attempt_stats)

            if guess == word:
                return (attempt, stats)
        
        return (attempt_limit+1, stats)

    def play_all(self, player : WordleBot, dict_path=Path("wordle/wordle_dictionary.txt"), attempt_limit=20) -> tuple:
        dictionary = []
        with open(dict_path, 'r') as file:
            if self.verbose:
                for line in tqdm(file.readlines()):
                    dictionary.append(line.strip().upper())
            else:
                for line in file.readlines():
                    dictionary.append(line.strip().upper())
        
        results = {}
        for word in tqdm(dictionary):
            result, stats = self.play(word, player, attempt_limit)
            results[result]= results.get(result,0)+1
            if result == attempt_limit+1 and self.verbose:
                print(f"Failed on word: {word}\nStats: {stats}")
            player.reset()
        
        mean = sum([key*results[key] for key in results.keys()]) / sum(results.values())
        return (mean, dict(sorted(results.items())))