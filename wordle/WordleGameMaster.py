from bots import WordleBot
from tqdm import tqdm
class WordleGameMaster:
    """WordleGameMaster manages the automated playing of Wordle using bots.

    It can be used in one of two ways: 
    One round at a time with the caller providing the answer for that round.
    Multiple rounds with aggregated results using a provided list of answers.       
    """
    
    def __init__(self, 
                 valid_words : list, 
                 verbose : bool = False,
    ) -> None:
        """Initialises WordleGameMaster with valid_words list and verbose.
        
        Args:
            valid_words: A list of valid words that can be submitted as guesses.
            verbose: A boolean indicating whether to output debugging information.
        """
        self.verbose = verbose
        self.valid_words = set(valid_words)

    def play(self, 
             answer : str, 
             player : WordleBot, 
             attempt_limit : int = 20,
    ) -> dict:
        """Plays a single round of wordle with the given bot.

        Retrieves guesses from the bot until it guesses correctly or reaches max attempts.
        The letters of each guess are scored according to the score_guess function.

        Args:
            answer: the word the bot needs to guess.
            player: the bot used to generate guesses.
            attempt_limit: the maximum number of allowed_attempts (prevent infinite loops).

        Returns:
            A dict of results with keys:
            'score': An int representing the number of attempts the bot took to guess correctly.
            'results': A list of the individual letter scores from each attempt.
            'guesses': A list of guesses submitted by the bot.
        
        Raises:
            ValueError: The bot attempted to guess an invalid word.
        """
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

    def score_guess(self, 
                    answer : str, 
                    guess : str,
    ) -> list:
        """Scores a guess based on whether its letters match with the answer.

        The letters of the guess are scored as:
        'g' for correct letter in the correct place (green)
        'y' for correct letter in the wrong place (yellow)
        'b' for incorrect letter (black)

        Args:
            answer: The answer the guess must try to match.
            guess: The guess given by the bot.

        Returns:
            A list of single character strings the same length as the guess
            indicating whether the letter in each position is green, yellow or black.
        """
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

    def feedback_result(self, 
                        bot : WordleBot, 
                        guess : str, 
                        results : list,
    ) -> None:
        """A utility function that updates the bot with the results of its guess.

        Args:
            bot: The bot being updated with the results.
            guess: The guess submitted by the bot.
            results: The list of scores for each letter in the guess.
        """
        for position, char in enumerate(guess):
                    result = results[position]
                    if result == 'g':
                        bot.green(char, position)
                    elif result == 'y':
                        bot.yellow(char, position)                
                    elif result == 'b':
                        bot.black(char)

    def play_all(self, 
                 player : WordleBot, 
                 answers : list, 
                 max_attempts : int = 6,
    ) -> tuple:
        """Plays wordle with a bot for each word in answers and aggregates results.
        
        Args:
            player: The bot used to generate guesses.
            answers: The list of words to play with.
            max_attempts: The number of guesses allowed for successful round.

        Returns:
            A dictionary with aggregated results under the keys:
            'mean_score': The mean score from all rounds.
            'stats': The distribution of scores from all rounds.
            'failed_rounds': The session output from each failed round.

        Raises:
            ValueError: The bot attempted to guess an invalid word.
        """
        stats = {}
        failed_rounds = []
        for answer in tqdm(answers):
            session = self.play(answer, player)
            score = session["score"]
            stats[score] = stats.get(score, 0) + 1
            if score >= max_attempts:
                failed_rounds.append(session)
                if self.verbose:
                    print(f"Failed on answer: {answer}\nGuesses: {session['guesses']}\nStats: {session['stats']}")

        results = {}
        results["mean_score"] = sum([key*stats[key] for key in stats.keys()]) / sum(stats.values())
        results["stats"] = dict(sorted(stats.items()))
        results["failed_rounds"] = failed_rounds
        return results