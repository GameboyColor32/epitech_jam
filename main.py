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
"""

class Question:
    def __init__(self, question: str, hero: list[str]):
        self.question = question
        self.heroes = hero

class Core:
    def __init__(self, heroes: list[str]):
        self._heroes: dict = {hero: 0 for hero in heroes}
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
            self.register_question(Question(l[0], [h.replace("\"", "") for h in l[1].split(",")]))

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

#@TODO load heros only from the questions file
def main(ac: int, av: list[str]):
    if ac < 1:
        print(usage)
        sys.exit(84)
    if av[0] == "-h":
        print(usage)
        sys.exit(0)
    with open(av[0], "r") as file:
        reader = csv.reader(file, delimiter=";")
        heroes: list = [item for sublist in reader for item in sublist]
    core: Core = Core(heroes)
    core.load_questions("data/questions.csv")
    # core.register_question(Question("Do you like history?", ["Napoléon", "Hades", "Zeus", "\"Alexandre le Grand\""]))
    core.loop()
    print(core)

if __name__ == "__main__":
    main(len(sys.argv) - 1, sys.argv[1:])
