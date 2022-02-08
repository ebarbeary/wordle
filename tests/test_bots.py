from wordle.bots import LetterCount, Random, RandomStart
from wordle import WordleGameMaster
from pathlib import Path

def test_bots():
    verbose = False
    bots = [LetterCount, Random, RandomStart]
    for bot in bots:
        print(f"\nTesting \'{bot.bot_name}\' using wordle dictionary")
        player = bot(dict_path=Path("wordle/wordle_dictionary.txt"), verbose=verbose)
        gm = WordleGameMaster(verbose=verbose)
        mean, results = gm.play_all(player)
        print(f"Mean Score: {mean}")
        print(f"Results distribution: {results}")
    assert True