# pdf parser v 1.2
# copyright 2020 Juno Hoffman

# this entire file is devoted to one function: parse
# parse() takes a path to a pdf and creates a JSON table of all the questions in the pdf
# still cannot take compressed pdfs

import re, json

def parse(path):
    # gets the pdf's guts (a long, mostly nonsence, string)
    pdf = open(path, encoding="unicode-escape", mode='r') # used https://stackoverflow.com/a/64847233
    pdfGuts = pdf.read()
    pdf.close()

    docString = ''
    inBrackets = False
    isText = False
    prevChar = None

    # for pdfs, text is usually formatted like so: [(H)5.1 (i)6.9 (gh)12 ( S)7.7 (c)-7.8 (h)12 (ool)6.9 ( )]TJ
    # to get rid of the other crud, we only want the stuff in the parentheses, so this loop gets rid of everthing else
    for index in range(len(pdfGuts)):
        char = pdfGuts[index]
    
        # had some issues with text in the form "junk[more junk(even more junk..." regestering as actual text
        # so this conditional only sets inBrackets if the program sees "[("
        if char == '(' and pdfGuts[index-1] == '[':
            inBrackets = True
            isText = True
        
        # this next one's a bit complicated. Some text isn't in brackets and then parenthisies
        # instead it's in the form (text)Tj
        # but as I said above, I can't just use anything after a parenthisis or I get a BUNCH of junk
        # so when the code sees a lone parenthisis (so not in brackets) it looks ahead to see if it can find
        # the corrosponding )Tj
        elif char == '(' and not inBrackets:
            peekAheadIndex = index
            while peekAheadIndex < index + 10:
                peekAheadStr = pdfGuts[peekAheadIndex-2:peekAheadIndex+1]
                if peekAheadStr == ")Tj":
                    inBrackets = True
                    isText = True
                    break
                elif '[' in peekAheadStr:
                    inBrackets = False
                    isText = False
                    break
                peekAheadIndex += 1

        elif char == ']':
            inBrackets = False

        # special characters are put after \s just like python
        # this doesn't act on parentheses that are after a \
        elif char == '(' and pdfGuts[index-1] != "\\":
           isText = True
        elif char == ')' and pdfGuts[index-1] != "\\":
           isText = False
        elif pdfGuts[index-2:index+1] == ")Tj":
            isText = False
            inBrackets = False
        # \s are usally nonsence, so ignore them
        elif isText and inBrackets and char != "\\":
            docString += char
    
    # make that JSON!   
    createJSONset(docString)
    return "questionSet.json"
    
def createJSONset(docString):
    qSet = dict()
    qSet["Tossup Questions"] = []
    qSet["Bonus Questions"] = []

    # there's a bunch of headers still in the pdf with page numbers 'n' stuff
    # fun fact: page numbers aren't science questions!
    headerPattern = re.compile(r'    High School Round \d     Page \d{1,2}')
    docList = headerPattern.split(docString)
    docString = ""
    for string in docList:
        docString += string

    qSet = getSATossup(docString, qSet)
    qSet = getSABonus(docString, qSet)
    qSet = getMCTossup(docString, qSet)
    qSet = getMCBonus(docString, qSet)
   
    # make that JSON!!!
    with open('questionSet.json', 'w') as file:
        json.dump(qSet, file)
        
def getSATossup(docString, qSet):
    # I don't know very much about regex, but I think I know what I'm doing
    # note: I copied no code for this but I used this video: https://youtu.be/K8L6KVGG-7o
    saTossupPattern = re.compile(r'TOSS-UP  \d.{1,50}Short Answer') 
    # filter for things in pattern TOSS and then a digit, 
    # then some characters, and then "Short Answer"
    saTossups = saTossupPattern.finditer(docString)
    for tossup in saTossups:
        tempDict = dict()
        pos = tossup.start() # keeps track of the position of the data we're looking at

        # sets the question number
        if tossup.group()[5] in ['0','1','2','3','4','5','6','7','8','9']: # is it a 2 digit num?
            tempDict["Question"] = int(tossup.group()[9:11])
            pos += 14
        else:
            tempDict["Question"] = int(tossup.group()[9])
            pos += 13
        
        # sets the field
        fieldStr = ""
        while docString[pos].isupper() or docString[pos] == " ": # break on the h of Short Answer
            fieldStr += docString[pos]
            pos += 1
        
        # get rid of the stuff that isn't the type
        fieldStr = fieldStr[:-1]
        fieldStr = fieldStr.strip()

        tempDict["Field"] = fieldStr

        # set the type to short answer
        tempDict["Type"] = "sa"

        # get question text
        pos = tossup.end()
        qStr = ""
        while docString[pos:pos + 6] != "ANSWER":
            qStr += docString[pos]
            pos += 1
        tempDict["Text"] = qStr.strip()
        pos += 9

        # set choices to null
        tempDict["W"] = None
        tempDict["X"] = None
        tempDict["Y"] = None
        tempDict["Z"] = None

        # set answerline
        ansStr = ""
        while docString[pos:pos + 5] != "BONUS":
            ansStr += docString[pos]
            pos += 1
        tempDict["Answer"] = ansStr.strip()

        # add the question to the question list
        qSet["Tossup Questions"].append(tempDict)

    return qSet

def getSABonus(docString, qSet):
    saBonusPattern = re.compile(r'BONUS  \d.{1,50}Short Answer') 
    # same as before, just now looking for bonuses
    saBonuses = saBonusPattern.finditer(docString)
    for bonus in saBonuses:
        tempDict = dict()
        pos = bonus.start() # keeps track of the position of the data we're looking at

        # sets the question number
        if bonus.group()[8] in ['0','1','2','3','4','5','6','7','8','9']: # is it a 2 digit num?
            tempDict["Question"] = int(bonus.group()[7:9])
            pos += 12
        else:
            tempDict["Question"] = int(bonus.group()[7])
            pos += 11
        
        # sets the field
        fieldStr = ""
        while docString[pos].isupper() or docString[pos] == " ": # break on the h of Short Answer
            fieldStr += docString[pos]
            pos += 1
        
        # get rid of the stuff that isn't the type
        fieldStr = fieldStr[:-1]
        fieldStr = fieldStr.strip()

        tempDict["Field"] = fieldStr

        # set the type to short answer
        tempDict["Type"] = "sa"

        # get question text
        pos = bonus.end()
        qStr = ""
        while docString[pos:pos + 6] != "ANSWER":
            qStr += docString[pos]
            pos += 1
        tempDict["Text"] = qStr.strip()
        pos += 9

        # set choices to null
        tempDict["W"] = None
        tempDict["X"] = None
        tempDict["Y"] = None
        tempDict["Z"] = None

        # set answerline
        ansStr = ""
        while pos + 4 < len(docString) and docString[pos:pos + 4] != "TOSS": 
            # using short circuit analysis to keep it from breaking on the last bonus
            ansStr += docString[pos]
            pos += 1
        tempDict["Answer"] = ansStr.strip()

        # add the question to the question list
        qSet["Bonus Questions"].append(tempDict)

    return qSet

def getMCTossup(docString, qSet):
    mcTossupPattern = re.compile(r'TOSS-UP  \d.{1,50}Multiple Choice') 
    # filter for things in pattern TOSS and then a digit, 
    # then some characters, and then "Multiple Choice"
    mcTossups = mcTossupPattern.finditer(docString)
    for tossup in mcTossups:
        tempDict = dict()
        pos = tossup.start() # keeps track of the position of the data we're looking at

        # sets the question number
        if tossup.group()[10] in ['0','1','2','3','4','5','6','7','8','9']: # is it a 2 digit num?
            tempDict["Question"] = int(tossup.group()[9:11])
            pos += 14
        else:
            tempDict["Question"] = int(tossup.group()[9])
            pos += 13
        
        # sets the field
        fieldStr = ""
        while docString[pos].isupper() or docString[pos] == " ": # break on the h of Short Answer
            fieldStr += docString[pos]
            pos += 1
        
        # get rid of the stuff that isn't the type
        fieldStr = fieldStr[:-1]
        fieldStr = fieldStr.strip()

        tempDict["Field"] = fieldStr

        # set the type to short answer
        tempDict["Type"] = "mc"

        # get question text
        pos = tossup.end()
        qStr = ""
        while docString[pos:pos + 2] != "W)":
            qStr += docString[pos]
            pos += 1
        tempDict["Text"] = qStr.strip()
        pos += 4

        # get answer choices
        ansChoice = ""
        while docString[pos:pos + 2] != "X)":
            ansChoice += docString[pos]
            pos += 1
        tempDict["W"] = ansChoice.strip()
        pos += 4

        ansChoice = ""
        while docString[pos:pos + 2] != "Y)":
            ansChoice += docString[pos]
            pos += 1
        tempDict["X"] = ansChoice.strip()
        pos += 4

        ansChoice = ""
        while docString[pos:pos + 2] != "Z)":
            ansChoice += docString[pos]
            pos += 1
        tempDict["Y"] = ansChoice.strip()
        pos += 4

        ansChoice = ""
        while docString[pos:pos + 6] != "ANSWER":
            ansChoice += docString[pos]
            pos += 1
        tempDict["Z"] = ansChoice.strip()
        pos += 9


        # set answerline
        ansStr = ""
        while docString[pos:pos + 5] != "BONUS":
            ansStr += docString[pos]
            pos += 1
        tempDict["Answer"] = ansStr.strip()

        # add the question to the question list
        qSet["Tossup Questions"].append(tempDict)

    return qSet

def getMCBonus(docString, qSet):
    mcBonusPattern = re.compile(r'BONUS  \d.{1,50}Multiple Choice') 
    # filter for things in pattern TOSS and then a digit, 
    # then some characters, and then "Multiple Choice"
    mcBonuses = mcBonusPattern.finditer(docString)
    for bonus in mcBonuses:
        tempDict = dict()
        pos = bonus.start() # keeps track of the position of the data we're looking at

        # sets the question number
        if bonus.group()[8] in ['0','1','2','3','4','5','6','7','8','9']: # is it a 2 digit num?
            tempDict["Question"] = int(bonus.group()[7:9])
            pos += 12
        else:
            tempDict["Question"] = int(bonus.group()[7])
            pos += 11
        
        # sets the field
        fieldStr = ""
        while docString[pos].isupper() or docString[pos] == " ":
            fieldStr += docString[pos]
            pos += 1
        
        # get rid of the stuff that isn't the type
        fieldStr = fieldStr[:-1]
        fieldStr = fieldStr.strip()

        tempDict["Field"] = fieldStr

        # set the type to short answer
        tempDict["Type"] = "mc"

        # get question text
        pos = bonus.end()
        qStr = ""
        while docString[pos:pos + 2] != "W)":
            qStr += docString[pos]
            pos += 1
        tempDict["Text"] = qStr.strip()
        pos += 4

        # get answer choices
        ansChoice = ""
        while docString[pos:pos + 2] != "X)":
            ansChoice += docString[pos]
            pos += 1
        tempDict["W"] = ansChoice.strip()
        pos += 4

        ansChoice = ""
        while docString[pos:pos + 2] != "Y)":
            ansChoice += docString[pos]
            pos += 1
        tempDict["X"] = ansChoice.strip()
        pos += 4

        ansChoice = ""
        while docString[pos:pos + 2] != "Z)":
            ansChoice += docString[pos]
            pos += 1
        tempDict["Y"] = ansChoice.strip()
        pos += 4

        ansChoice = ""
        while docString[pos:pos + 6] != "ANSWER":
            ansChoice += docString[pos]
            pos += 1
        tempDict["Z"] = ansChoice.strip()
        pos += 9


        # set answerline
        ansStr = ""
        while docString[pos:pos + 4] != "TOSS" and pos < len(docString):
            ansStr += docString[pos]
            pos += 1
        tempDict["Answer"] = ansStr.strip()

        # add the question to the question list
        qSet["Bonus Questions"].append(tempDict)

    return qSet