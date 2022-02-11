from bots import WordleBot
from tqdm import tqdm
from pathlib import Path

class WordleGameMaster:
    
    def __init__(self, valid_words=list, verbose=False) -> None:
        self.verbose = verbose
        self.valid_words = set(valid_words)
        return
    
    def play(self, word : str, player : WordleBot, attempt_limit=20) -> tuple:
        word = word.upper()
        if self.verbose:
            print(f"Begin game with word: \'{word}\' using player: \'{player.bot_name}\'\n")
        stats = []
        for attempt in range(1, attempt_limit):
            if self.verbose:
                print(f"***Attempt {attempt}***")            
            
            guess = player.guess().upper()
            if guess not in self.valid_words:
                raise ValueError(f"Player guess \'{guess}\' not a valid word")
            results = self.score_guess(word, guess)            
            stats.append(results)
            
            if guess == word:
                return (attempt, stats)
            else:
                self.feedback_result(player, guess, results)
        return (attempt_limit+1, stats)

    def score_guess(self, word : str, guess : str):
        results = []
        for position, char in enumerate(guess):
            if char == word[position]:
                results.append('g')
            elif char in word:
                results.append('y')
            else:
                results.append('b')            
        if self.verbose:
            print(f"Results for guess \'{guess}\': {results}\n")
        return results

    def feedback_result(self, bot : WordleBot, guess : str, results : list):
        for position, char in enumerate(guess):
                    result = results[position]
                    if result == 'g':
                        bot.green(char, position)
                    elif result == 'y':
                        bot.yellow(char, position)                
                    elif result == 'b':
                        bot.black(char)

    def play_all(self, player : WordleBot, word_list : list, attempt_limit=20) -> tuple:
        results = {}
        for word in tqdm(word_list):
            result, stats = self.play(word, player, attempt_limit)
            results[result]= results.get(result,0)+1
            if result == attempt_limit+1 and self.verbose:
                print(f"Failed on word: {word}\nStats: {stats}")
            player.reset()

        mean = sum([key*results[key] for key in results.keys()]) / sum(results.values())
        return (mean, dict(sorted(results.items())))