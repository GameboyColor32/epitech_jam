#!/usr/bin/python3

import csv
import sys
import random


bat =r"""
THE HERO GUESSER
  _   ,_,   _
 / `'=) (='` \
/.-.-.\ /.-.-.\
`      "      `
"""

usage="""
USAGE
\tpython3 main.py data/heroes.csv

HOW DOES IT WORK
\tTo add questions, just edit the questions.csv file with this syntax:
\t\tquestion;comma_separated_list_of_heros,...
\tIf there is a space in the name, put it between "
\tBased on a yes or no question, the program will add or substract points from the heroes from the list of the quesion
\tSo if I respond no to the question you gave me, the heroes from the list will lost points.
\tOr you can just call:
\t\tcore.register_question(Question("question", [list_of_heroes]))
"""

class Question:
    def __init__(self, question: str, hero: list[str]):
        self.question = question
        self.heroes = hero

class Core:
    def __init__(self):
        self._heroes: dict = {}
        self.questions: list[Question] = []

    #@todo select only the first 25 questions parce que ça fait beaucoup la quand même
    def loop(self):
        print(bat)
        random.shuffle(self.questions)

        for question in self.questions:
            print(question.question, end='')
            res = input(" (Y/n): ").lower().strip()
            if res != "y" and res != "n" and res != "":
                print("Invalid input")
                continue
            point = 1 if res == "y" or res == "" else -1
            for hero in question.heroes:
                self._heroes[hero] += point

    def load_questions(self, questons_file: str):
        for line in open(questons_file, "r").readlines():
            l = line.strip().split(";")
            h = [h.replace("\"", "") for h in l[1].split(",")]
            self.register_question(Question(l[0], h))
            for hero in h:
                if hero not in self._heroes:
                    self._heroes[hero] = 0

    def register_question(self, question: Question):
        self.questions.append(question)

    def __repr__(self) -> str:
        return "Core()"

    def __str__(self) -> str:
        final: list[str] = ["Results"]

        for key, val in self._heroes.items():
            final.append("{} : {}".format(key, val))
        final.append("You are: {}".format(max(self._heroes, key=self._heroes.get)))
        return "\n".join(final)

def main(ac: int, av: list[str]):
    if ac == 1 and av[0] == "-h":
        print(usage)
        sys.exit(0)
    core: Core = Core()
    core.load_questions("data/questions.csv")
    core.loop()
    print(core)

if __name__ == "__main__":
    main(len(sys.argv) - 1, sys.argv[1:])
