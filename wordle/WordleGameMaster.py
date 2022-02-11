from bots import WordleBot
from tqdm import tqdm
class WordleGameMaster:
    
    def __init__(self, valid_words=list, verbose=False) -> None:
        self.verbose = verbose
        self.valid_words = set(valid_words)
        return
    
    def play(self, answer : str, player : WordleBot, attempt_limit=20) -> dict:
        answer = answer.upper()
        if self.verbose:
            print(f"Begin game with answer: \'{answer}\' using player: \'{player.bot_name}\'\n")
        stats = []
        guesses = []
        for attempt in range(1, attempt_limit):
            if self.verbose:
                print(f"***Attempt {attempt}***")            
            guess = player.guess().upper()
            if guess not in self.valid_words:
                raise ValueError(f"Player guess \'{guess}\' not a valid word")
            results = self.score_guess(answer, guess)            
            stats.append(results)
            guesses.append(guess)            
            if guess == answer:
                break
            else:
                self.feedback_result(player, guess, results)
        player.reset()
        return {"score":attempt, "results":stats, "guesses":guesses}

    def score_guess(self, answer : str, guess : str):
        results = []
        for position, char in enumerate(guess):
            if char == answer[position]:
                results.append('g')
            elif char in answer:
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

    def play_all(self, player : WordleBot, answers : list, max_attempts=6) -> tuple:
        results = {}
        for answer in tqdm(answers):
            session = self.play(answer, player)
            score = session["score"]
            results[score] = results.get(score, 0) + 1
            if score >= max_attempts and self.verbose:
                print(f"Failed on answer: {answer}\nGuesses: {session['guesses']}\nStats: {session['stats']}")

        mean = sum([key*results[key] for key in results.keys()]) / sum(results.values())
        return (mean, dict(sorted(results.items())))