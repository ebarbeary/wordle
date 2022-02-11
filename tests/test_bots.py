from wordle.bots import ModalLetter, Random
from wordle import WordleGameMaster
from pathlib import Path

def test_bots():
    verbose = False
    bots = [ModalLetter, Random]
    answers = []
    with open(Path("dictionaries/wordle_dictionary.txt"), 'r') as file:
        for line in file.readlines():
            answers.append(line.strip().upper())
    
    valid_words = []
    with open(Path("dictionaries/collins_scrabble_words_2019.txt"), 'r') as file:
        for line in file.readlines():
            word = line.strip().upper()
            if len(word) == 5:
                valid_words.append(word)

    for bot in bots:
        print(f"\nTesting \'{bot.bot_name}\' using wordle dictionary")
        player = bot(dictionary=valid_words, verbose=verbose)
        gm = WordleGameMaster(valid_words, verbose=verbose)
        results = gm.play_all(player, answers)
        print(f"Mean Score: {results['mean_score']}")
        print(f"Results distribution: {results['stats']}")
        # print(f"Failed Words: {results['failed_rounds']}")
    assert True