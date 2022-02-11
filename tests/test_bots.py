from wordle.bots import LetterCount, Random, RandomStart
from wordle import WordleGameMaster
from pathlib import Path

def test_bots():
    verbose = False
    bots = [LetterCount, Random, RandomStart]
    dictionary = []
    with open(Path("dictionaries/wordle_dictionary.txt"), 'r') as file:
        for line in file.readlines():
            dictionary.append(line.strip().upper())
    
    valid_words = []
    with open(Path("dictionaries/collins_scrabble_words_2019.txt"), 'r') as file:
        for line in file.readlines():
            word = line.strip().upper()
            if len(word) == 5:
                valid_words.append(word)

    for bot in bots:
        print(f"\nTesting \'{bot.bot_name}\' using wordle dictionary")
        player = bot(dictionary=valid_words, verbose=verbose)
        gm = WordleGameMaster(valid_words=valid_words, verbose=verbose)
        mean, results = gm.play_all(player, word_list=dictionary)
        print(f"Mean Score: {mean}")
        print(f"Results distribution: {results}")
    assert True