import random

# some of the most popular names, plus some I just like
nameList = ["James", "Mary", "John", "Jen", "Mike", "Will", "Beth", "David", "Jessica", "Tom", "Joe",
            "Charlie", "Sarah", "Grace", "Chris", "Nancy", "Lisa", "Matt", "Margaret", "Anthony",
            "Daniel", "Ashley", "Mark", "Paul", "Peyton", "Andrew", "Kim", "Michelle", "Jill",
            "Julia", "Josh", "Kevin", "Brian", "Edward", "Tim", "Jeff", "Ryan", "Becca", "Laura",
            "Anna", "Scott", "Emma", "Raymond", "Greg", "Benjamin", "Braedon", "Lawrence", 
            "Taylor", "Rowan"]

class player():
    def __init__(self, gamemode): # gamemode is an int between 1-4 indicating difficulty
        self.name = random.choice(nameList)
        
        self.skills = {} # a dictionary of all skills
        self.skills["BIOLOGY"] = random.randint(100*(gamemode-1), 100*(gamemode+1))/500
        self.skills["CHEMISTRY"] = random.randint(100*(gamemode-1), 100*(gamemode+1))/500
        self.skills["EARTH AND SPACE"] = random.randint(100*(gamemode-1), 100*(gamemode+1))/500
        self.skills["ENERGY"] = random.randint(100*(gamemode-1), 100*(gamemode+1))/500
        self.skills["MATH"] = random.randint(100*(gamemode-1), 100*(gamemode+1))/500
        self.skills["PHYSICS"] = random.randint(100*(gamemode-1), 100*(gamemode+1))/500
        self.skills["GENERAL SCIENCE"] = random.randint(100*(gamemode-1), 100*(gamemode+1))/500 # only in some sets; also used if type cannot be deterimined
        self.skills["chill"] = random.randint(100*(gamemode-1), 100*(gamemode+1))/500
        self.skills["speed"] = random.randint(100*(gamemode-1), 100*(gamemode+1))/500

    def __repr__(self):
        return f"{self.name} {self.skills}"

    # returns a tuple of three values: the first is correctness which is a bool
    # the second is time, measured in question lengths (less than 1 is an interrups)
    # third is certainty, mostly used for (hopefully) setting facial expressions
    def getBuzz(self, qtype):
        if qtype not in ["BIOLOGY", "CHEMISTRY", "EARTH AND SPACE", "ENERGY", "MATH", "PHYSICS", "GENERAL SCIENCE"]:
            qtype = "GENERAL SCIENCE"
        qscore = random.random()
        if self.skills[qtype] + .25*self.skills["chill"] > qscore: # calm player are a bit more likely to get a question right
            correctness = True
        else: 
            correctness = False

        certainty = self.skills[qtype]*(random.uniform(0.75, 1.25))
        if certainty > 1: certainty = 1 # float between 0 and 1

        speed = 3 - 1.5*(self.skills["speed"] + certainty) # float between 0 and 2

        return correctness, speed, certainty

def createTeam(gamemode):
    player1 = player(gamemode)
    player2 = player(gamemode)
    player3 = player(gamemode)
    player4 = player(gamemode)

    return (player1, player2, player3, player4)