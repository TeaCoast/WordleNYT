import random

DIRECTORY = __file__[:__file__.rfind('\\')].replace('\\', '/') + '/'

WORDLE_ANSWERS = DIRECTORY + "wordle_answers.txt"
WORDLE_ANSWERS_TOTAL = 2309
WORDLE_BANK = DIRECTORY + "wordle_bank.txt"

def get_random_word():
    index = random.randrange(0, WORDLE_ANSWERS_TOTAL)
    with open(WORDLE_ANSWERS, 'r') as word_answers:
        for i, line in enumerate(word_answers):
            if i == index:
                return line[:-1]
    raise IndexError("random index too big (it's not your fault)")

def check_word(word: str):
    word = word.lower() + '\n' 
    with open(WORDLE_BANK, 'r') as word_bank:
        for check_word in word_bank:
            if word == check_word:
                return True
    return False

BLACK = '\033[0m'
YELLOW = '\033[43m'
GREEN = '\033[42m'

class WordleAPI:
    word: str
    guess_count = 0
    guesses: list[str]


    def __init__(self, word: str|None = None):
        if word is None:
            self.word = get_random_word()
        else:
            self.word = word
        self.guesses = ['| ' * 5 + '|'] * 6
    
    def guess_word(self, word_guess: str):
        # determine guess validity
        if len(word_guess) != 5:
            return None
        if not check_word(word_guess):
            return None
        # color guess
        remaining_answer = [char for char in self.word]
        colored_guess = [0, 0, 0, 0, 0]
        for i in range(5):
            if word_guess[i] == self.word[i]:
                remaining_answer[i] = ' '
                colored_guess[i] = 2
        for i in range(5):
            if colored_guess[i] == 0 and word_guess[i] in remaining_answer:
                remaining_answer[remaining_answer.index(word_guess[i])] = ' '
                colored_guess[i] = 1
        colored_word = '|' + ''.join([('', YELLOW, GREEN)[colored_guess[i]] + word_guess[i] + BLACK + '|' for i in range(5)])
        self.guesses[self.guess_count] = colored_word
        self.guess_count += 1
        # check if guess is answer
        if self.word == word_guess:
            return True
        return False
    
    def __repr__(self):
        return fr"WordleAPI({self.word=}, {self.guesses=})"
    
    def __str__(self):
        return '\n'.join(self.guesses)


print("welcome to wordle, guess the word in 5 letters\n")

wordleapi = WordleAPI()

print(wordleapi)
print()

while True:
    valid = None
    word_guess = ''
    retry = False
    while valid is None:
        if retry:
            print("Invalid word, try again")
        word_guess = input("enter a valid English word with 5 letters: ").lower().strip()
        if word_guess == "exit":
            break
        valid = wordleapi.guess_word(word_guess)
        retry = True
    if word_guess == "exit":
        break
    print()
    if valid == True:
        print(wordleapi)
        print("you won the game!")
        break
    elif valid == False:
        print(wordleapi)
    if wordleapi.guess_count >= 6:
        print(f"you lost the game, the word was {wordleapi.word}")
        break