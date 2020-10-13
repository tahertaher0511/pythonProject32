import random
from os import path


class RockPaperScissors:
    allowed_input = ("!help", "!rating", "!exit", "rock", "paper", "scissors")
    allowed_game_input = ("rock", "paper", "scissors")
    winner_pairs = {"rock": "paper", "paper": "scissors", "scissors": "rock"}  # value wins
    scores_path = "rating.txt"
    POINTS_WIN = 100
    POINTS_DRAW = 50

    # the game files are created in __init__, if not already existing
    def __init__(self):
        self.user_input = ""
        self.cpu_choice = ""
        self.exit = False
        self.user_name = ""
        # create game files now, if they are not created yet
        if not path.exists(self.scores_path):
            open(self.scores_path, "w").close()

    def get_random_option_cpu(self):
        random.seed()
        self.cpu_choice = random.choice(self.allowed_game_input)

    def scores_to_list(self):
        score_sheet = open(self.scores_path, "r")
        current_scores = [player_entry.strip("\n").split() for player_entry in score_sheet]
        score_sheet.close()
        return current_scores

    def increase_user_score(self, score):
        # read the current scores
        scores = self.scores_to_list()
        # update the specific score
        for entry in scores:
            if entry[0] == self.user_name:
                entry[1] = str(int(entry[1]) + score)
        # update the score file
        score_sheet = open(self.scores_path, "w")
        for entry in scores:
            score_sheet.write(entry[0] + " " + entry[1] + "\n")
            # print(entry[0], entry[1], sep=" ", end="\n", file=score_sheet)
        score_sheet.close()

    def announce_winner(self):
        # 1. draw
        if self.user_input == self.cpu_choice:
            print("There is a draw ({})".format(self.cpu_choice))
            self.increase_user_score(score=self.POINTS_DRAW)
        # 2. computer wins
        elif self.winner_pairs[self.user_input] == self.cpu_choice:
            print("Sorry, but computer chose {}".format(self.cpu_choice))
        # 3. player wins
        elif self.winner_pairs[self.cpu_choice] == self.user_input:
            print("Well done. Computer chose {} and failed".format(self.cpu_choice))
            self.increase_user_score(score=self.POINTS_WIN)

    def is_game_input(self):
        return self.user_input in self.allowed_game_input

    def get_user_input(self):
        action = input()
        if action not in self.allowed_input:
            self.user_input = ""
            print("Please write !help to see your options.")
        else:
            if action == "!exit":
                print("Bye!")
                self.user_input = ""
                self.exit = True
            elif action == "!help":
                self.user_input = ""
                print("Write either (rock or paper or scissors) or (!exit) or (!rating)")
            elif action == "!rating":
                self.user_input = ""
                scores = self.scores_to_list()
                for entry in scores:
                    if entry[0] == self.user_name:
                        print("Your rating:", entry[1])
            else:
                # all other cases are game input (rock, paper, scissors, ..):
                self.user_input = action

    # get_user_name is executed at the start of the game
    def register_new_user(self):
        score_sheet = open(self.scores_path, "a")
        score_sheet.write(self.user_name + " 0\n")
        # print(self.user_name, "0", sep=" ", end="\n", file=score_sheet)
        score_sheet.close()

    def get_correct_user_name(self):
        self.user_name = input("Enter your name: ").replace(" ", "")
        print("Hello, {}".format(self.user_name))
        # add the user to the score sheet if not already in the sheet
        if path.getsize(self.scores_path) > 0:
            scores = self.scores_to_list()
            user_in_scores = False
            for entry in scores:
                if entry[0] == self.user_name:
                    user_in_scores = True
            if not user_in_scores:
                self.register_new_user()
        else:
            # in case there was no user at all, add the user right away
            self.register_new_user()

    def no_user_name_yet(self):
        return self.user_name == ""

    def game(self):
        while not self.exit:
            if self.no_user_name_yet():
                self.get_correct_user_name()
            else:
                self.get_user_input()
                if self.is_game_input():
                    self.get_random_option_cpu()
                    self.announce_winner()


rockpaperscissors = RockPaperScissors()
rockpaperscissors.game()
