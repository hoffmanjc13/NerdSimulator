# Nerd Simulation: the game v1.2
# a game by Juno Hoffman

# copyright 2020, or something
# just don't don't steal this or something, k?

from cmu_112_graphics import * 
# from https://www.cs.cmu.edu/~112/notes/hw4.html to make the graphics work

from opponents import *
from pdfParser import *

import time, json, math
import random

class SplashScreen(Mode):
    def appStarted(mode): # should I be using self instead of mode? yeah, but I only noticed partway through and I'm not switching
        mode.protologo = mode.loadImage("nerdSimulatorJoke.jpg")
        mode.logo = mode.scaleImage(mode.protologo, .25)
        mode.mouseOver = None
        mode.mouseX, mode.mouseY = 0, 0

        # set up button loctations
        # haha butts
        mode.gameButtX0, mode.gameButtX1 = mode.app.width/2 - 200, mode.app.width/2 + 200
        mode.gameButtY0, mode.gameButtY1 = mode.app.height/2 - 50, mode.app.height/2 + 50

        mode.twoPButtX0, mode.twoPButtX1 = mode.app.width/2 - 200, mode.app.width/2 + 200
        mode.twoPButtY0, mode.twoPButtY1 = mode.app.height/2 + 100, mode.app.height/2 + 200

        mode.rulesButtX0, mode.rulesButtX1 = mode.app.width/2 - 200, mode.app.width/2 + 200
        mode.rulesButtY0, mode.rulesButtY1 = mode.app.height/2 + 250, mode.app.height/2 + 350


    def mouseMoved(mode, event):
        mode.mouseX, mode.mouseY = event.x, event.y
        if mode.gameButtX0 < event.x < mode.gameButtX1 and mode.gameButtY0 < event.y < mode.gameButtY1:
            mode.mouseOver = "gameButton"

        elif mode.twoPButtX0 < event.x < mode.twoPButtX1 and mode.twoPButtY0 < event.y < mode.twoPButtY1:
            mode.mouseOver = "twoPlayerButton"
        
        elif mode.rulesButtX0 < event.x < mode.rulesButtX1 and mode.rulesButtY0 < event.y < mode.rulesButtY1:
            mode.mouseOver = "rulesButton"

        else:
            mode.mouseOver = None


    def mousePressed(mode, event):
        if mode.mouseOver == "gameButton":
            mode.app.setActiveMode(mode.app.gameSettings)
        elif mode.mouseOver == "twoPlayerButton":
            pass
            #mode.app.setActiveMode(mode.app.twoPlayer)
        elif mode.mouseOver == "rulesButton":
            mode.app.setActiveMode(mode.app.gameHelp)

    def redrawAll(mode, canvas):
        # the DOE has a bunch of rules about logos 'n' stuff. I use some of them
        # I mostly ignore them tho
        # here's the full list, and also the file: https://science.osti.gov/wdts/nsb/About/Logos#:~:text=of%20the%20logo.-,Color%20Variations,on%20white%20or%20light%20backgrounds).&text=Note%3A%20The%20green%20and%20blue,use%20the%20following%20colors%2C%20respectively.

        canvas.create_image(mode.app.width/2, 10, image=ImageTk.PhotoImage(mode.logo), anchor="n")

        # if you're mousing over a button, it turns blue
        if mode.mouseOver == "gameButton":
            canvas.create_rectangle(mode.gameButtX0, mode.gameButtY0, mode.gameButtX1, mode.gameButtY1, fill="#004990", outline="white")
            canvas.create_text((mode.gameButtX0+mode.gameButtX1)/2, (mode.gameButtY0+mode.gameButtY1)/2, text="START GAME", fill="white", font="Arial 12 bold")
            
            canvas.create_rectangle(mode.twoPButtX0, mode.twoPButtY0, mode.twoPButtX1, mode.twoPButtY1, fill="#0F6636", outline="white")
            canvas.create_text((mode.twoPButtX0+mode.twoPButtX1)/2, (mode.twoPButtY0+mode.twoPButtY1)/2, text="MULTIPLAYER", fill="white", font="Arial 12 bold")

            canvas.create_rectangle(mode.rulesButtX0, mode.rulesButtY0, mode.rulesButtX1, mode.rulesButtY1, fill="#0F6636", outline="white")
            canvas.create_text((mode.rulesButtX0+mode.rulesButtX1)/2, (mode.rulesButtY0+mode.rulesButtY1)/2, text="RULES", fill="white", font="Arial 12 bold")


        elif mode.mouseOver == "twoPlayerButton":
            canvas.create_rectangle(mode.twoPButtX0, mode.twoPButtY0, mode.twoPButtX1, mode.twoPButtY1, fill="#004990", outline="white")
            canvas.create_text((mode.twoPButtX0+mode.twoPButtX1)/2, (mode.twoPButtY0+mode.twoPButtY1)/2, text="MULTIPLAYER", fill="white", font="Arial 12 bold")

            canvas.create_rectangle(mode.gameButtX0, mode.gameButtY0, mode.gameButtX1, mode.gameButtY1, fill="#0F6636", outline="white")
            canvas.create_text((mode.gameButtX0+mode.gameButtX1)/2, (mode.gameButtY0+mode.gameButtY1)/2, text="START GAME", fill="white", font="Arial 12 bold")

            canvas.create_rectangle(mode.rulesButtX0, mode.rulesButtY0, mode.rulesButtX1, mode.rulesButtY1, fill="#0F6636", outline="white")
            canvas.create_text((mode.rulesButtX0+mode.rulesButtX1)/2, (mode.rulesButtY0+mode.rulesButtY1)/2, text="RULES", fill="white", font="Arial 12 bold")

        elif mode.mouseOver == "rulesButton":
            canvas.create_rectangle(mode.rulesButtX0, mode.rulesButtY0, mode.rulesButtX1, mode.rulesButtY1, fill="#004990", outline="white")
            canvas.create_text((mode.rulesButtX0+mode.rulesButtX1)/2, (mode.rulesButtY0+mode.rulesButtY1)/2, text="RULES", fill="white", font="Arial 12 bold")
            
            canvas.create_rectangle(mode.gameButtX0, mode.gameButtY0, mode.gameButtX1, mode.gameButtY1, fill="#0F6636", outline="white")
            canvas.create_text((mode.gameButtX0+mode.gameButtX1)/2, (mode.gameButtY0+mode.gameButtY1)/2, text="START GAME", fill="white", font="Arial 12 bold")

            canvas.create_rectangle(mode.twoPButtX0, mode.twoPButtY0, mode.twoPButtX1, mode.twoPButtY1, fill="#0F6636", outline="white")
            canvas.create_text((mode.twoPButtX0+mode.twoPButtX1)/2, (mode.twoPButtY0+mode.twoPButtY1)/2, text="MULTIPLAYER", fill="white", font="Arial 12 bold")

        else:
            canvas.create_rectangle(mode.gameButtX0, mode.gameButtY0, mode.gameButtX1, mode.gameButtY1, fill="#0F6636", outline="white")
            canvas.create_text((mode.gameButtX0+mode.gameButtX1)/2, (mode.gameButtY0+mode.gameButtY1)/2, text="START GAME", fill="white", font="Arial 12 bold")

            canvas.create_rectangle(mode.twoPButtX0, mode.twoPButtY0, mode.twoPButtX1, mode.twoPButtY1, fill="#0F6636", outline="white")
            canvas.create_text((mode.twoPButtX0+mode.twoPButtX1)/2, (mode.twoPButtY0+mode.twoPButtY1)/2, text="MULTIPLAYER", fill="white", font="Arial 12 bold")

            canvas.create_rectangle(mode.rulesButtX0, mode.rulesButtY0, mode.rulesButtX1, mode.rulesButtY1, fill="#0F6636", outline="white")
            canvas.create_text((mode.rulesButtX0+mode.rulesButtX1)/2, (mode.rulesButtY0+mode.rulesButtY1)/2, text="RULES", fill="white", font="Arial 12 bold")

class GameHelp(Mode):
    def appStarted(mode):
        mode.buttonX0, mode.buttonX1 = mode.app.width/2 - 200, mode.app.width/2 + 200
        mode.buttonY0, mode.buttonY1 = mode.app.height - 150, mode.app.height - 50

        mode.mouseOver = None

        mode.text = '''
        \tNerd Simulator Bowl is a game designed to help students practice for Sciencebowl, and also just because I like Sciencebowl. This game reads official Sciencebowl question sets and allows you to play against computer generated opponents.
        \tEvery round consists of tossup and bonus questions. Tossup question are fast-pased questions with a short time limit that both teams get a chance to answer. If you buzz in with the correct answer (using the spacebar) before the other team, you earn 4 points and the right to answer the next bonus. Bonus questions are comparatively harder, and have a significantly longer time limit. Additionally, only the team who correctly answered the last tossup may answer the bonus. If you correctly get the bonus question, you get 10 points.
        \tTo read question sets, or to read the official Sciencebowl rules, visit the DOE's website, https://science.osti.gov/wdts/nsb.
        '''
        mode.text = formatRules(mode.text, 75)
    
    def mouseMoved(mode, event):
        mode.mouseX, mode.mouseY = event.x, event.y
        if mode.buttonX0 < event.x < mode.buttonX1 and mode.buttonY0 < event.y < mode.buttonY1:
            mode.mouseOver = "button"
        else:
            mode.mouseOver = None

    def mousePressed(mode, event):
        if mode.mouseOver == "button":
            mode.app.setActiveMode(mode.app.splashScreen)

    def redrawAll(mode, canvas):
        if mode.mouseOver == "button":
            canvas.create_rectangle(mode.buttonX0, mode.buttonY0, mode.buttonX1, mode.buttonY1, fill="#004990", outline="white")
            canvas.create_text((mode.buttonX0+mode.buttonX1)/2, (mode.buttonY0+mode.buttonY1)/2, text="BACK", fill="white", font="Arial 12 bold")
        else:
            canvas.create_rectangle(mode.buttonX0, mode.buttonY0, mode.buttonX1, mode.buttonY1, fill="#0F6636", outline="white")
            canvas.create_text((mode.buttonX0+mode.buttonX1)/2, (mode.buttonY0+mode.buttonY1)/2, text="BACK", fill="white", font="Arial 12 bold")
        
        canvas.create_text(mode.app.width/2, 60, text="Rules", fill="#004990", font="Ariel 72 bold")
        canvas.create_text(mode.app.width/2, 100, text=mode.text, font="Arial 12", anchor="n", fill="#090909")

class GameSettings(Mode):
    def appStarted(mode):
        mode.protologo = mode.loadImage("nerdSimulatorJoke.jpg")
        mode.logo = mode.scaleImage(mode.protologo, .1)
        mode.gamemode = "traditional" # options are tradional or tossups only
        mode.gameDifficulty = 1 # options are 1-5, I think
        mode.hasDrawing = True # it's a bool. take a guess what the options are
        mode.roundNum = 0 # between 1 and 16 (if 0 pick random of the sets not yet done)

        # this section is just listing off all the buttons
        mode.mouseOver = None
        # has bonuses?
        mode.tradButtX0, mode.tradButtX1 = mode.app.width*.25 - 100, mode.app.width*.25 + 100
        mode.tradButtY0, mode.tradButtY1 = 300, 350

        mode.tuButtX0, mode.tuButtX1 = mode.app.width*.25 - 100, mode.app.width*.25 + 100
        mode.tuButtY0, mode.tuButtY1 = 375, 425

        # has drawing questions?
        mode.hasDrawButtX0, mode.hasDrawButtX1 = mode.app.width*.75 - 100, mode.app.width*.75 + 100
        mode.hasDrawButtY0, mode.hasDrawButtY1 = 300, 350

        mode.noDrawButtX0, mode.noDrawButtX1 = mode.app.width*.75 - 100, mode.app.width*.75 + 100
        mode.noDrawButtY0, mode.noDrawButtY1 = 375, 425

        # how hard?
        mode.easyButtX0, mode.easyButtX1 = mode.app.width*.2 - 50, mode.app.width*.2 + 50
        mode.easyButtY0, mode.easyButtY1 = 500, 525

        mode.medButtX0, mode.medButtX1 = mode.app.width*.4 - 50, mode.app.width*.4 + 50
        mode.medButtY0, mode.medButtY1 = 500, 525

        mode.hardButtX0, mode.hardButtX1 = mode.app.width*.6 - 50, mode.app.width*.6 + 50
        mode.hardButtY0, mode.hardButtY1 = 500, 525

        mode.ultraButtX0, mode.ultraButtX1 = mode.app.width*.8 - 50, mode.app.width*.8 + 50
        mode.ultraButtY0, mode.ultraButtY1 = 500, 525 # haha. ultra butt.

        # what round?
        mode.setRoundButtX0, mode.setRoundButtX1 = mode.app.width/3 - 100, mode.app.width/3 + 100
        mode.setRoundButtY0, mode.setRoundButtY1 = 650, 675

        mode.resetRoundButtX0, mode.resetRoundButtX1 = 2*mode.app.width/3 - 100, 2*mode.app.width/3 + 100
        mode.resetRoundButtY0, mode.resetRoundButtY1 = 650, 675

        # start!
        mode.startButtX0, mode.startButtX1 = mode.app.width/2 - 100, mode.app.width/2 + 100
        mode.startButtY0, mode.startButtY1 = mode.app.height - 100, mode.app.height - 25

    # to make the buttons change color when moused over
    def mouseMoved(mode, event):
        if mode.tradButtX0 < event.x < mode.tradButtX1 and mode.tradButtY0 < event.y < mode.tradButtY1:
            mode.mouseOver = "tradButt"
        elif mode.tuButtX0 < event.x < mode.tuButtX1 and mode.tuButtY0 < event.y < mode.tuButtY1:
            mode.mouseOver = "tossupButt"

        elif mode.hasDrawButtX0 < event.x < mode.hasDrawButtX1 and mode.hasDrawButtY0 < event.y < mode.hasDrawButtY1:
            mode.mouseOver = "hasDrawButt"
        elif mode.noDrawButtX0 < event.x < mode.noDrawButtX1 and mode.noDrawButtY0 < event.y < mode.noDrawButtY1:
            mode.mouseOver = "noDrawButt"

        elif mode.easyButtX0 < event.x < mode.easyButtX1 and mode.easyButtY0 < event.y < mode.easyButtY1:
            mode.mouseOver = "easyButt"
        elif mode.medButtX0 < event.x < mode.medButtX1 and mode.medButtY0 < event.y < mode.medButtY1:
            mode.mouseOver = "medButt"
        elif mode.hardButtX0 < event.x < mode.hardButtX1 and mode.hardButtY0 < event.y < mode.hardButtY1:
            mode.mouseOver = "hardButt"
        elif mode.ultraButtX0 < event.x < mode.ultraButtX1 and mode.ultraButtY0 < event.y < mode.ultraButtY1:
            mode.mouseOver = "ultraButt"
        
        elif mode.setRoundButtX0 < event.x < mode.setRoundButtX1 and mode.setRoundButtY0 < event.y < mode.setRoundButtY1:
            mode.mouseOver = "setRoundButt"
        elif mode.resetRoundButtX0 < event.x < mode.resetRoundButtX1 and mode.resetRoundButtY0 < event.y < mode.resetRoundButtY1:
            mode.mouseOver = "resetRoundButt"

        elif mode.startButtX0 < event.x < mode.startButtX1 and mode.startButtY0 < event.y < mode.startButtY1:
            mode.mouseOver = "startButt"
        
        else:
            mode.mouseOver = None

    def mousePressed(mode, event):
        if mode.mouseOver == "tradButt":
            mode.gamemode = "traditional"
        elif mode.mouseOver == "tossupButt":
            mode.gamemode = "tossups"

        elif mode.mouseOver == "hasDrawButt":
            mode.hasDrawing = True
        elif mode.mouseOver == "noDrawButt":
            mode.hasDrawing = False

        elif mode.mouseOver == "easyButt":
            mode.gameDifficulty = 1
        elif mode.mouseOver == "medButt":
            mode.gameDifficulty = 2
        elif mode.mouseOver == "hardButt":
            mode.gameDifficulty = 3
        elif mode.mouseOver == "ultraButt":
            mode.gameDifficulty = 4

        elif mode.mouseOver == "setRoundButt":
            mode.roundNum = simpledialog.askstring("Set Round", "What round would you like?")
            try: 
                mode.roundNum = int(mode.roundNum)
            except: 
                print("not allowed!")
                mode.roundNum = 0
            mode.mouseOver = None

        elif mode.mouseOver == "resetRoundButt":
            with open("questionSets/setsRead.txt", 'w') as file:
                file.write("")

        elif mode.mouseOver == "startButt":
            # push all required variables to app
            mode.app.gamemode = mode.gamemode
            mode.app.gameDifficulty = mode.gameDifficulty
            mode.app.hasDrawing = mode.hasDrawing
            mode.app.roundNum = mode.roundNum

            # switch mode to tossups
            mode.app.setActiveMode(mode.app.gameSetup)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.app.width/2, 10, image=ImageTk.PhotoImage(mode.logo), anchor="n")

        canvas.create_rectangle(mode.tradButtX0, mode.tradButtY0, mode.tradButtX1, mode.tradButtY1, fill="#0F6636")
        canvas.create_rectangle(mode.tuButtX0, mode.tuButtY0, mode.tuButtX1, mode.tuButtY1, fill="#0F6636")

        canvas.create_rectangle(mode.hasDrawButtX0, mode.hasDrawButtY0, mode.hasDrawButtX1, mode.hasDrawButtY1, fill="#0F6636")
        canvas.create_rectangle(mode.noDrawButtX0, mode.noDrawButtY0, mode.noDrawButtX1, mode.noDrawButtY1, fill="#0F6636")

        canvas.create_rectangle(mode.easyButtX0, mode.easyButtY0, mode.easyButtX1, mode.easyButtY1, fill="#0F6636")
        canvas.create_rectangle(mode.medButtX0, mode.medButtY0, mode.medButtX1, mode.medButtY1, fill="#0F6636")
        canvas.create_rectangle(mode.hardButtX0, mode.hardButtY0, mode.hardButtX1, mode.hardButtY1, fill="#0F6636")
        canvas.create_rectangle(mode.ultraButtX0, mode.ultraButtY0, mode.ultraButtX1, mode.ultraButtY1, fill="#0F6636")

        canvas.create_rectangle(mode.setRoundButtX0, mode.setRoundButtY0, mode.setRoundButtX1, mode.setRoundButtY1, fill="#0F6636")
        canvas.create_rectangle(mode.resetRoundButtX0, mode.resetRoundButtY0, mode.resetRoundButtX1, mode.resetRoundButtY1, fill="#0F6636")

        canvas.create_rectangle(mode.startButtX0, mode.startButtY0, mode.startButtX1, mode.startButtY1, fill="#0F6636")

        # ifs instead of elifs because these are all independant
        if mode.mouseOver == "tradButt" or mode.gamemode == "traditional":
            canvas.create_rectangle(mode.tradButtX0, mode.tradButtY0, mode.tradButtX1, mode.tradButtY1, fill="#004990")
        if mode.mouseOver == "tossupButt" or mode.gamemode != "traditional":
            canvas.create_rectangle(mode.tuButtX0, mode.tuButtY0, mode.tuButtX1, mode.tuButtY1, fill="#004990")
        
        if mode.mouseOver == "hasDrawButt" or mode.hasDrawing:
            canvas.create_rectangle(mode.hasDrawButtX0, mode.hasDrawButtY0, mode.hasDrawButtX1, mode.hasDrawButtY1, fill="#004990")
        if mode.mouseOver == "noDrawButt" or not mode.hasDrawing:
            canvas.create_rectangle(mode.noDrawButtX0, mode.noDrawButtY0, mode.noDrawButtX1, mode.noDrawButtY1, fill="#004990")

        if mode.mouseOver == "easyButt" or mode.gameDifficulty == 1:
            canvas.create_rectangle(mode.easyButtX0, mode.easyButtY0, mode.easyButtX1, mode.easyButtY1, fill="#004990")
        if mode.mouseOver == "medButt" or mode.gameDifficulty == 2:
            canvas.create_rectangle(mode.medButtX0, mode.medButtY0, mode.medButtX1, mode.medButtY1, fill="#004990")
        if mode.mouseOver == "hardButt" or mode.gameDifficulty == 3:
            canvas.create_rectangle(mode.hardButtX0, mode.hardButtY0, mode.hardButtX1, mode.hardButtY1, fill="#004990")
        if mode.mouseOver == "ultraButt" or mode.gameDifficulty == 4:
            canvas.create_rectangle(mode.ultraButtX0, mode.ultraButtY0, mode.ultraButtX1, mode.ultraButtY1, fill="#004990")
        
        if mode.mouseOver == "setRoundButt":
            canvas.create_rectangle(mode.setRoundButtX0, mode.setRoundButtY0, mode.setRoundButtX1, mode.setRoundButtY1, fill="#004990")
        if mode.mouseOver == "resetRoundButt":
            canvas.create_rectangle(mode.resetRoundButtX0, mode.resetRoundButtY0, mode.resetRoundButtX1, mode.resetRoundButtY1, fill="#004990")

        if mode.mouseOver == "startButt":
            canvas.create_rectangle(mode.startButtX0, mode.startButtY0, mode.startButtX1, mode.startButtY1, fill="#004990")

        canvas.create_text((mode.tradButtX0 + mode.tradButtX1)/2, (mode.tradButtY0 + mode.tradButtY1)/2, text="Traditional", fill="white", font="Ariel 12")
        canvas.create_text((mode.tuButtX0 + mode.tuButtX1)/2, (mode.tuButtY0 + mode.tuButtY1)/2, text="Tossups only", fill="white", font="Ariel 12")

        canvas.create_text((mode.hasDrawButtX0 + mode.hasDrawButtX1)/2, (mode.hasDrawButtY0 + mode.hasDrawButtY1)/2, text="Include Drawing Bonuses", fill="white", font="Ariel 12")
        canvas.create_text((mode.noDrawButtX0 + mode.noDrawButtX1)/2, (mode.noDrawButtY0 + mode.noDrawButtY1)/2, text="No Drawing Bonuses", fill="white", font="Ariel 12")

        canvas.create_text((mode.easyButtX0 + mode.easyButtX1)/2, (mode.easyButtY0 + mode.easyButtY1)/2, text="Easy", fill="white", font="Ariel 12")
        canvas.create_text((mode.medButtX0 + mode.medButtX1)/2, (mode.medButtY0 + mode.medButtY1)/2, text="Medium", fill="white", font="Ariel 12")
        canvas.create_text((mode.hardButtX0 + mode.hardButtX1)/2, (mode.hardButtY0 + mode.hardButtY1)/2, text="Hard", fill="white", font="Ariel 12")
        canvas.create_text((mode.ultraButtX0 + mode.ultraButtX1)/2, (mode.ultraButtY0 + mode.ultraButtY1)/2, text="Ultra", fill="white", font="Ariel 12")

        canvas.create_text((mode.setRoundButtX0 + mode.setRoundButtX1)/2, (mode.setRoundButtY0 + mode.setRoundButtY1)/2, text="Select Round", fill="white", font="Ariel 12")
        canvas.create_text((mode.resetRoundButtX0 + mode.resetRoundButtX1)/2, (mode.resetRoundButtY0 + mode.resetRoundButtY1)/2, text="Reset List of Played Rounds", fill="white", font="Ariel 12")
        
        canvas.create_text((mode.startButtX0 + mode.startButtX1)/2, (mode.startButtY0 + mode.startButtY1)/2, text="Start!", fill="white", font="Ariel 12")

        canvas.create_text((mode.tradButtX0 + mode.tradButtX1)/2, mode.tradButtY0-50, text="Select Game Mode:", font="Ariel 16 bold")
        canvas.create_text((mode.hasDrawButtX0 + mode.hasDrawButtX1)/2, mode.hasDrawButtY0-50, text="Include Drawing Bonuses?", font="Ariel 16 bold")
        canvas.create_text(mode.app.width/2, mode.easyButtY0-50, text="Select Game Difficulty", font="Ariel 16 bold")
        canvas.create_text(mode.app.width/2, mode.setRoundButtY0-75, text="Select Question Set", font="Ariel 16 bold")
        canvas.create_text(mode.app.width/2, mode.setRoundButtY0-50, text="Input the number of the round you want to play, or leave it blank to randomly select a round you've never seen before", font="Ariel 14")


class GameSetup(Mode):
    def appStarted(mode):
        if mode.app.roundNum == 0: # if no set is picked, chose randomly
            while True:
                mode.app.roundNum = random.randint(1,16)
                with open("questionSets/setsRead.txt", "r") as file:
                    setList = file.read().split(" ")
                    if len(setList) >= 15:
                        break
                    if str(mode.app.roundNum) not in setList:
                        break

        # parse the question set and note that it's been read
        # using a tip from here: https://stackoverflow.com/a/56381383
        with open("questionSets/setsRead.txt", "r+") as file:
            setList = file.read().split(" ")
            if str(mode.app.roundNum) not in setList:
                file.write(str(mode.app.roundNum) + " ")
        
        filename = f"questionSets/round{mode.app.roundNum}.pdf"
        
        with open(parse(filename)) as f:
            mode.app.questionSet = json.load(f)

        # initialize the game
        mode.app.p1, mode.app.p2, mode.app.p3, mode.app.p4 = createTeam(mode.app.gameDifficulty)
        mode.app.questionNum = 0
        mode.app.bonusNum = 1
        mode.app.startTime = time.time() # rounds last 16min or until all questions have been read
        mode.app.yourScore = 0
        mode.app.opponentScore = 0
    
    def keyPressed(mode, event):
        if event.key == "Space": # press space to start the first tossup
            mode.app.questionNum+= 1
            mode.app.setActiveMode(mode.app.tossup)
        elif event.key == "p":
            mode.app.lastMode = mode.app.gameSetup
            mode.app.setActiveMode(mode.app.gamePaused)
    
    def redrawAll(mode, canvas):
        canvas.create_text(mode.app.width/2, mode.app.height/2, text="Press SPACE to start the first tossup!")

class Tossup(Mode):
    def appStarted(mode):
        mode.resetBuzzer()

    def resetBuzzer(mode):
        if mode.app.questionNum > 25:
            mode.app.setActiveMode(mode.app.gameOver)
        else:
            mode.buzzTime = time.time() + 30000
            mode.buzzed = ""

            mode.correct = None
            mode.buzzerOn = False

            mode.currentQ = mode.app.questionSet["Tossup Questions"][mode.app.questionNum - 1]["Text"]
            mode.currentQ = formatQs(mode.currentQ, 200)
            mode.qtype = mode.app.questionSet["Tossup Questions"][mode.app.questionNum - 1]["Field"].strip()
            mode.qlen = mode.currentQ.count(" ")/4 # loosly based on https://www.researchgate.net/publication/332380784_How_many_words_do_we_read_per_minute_A_review_and_meta-analysis_of_reading_rate
            # I used 240 wpm for reading rate because it came out to a neat 4 wps
            mode.w = mode.app.questionSet["Tossup Questions"][mode.app.questionNum - 1]["W"]
            mode.x = mode.app.questionSet["Tossup Questions"][mode.app.questionNum - 1]["X"]
            mode.y = mode.app.questionSet["Tossup Questions"][mode.app.questionNum - 1]["Y"]
            mode.z = mode.app.questionSet["Tossup Questions"][mode.app.questionNum - 1]["Z"]

            # generates the buzzer values for the oppoents
            mode.cor1, mode.speed1, mode.app.cer1 = mode.app.p1.getBuzz(mode.qtype)
            mode.cor2, mode.speed2, mode.app.cer2 = mode.app.p2.getBuzz(mode.qtype)
            mode.cor3, mode.speed3, mode.app.cer3 = mode.app.p3.getBuzz(mode.qtype)
            mode.cor4, mode.speed4, mode.app.cer4 = mode.app.p4.getBuzz(mode.qtype)

            mode.speed1 *= mode.qlen
            mode.speed2 *= mode.qlen
            mode.speed3 *= mode.qlen
            mode.speed4 *= mode.qlen

            mode.qtime = mode.qlen + 7 # in this case, the magic number is pulled from the rulebook (you get 7 sec to answer)
            mode.app.tuStart = time.time()
            mode.buzzerOn = True
            mode.qAnswer = mode.app.questionSet["Tossup Questions"][mode.app.questionNum - 1]["Answer"]


    def keyPressed(mode, event):
        if event.key == "Space" and mode.buzzerOn:
            mode.buzzed = "You"
            mode.buzzerOn = False
            while True:
                answer = simpledialog.askstring("Answer Box", "What is you answer?")
                if answer == None:
                    print("You must answer")
                else:
                    answer = answer.upper()
                    answer = answer.strip()
                    break
            mode.buzzTime = time.time()
            if answer in mode.qAnswer and answer != "":
                mode.correct = True
                mode.app.questionNum += 1
                mode.app.yourScore += 4
            else:
                mode.correct = False
                mode.app.questionNum += 1

        elif event.key == 'p':
            mode.app.lastMode = mode.app.tossup
            mode.app.setActiveMode(mode.app.gamePaused)

    def timerFired(mode):
        # is it a dead q?
        if mode.buzzerOn and mode.app.tuStart + mode.qtime < time.time():
            mode.buzzerOn = False
            mode.app.questionNum += 1
            mode.buzzTime = time.time()

        # have any of the opponents buzzed?
        elif mode.buzzerOn and mode.app.tuStart + mode.speed1 < time.time():
            mode.buzzed = mode.app.p1.name
            mode.buzzerOn = False
            if mode.cor1:
                mode.correct = True
                mode.app.opponentScore += 4
            else:
                mode.correct = False
            mode.app.questionNum += 1
            mode.buzzTime = time.time()

        elif mode.buzzerOn and mode.app.tuStart + mode.speed2 < time.time():
            mode.buzzed = mode.app.p2.name
            mode.buzzerOn = False
            if mode.cor2:
                mode.correct = True
                mode.app.opponentScore += 4
            else:
                mode.correct = False
            mode.app.questionNum += 1
            mode.buzzTime = time.time()

        elif mode.buzzerOn and mode.app.tuStart + mode.speed3 < time.time():
            mode.buzzed = mode.app.p3.name
            mode.buzzerOn = False
            if mode.cor3:
                mode.correct = True
                mode.app.opponentScore += 4
            else:
                mode.correct = False
            mode.app.questionNum += 1
            mode.buzzTime = time.time()

        elif mode.buzzerOn and mode.app.tuStart + mode.speed4 < time.time():
            mode.buzzed = mode.app.p4.name
            mode.buzzerOn = False
            if mode.cor4:
                mode.correct = True
                mode.app.opponentScore += 4
            else:
                mode.correct = False
            mode.app.questionNum += 1
            mode.buzzTime = time.time()

        elif not mode.buzzerOn:
            if time.time() > mode.buzzTime + 2:
                if mode.correct and mode.buzzed == "You" and mode.app.gamemode == "traditional":
                    mode.resetBuzzer()
                    mode.app.setActiveMode(mode.app.bonus)
                else:
                    mode.resetBuzzer()

    def appStopped(self):
        self.messages.append('appStopped')
        print('appStopped!')

    def redrawAll(mode, canvas):
        if mode.currentQ == "": # if there's no question (SHOULD NOT HAPPEN!!!)
            canvas.create_text(mode.app.width/2, mode.app.height/2, text="press SPACE to start the next question")
        
        elif not mode.buzzerOn and mode.buzzed == "": # Timed out
            canvas.create_rectangle(0,0, mode.app.width, mode.app.height, fill="red")
            canvas.create_text(mode.app.width/2, mode.app.height/2 - 50, text="Your time is up!")
            canvas.create_text(mode.app.width/2, mode.app.height/2 - 50, text=f"The answer was {mode.qAnswer}!")
        
        elif mode.correct == True: # someone got it!!
            canvas.create_rectangle(0,0, mode.app.width, mode.app.height, fill="green")
            canvas.create_text(mode.app.width/2, mode.app.height/2 + 50, text=f"{mode.buzzed} answered correctly!")
        
        elif mode.correct == False: # someone was wrong :(
            canvas.create_rectangle(0,0, mode.app.width, mode.app.height, fill="red")
            canvas.create_text(mode.app.width/2, mode.app.height/2, text=f"{mode.buzzed} answered incorrectly")
            canvas.create_text(mode.app.width/2, mode.app.height/2 + 50, text=f"The answer was {mode.qAnswer}!")
        
        else:
            if mode.w == None: # if short answer
                canvas.create_text(mode.app.width/2, mode.app.height/2 - 50, text=mode.currentQ)
                canvas.create_text(mode.app.width/2, mode.app.height/2, text="press SPACE to buzz")
            else:
                canvas.create_text(mode.app.width/2, mode.app.height/2 - 100, text=mode.currentQ)
                canvas.create_text(mode.app.width/2, mode.app.height/2 - 50, text=mode.w)
                canvas.create_text(mode.app.width/2, mode.app.height/2 - 25, text=mode.x)
                canvas.create_text(mode.app.width/2, mode.app.height/2, text=mode.y)
                canvas.create_text(mode.app.width/2, mode.app.height/2 + 25, text=mode.z)
                canvas.create_text(mode.app.width/2, mode.app.height/2 + 75, text="press SPACE to buzz")

# still from the tech demo because it still works
def formatQs(text, lineLen):
    if len(text) < lineLen:
        return text
    else:
        pos = lineLen
        while pos < len(text):
            '''if "\n" in text[pos-lineLen:pos]:
                pos += lineLen
            '''
            if text[pos] == " ":
                text = text[:pos] + "\n" + text[pos+1:]
                pos += lineLen
            else:
                pos += 1
        return text

def formatRules(text, lineLen):
    textList = text.splitlines()
    text = ""
    for line in textList:
        if len(line) < lineLen:
            text += line + "\n\n"
        else:
            pos = lineLen
            while pos < len(line):
                if line[pos] == " ":
                    line = line[:pos] + "\n\n" + line[pos+1:]
                    pos += lineLen
                else:
                    pos += 1
            text += line + "\n\n"
    return text

def isLine(stroke):
    if len(stroke) < 2: # if it's not a line, don't bother checking
        return False, 0, 0, 0, 0, 0
    
    x0, x1 = stroke[0][0], stroke[-1][0]
    y0, y1 = stroke[0][1], stroke[-1][1]

    # uses a linear regression to guess what line a stroke would be if it were a line
    # formula from Khan Academy, because they rock (https://www.khanacademy.org/math/statistics-probability/describing-relationships-quantitative-data/more-on-regression/v/regression-line-example)
    meanX = meanY = meanXY = meanXsqrd = 0
    for dot in stroke:
        meanX += dot[0]
        meanY += dot[1]
        meanXY += dot[0]*dot[1]
        meanXsqrd += dot[0]**2
    meanX /= len(stroke)
    meanY /= len(stroke)
    meanXY /= len(stroke)
    meanXsqrd /= len(stroke)

    mNumerator = meanX*meanY - meanXY
    mDenominator = meanX**2 - meanXsqrd
    try: 
        m = mNumerator/mDenominator
    except ZeroDivisionError:
        # if you manage to draw something that would be a perfectly straight line,
        # m should be basically infinity
        m = 1.7976931348623157e+308

    b = meanY - m*meanX

    # now we get our R to see how well our generated line fits the stroke
    # formula again from Khan Academy (https://www.khanacademy.org/math/ap-statistics/bivariate-data-ap/correlation-coefficient-r/v/calculating-correlation-coefficient-r)
    # thank you Sal Khan; you're a total bro
    stdevX = stdevY = 0 # standard deviations
    for dot in stroke:
        stdevX += (dot[0] - meanX)**2
        stdevY += (dot[1] - meanY)**2
    stdevX /= len(stroke) - 1
    stdevY /= len(stroke) - 1
    stdevX **= .5
    stdevY **= .5

    if stdevX == 0 or stdevY == 0: 
        # if this is true, it's a perfect vertical or horisontal line
        # so don't bother with the rest
        # (also if stdev = 0, a z score is meaningless, so I can't get R)
        return True, m, x0, y0, x1, y1

    R = 0
    for dot in stroke:
        XZscore = (dot[0] - meanX)/stdevX
        YZscore = (dot[1] - meanY)/stdevY
        R += XZscore*YZscore
    R /= len(stroke) - 1
    R = abs(R) # technically R is + or -. But I don't want to deal with negative numbers

    # R is a measure of how data corralates
    # so if R is high, your data is very liney and if it's low, your data isn't very liney
    # if a given stroke has a high R, it's catagorized as a line. Otherwise, it's not
    return (R > .6), m, x0, y0, x1, y1

# returns a tuple containing a bool and 3 floats
# the bool True if a given stroke is a circle; the floats are the radius, and the coords of the center of the circle
def isCircle(stroke):
    if len(stroke) < 3: # if it's not at least a triangle, don't bother checking
        return False, 0, 0, 0

    cX = cY = cR = 0
    for dot in stroke:
        cX += dot[0]
        cY += dot[1]
    cX /= len(stroke)
    cY /= len(stroke)

    for dot in stroke:
        cR += ((cX - dot[0])**2 + (cY - dot[1])**2)**.5
    cR /= len(stroke)

    # compared to line detection, circle detection is much simpler
    # if the start and end of a stroke are close together, it's a circle
    x0, y0 = stroke[0][0], stroke[0][1]
    xn, yn = stroke[-1][0], stroke[-1][1]
    return (abs(x0-xn) < .75*cR and abs(y0-yn) < .75*cR), cX, cY, cR
    # if I get a chance, I will add a conditional that rules out figure-8s

# returns a tuple containing a bool and 2 floats
# the bool True if a given stroke is a dot; the floats are the coords of the dot
def isDot(stroke):
    x = stroke[0][0]
    y = stroke[0][1]
    return (len(stroke) == 1), x, y

class Bonus(Mode):
    def appStarted(mode):
        mode.resetBonus()

    def resetBonus(mode):
        if random.random() > 0 and mode.app.hasDrawing:
            mode.app.setActiveMode(mode.app.drawingBonus)
        mode.buzzTime = time.time() + 30000
        if mode.app.bonusNum > 25:
            mode.app.setActiveMode(mode.app.gameOver)

        mode.correct = None
        mode.buzzerOn = False

        mode.currentQ = mode.app.questionSet["Bonus Questions"][mode.app.bonusNum - 1]["Text"]
        mode.currentQ = formatQs(mode.currentQ, 200)
        mode.qtype = mode.app.questionSet["Bonus Questions"][mode.app.bonusNum - 1]["Field"].strip()
        mode.qlen = mode.currentQ.count(" ")/4 # loosly based on https://www.researchgate.net/publication/332380784_How_many_words_do_we_read_per_minute_A_review_and_meta-analysis_of_reading_rate
        # I used 240 wpm for reading rate because it came out to a neat 4 wps
        mode.w = mode.app.questionSet["Bonus Questions"][mode.app.bonusNum - 1]["W"]
        mode.x = mode.app.questionSet["Bonus Questions"][mode.app.bonusNum - 1]["X"]
        mode.y = mode.app.questionSet["Bonus Questions"][mode.app.bonusNum - 1]["Y"]
        mode.z = mode.app.questionSet["Bonus Questions"][mode.app.bonusNum - 1]["Z"]
        
        mode.qtime = mode.qlen + 20 # in this case, the magic number is pulled from the rulebook (you get 7 sec to answer)
        mode.app.tuStart = time.time()
        mode.buzzerOn = True
        mode.qAnswer = mode.app.questionSet["Bonus Questions"][mode.app.bonusNum - 1]["Answer"]


    def keyPressed(mode, event):
        if event.key == "Space" and mode.buzzerOn:
            mode.buzzed = "You"
            mode.buzzerOn = False
            while True:
                answer = simpledialog.askstring("Answer Box", "What is you answer?")
                if answer == None:
                    print("You must answer")
                else:
                    answer = answer.upper()
                    break
            if answer in mode.qAnswer:
                mode.app.yourScore += 10
                mode.correct = True
                mode.app.bonusNum += 1
                mode.buzzTime = time.time()
            else:
                mode.correct = False
                mode.app.bonusNum += 1
                mode.buzzTime = time.time()
        elif event.key == 'p':
            mode.app.lastMode = mode.app.gameSetup
            mode.app.setActiveMode(mode.app.gamePaused)

    def timerFired(mode):
        # is it a dead q?
        if mode.buzzerOn and mode.app.tuStart + mode.qtime < time.time():
            mode.buzzerOn = False
            mode.app.questionNum += 1
            mode.buzzTime = time.time()

        elif not mode.buzzerOn:
            if time.time() > mode.buzzTime + 2:
                mode.resetBonus()
                mode.app.tuStart = time.time()
                mode.app.setActiveMode(mode.app.tossup)

    def redrawAll(mode, canvas):
        if mode.currentQ == "": # if there's no question (SHOULD NOT HAPPEN!!!)
            canvas.create_text(mode.app.width/2, mode.app.height/2, text="press SPACE to start the next question")
        
        elif not mode.buzzerOn and mode.buzzed == "": # Timed out
            canvas.create_rectangle(0,0, mode.app.width, mode.app.height, fill="red")
            canvas.create_text(mode.app.width/2, mode.app.height/2 - 50, text="Your time is up!")
            canvas.create_text(mode.app.width/2, mode.app.height/2 - 50, text=f"The answer was {mode.qAnswer}!")
        
        elif mode.correct == True: # someone got it!!
            canvas.create_rectangle(0,0, mode.app.width, mode.app.height, fill="green")
            canvas.create_text(mode.app.width/2, mode.app.height/2 + 50, text=f"{mode.buzzed} answered correctly!")
        
        elif mode.correct == False: # someone was wrong :(
            canvas.create_rectangle(0,0, mode.app.width, mode.app.height, fill="red")
            canvas.create_text(mode.app.width/2, mode.app.height/2, text=f"{mode.buzzed} answered incorrectly")
            canvas.create_text(mode.app.width/2, mode.app.height/2 + 50, text=f"The answer was {mode.qAnswer}!")
        
        else:
            if mode.w == None: # if short answer
                canvas.create_text(mode.app.width/2, mode.app.height/2 - 50, text=mode.currentQ)
                canvas.create_text(mode.app.width/2, mode.app.height/2, text="press SPACE to buzz")
            else:
                canvas.create_text(mode.app.width/2, mode.app.height/2 - 100, text=mode.currentQ)
                canvas.create_text(mode.app.width/2, mode.app.height/2 - 50, text=mode.w)
                canvas.create_text(mode.app.width/2, mode.app.height/2 - 25, text=mode.x)
                canvas.create_text(mode.app.width/2, mode.app.height/2, text=mode.y)
                canvas.create_text(mode.app.width/2, mode.app.height/2 + 25, text=mode.z)
                canvas.create_text(mode.app.width/2, mode.app.height/2 + 75, text="press SPACE to buzz")

class DrawingBonus(Mode):
    def appStarted(mode):
        with open("drawingQuestionSet.json") as f:
            mode.drawingQuestionSet = json.load(f)

        mode.resetDrawingBonus()

    def resetDrawingBonus(mode):
        mode.dots = []
        mode.lineList = []
        mode.circleList = []
        mode.buzzTime = time.time() + 3000000
        mode.correct = None

        mode.question = random.choice(mode.drawingQuestionSet["Questions"])
        mode.questionText = formatQs(mode.question["Text"], 200)
        mode.answer = mode.question["Answer"]

    def keyPressed(mode, event):
        if event.key == 'r':
            mode.dots = []
            mode.lineList = []
            mode.circleList = []
        elif event.key == 'z':
            mode.dots.pop()
        elif event.key == 'Space':
            mode.buzzTime = time.time()
            if mode.scoreDrawing():
                mode.correct = True
                mode.app.yourScore += 20
            else:
                mode.correct = False
        elif event.key == 'p':
            mode.app.lastMode = mode.app.drawingBonus
            mode.app.setActiveMode(mode.app.gamePaused)
    
    def countHs(mode):
        hCount = 0
        for strokeI in range(len(mode.dots)-2):
            lineData0 = isLine(mode.dots[strokeI + 0])
            lineData1 = isLine(mode.dots[strokeI + 1])
            lineData2 = isLine(mode.dots[strokeI + 2])

            bool0 = lineData0[0]
            bool1 = lineData1[0]
            bool2 = lineData2[0]
            if not(bool0 and bool1 and bool2): continue
            # if not all of the strokes are lines, don't bother
            
            mList = [None, None, None]
            mList[0] = abs(lineData0[1])
            mList[1] = abs(lineData1[1])
            mList[2] = abs(lineData2[1])
            
            # checks that two lines are vertical and the other is horisontal
            # hT is the max slope for a line to be horisontal and vT is the min slope to be vertical
            hT, vT = .25, 5
            if mList[0] < hT: # checks that line0 is horis. and line1 and line2 are vert.
                # idk who the heck draws their Hs crossbar first
                # but if that's you, this is the test for you
                if not (mList[1] > vT and mList[2] > vT): continue
                else: crossbar, side1, side2 = 0, 1, 2
            
            elif mList[1] < hT: # checks that line1 is horis. and line0 and line2 are vert.
                # if this one is you, congrats; you're normal
                if not (mList[0] > vT and mList[2] > vT): continue
                else: crossbar, side1, side2 = 1, 0, 2

            elif mList[2] < hT: # checks that line2 is horis. and line0 and line1 are vert.
                # if this one is you, congrats; you're also normal
                if not (mList[0] > vT and mList[1] > vT): continue
                else: crossbar, side1, side2 = 2, 0, 1
            
            else: continue # if none of the lines are horis. it's not an H

            coordList = [None, None, None]
            # each entry takes the form (x0, y0, x1, y0)
            coordList[0] = (lineData0[2], lineData0[3], lineData0[4], lineData0[5])
            coordList[1] = (lineData1[2], lineData1[3], lineData1[4], lineData1[5])
            coordList[2] = (lineData2[2], lineData2[3], lineData2[4], lineData2[5])

            # get the x midpoint of each line
            crossbarX = (coordList[crossbar][0]+coordList[crossbar][2])/2
            side1X = (coordList[side1][0]+coordList[side1][2])/2
            side2X = (coordList[side2][0]+coordList[side2][2])/2
            
            # if the crossbar isn't in between the two sides in the x direction, it's not an H
            if not(min(side1X, side2X) < crossbarX < max(side1X, side2X)): continue

            # get the top and bottom of the H
            crossbarY = (coordList[crossbar][1]+coordList[crossbar][3])/2
            topY = (coordList[side1][1]+coordList[side2][1])/2
            bottomY = (coordList[side1][3]+coordList[side2][3])/2
            
            # if the crossbar isn't in between the two sides in the Y direction, it's not an H
            if not(min(topY, bottomY) < crossbarY < max(topY, bottomY)): continue

            # if it satisfies all the above, it's probably an H
            hCount += 1
        return hCount

    def countOs(mode):
        oCount = 0
        for stroke in mode.dots:
            if isCircle(stroke)[0]: oCount += 1
        return oCount

    def countDots(mode):
        dotCount = 0
        for stroke in mode.dots:
            if isDot(stroke)[0]: dotCount += 1
        return dotCount

    def countLines(mode):
        lineCount = 0
        for stroke in mode.dots:
            if isLine(stroke)[0]: lineCount += 1
        lineCount -= mode.countHs()*3 # if it's part of an H, it doesn't count
        return lineCount
    
    def countMisc(mode):
        miscCounts = len(mode.dots)
        miscCounts -= mode.countHs()*3
        miscCounts -= mode.countOs()
        miscCounts -= mode.countDots()
        miscCounts -= mode.countLines()
        return miscCounts

    def scoreDrawing(mode):
        drawingStats = [mode.countHs(), mode.countOs(), mode.countDots()//2, mode.countLines(), mode.countMisc()]
        correctStats = mode.answer # num Hs, num Os, num electron pairs, num bonds, num Cs
        print(drawingStats, correctStats)
        return drawingStats == correctStats
    
    def mousePressed(mode, event):
        mode.dots.append([])
        location = (event.x, event.y)
        mode.dots[-1].append(location)

    def mouseDragged(mode, event):
        location = (event.x, event.y)
        mode.dots[-1].append(location)

    def timerFired(mode):
        if time.time() > mode.buzzTime + 2:
            mode.resetDrawingBonus()
            mode.app.tuStart = time.time()
            mode.app.setActiveMode(mode.app.tossup)
        else:
            mode.lineList = []
            mode.circleList = []
            for stroke in mode.dots:
                if True:#isLine(stroke)[0]:
                    mode.lineList.append(isLine(stroke))
                elif True:#isCircle(stroke)[0]:
                    mode.circleList.append(isCircle(stroke))
    
    def redrawAll(mode, canvas):
        if mode.correct == None:
            canvas.create_text(mode.app.width/2, 50, text=f"{mode.questionText}")
            canvas.create_text(mode.app.width/2, 100, text="Press the MOUSE to draw. Hit Z to undo a stroke, R to start over and SPACE to submit.")
            for stroke in mode.dots:
                lastCoords = None
                for coords in stroke:
                    if len(stroke) == 1:
                        canvas.create_oval(coords[0]-1, coords[1]-1, coords[0]+1, coords[1]+1, fill="black")
                    else:
                        if lastCoords != None:
                            canvas.create_line(lastCoords[0], lastCoords[1], coords[0], coords[1])
                        lastCoords = coords
        elif mode.correct:
            canvas.create_rectangle(0, 0, mode.app.width, mode.app.height, fill="green")
            canvas.create_text(mode.app.width/2, mode.app.height/2, text="Correct!")
        else:
            canvas.create_rectangle(0, 0, mode.app.width, mode.app.height, fill="red")
            canvas.create_text(mode.app.width/2, mode.app.height/2, text="Incorrect!")

class GamePaused(Mode):
    def keyPressed(mode, event):
        if event.key == "p":
            mode.app.setActiveMode(mode.app.lastMode)
    def redrawAll(mode, canvas):
        canvas.create_text(mode.app.width/2, mode.app.height/2, text="Game Paused")

class GameOver(Mode):
    def redrawAll(mode, canvas):
        canvas.create_text(mode.app.width/2, mode.app.height/2, text=f"Your score:{mode.app.yourScore}, Other Team's score: {mode.app.opponentScore}")

class NerdSimulatorBowl(ModalApp):
    def appStarted(app):
        app.splashScreen = SplashScreen()
        app.gameHelp = GameHelp()
        app.gameSettings = GameSettings()
        app.gameSetup = GameSetup()
        app.tossup = Tossup()
        app.bonus = Bonus()
        app.drawingBonus = DrawingBonus()
        app.gamePaused = GamePaused()
        app.gameOver = GameOver()

        app.setActiveMode(app.splashScreen)
        app.timerDelay = 50

app = NerdSimulatorBowl(width=1500, height=800)