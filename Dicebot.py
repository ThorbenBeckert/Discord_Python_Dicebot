#This Bot-Version 1.0 just needs discord connection and random package to roll the Earthdawn (2015) step-based-skillchecks.

import discord
import random            


#Earthdawn diceroll with explosionquestion to roll maxed-dices additional times. INPUT is the number of dicesides and OUTPUT is a INT-List of one or more Elements.
def rollEarth(sides: int):
    value = []
    explosionquestion = random.choice(range(1, sides + 1))
    value.append(explosionquestion)
    while explosionquestion == sides:
        explosionquestion = random.choice(range(1, sides + 1))
        value.append(explosionquestion)
    return value
        

#Earthdawn step definition and the use of rollEarth-function. INPUT is the Step-size + used Karma (W6) and the OUTPUT is a INT-List of all rolled Dices (W20->W4) [dicerolls] + the sum of all dices [endvalue].
def step(Stepstep: int, Karma: int):
    StepMatrix = [[0,0,0,0,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],
                  [0,0,0,0,2],[0,0,0,1,1],[0,0,0,2,0],[0,0,1,1,0],[0,0,2,0,0],[0,1,1,0,0],[0,2,0,0,0],
                  [0,1,0,0,2],[0,1,0,1,1],[0,1,0,2,0],[0,1,1,1,0],
                  [1,0,0,0,2],[1,0,0,1,1],[1,0,0,2,0],[1,0,1,1,0],[1,0,2,0,0],[1,1,1,0,0],[1,2,0,0,0],
                  [1,1,0,0,2],[1,1,0,1,1],[1,1,0,2,0],[1,1,1,1,0],
                  [2,0,0,0,2],[2,0,0,1,1],[2,0,0,2,0],[2,0,1,1,0],[2,0,2,0,0],[2,1,1,0,0],[2,2,0,0,0],
                  [2,1,0,0,2],[2,1,0,1,1],[2,1,0,2,0],[2,1,1,1,0]]
    Sides = [20,12,10,8,6]
    dicerolls = []
    endvalue = 0
    
    if Stepstep < 4 and Stepstep > 0:
        dicerolls.extend(rollEarth(4))
        if Karma > 0:
            for i in range(Karma):
                dicerolls.extend(rollEarth(6))
        endvalue = sum(dicerolls) - (3-Stepstep)
    elif Stepstep < 41 and Stepstep > 3:
        for x in range(5):
            if StepMatrix[Stepstep-4][x] == 1:
                dicerolls.extend(rollEarth(Sides[x]))
            elif StepMatrix[Stepstep-4][x] == 2:
                dicerolls.extend(rollEarth(Sides[x]))
                dicerolls.extend(rollEarth(Sides[x]))
        if Karma > 0:
            for i in range(Karma):
                dicerolls.extend(rollEarth(6))
        endvalue = sum(dicerolls)
    return dicerolls, endvalue


def splitmessage(messagething):
    digits = [0,0,0]
    if len(messagething.split("k")) == 1:
        if len(messagething.split("mod")) == 1:
            digits[0] = [int(i) for i in messagething.split() if i.isdigit()]
            digits[1] = 0
            digits[2] = 0
        elif len(messagething.split("mod")) == 2:
            digits[0] = [int(i) for i in messagething.split("mod")[0].split() if i.isdigit()]
            digits[2] = [int(i) for i in messagething.split("mod")[1] if i.isdigit()]
            digits[2] = int(digits[2][0])
            if len(messagething.split("mod")[1].split("-")) == 2:
                digits[2] = -digits[2]
        digits[0] = int(digits[0][0])
    elif len(messagething.split("k")) == 2:
        if len(messagething.split("mod")) == 1:
            digits[0] = [int(i) for i in messagething.split("k")[0].split() if i.isdigit()]
            digits[1] = [int(i) for i in messagething.split("k")[1].split() if i.isdigit()]
            digits[2] = 0
        elif len(messagething.split("mod")) == 2:
            digits[0] = [int(i) for i in messagething.split("mod")[0].split("k")[0].split() if i.isdigit()]
            digits[1] = [int(i) for i in messagething.split("mod")[0].split("k")[1].split() if i.isdigit()]
            digits[2] = [int(i) for i in messagething.split("mod")[1] if i.isdigit()]
            digits[2] = int(digits[2][0])
            if len(messagething.split("mod")[1].split("-")) == 2:
                digits[2] = -digits[2]
        digits[0] = int(digits[0][0])
        digits[1] = int(digits[1][0])
    return digits


#Thats the real bot!
class MyClient(discord.Client):
    #Login
    async def on_ready(self):
        print("Ich bin da mit euch die Welt zu kritten")
    
    #onMessage
    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.content.startswith("^step "):
            print("Nachricht von " + str(message.author.display_name) + " enthält Inhalt: " + str(message.content[5:]))
            params = splitmessage(str(message.content[5:]))
            print(params)
            
            [dices,summing] = step(params[0],params[1])
            summing = summing + params[2]
            if summing < 0:
                summing = 0
            await message.channel.send(str(message.author.display_name) + " rolled Step " + str(params[0]) + " with " + str(params[1]) + " Karma and " + str(params[2]) + " mod.")
            await message.channel.send(str(message.author.display_name) + " gets: " + str(summing) + "  " + str(dices))

            
client = MyClient()
client.run(INPUT LINK TO BOT!!!!)
