import asyncio
import sys
import discord
from discord.ext import commands
import datetime
import webscrapper
import pickle

bot = commands.Bot(command_prefix='!?', description='Ghosts Bot')

grades = {"flex": 0, "fixed": 1, "blue": 2, "boss": 3, "blueacc": 4, "yellowacc": 5}
flex = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 5, "11": 5, "12": 5, "13": 10,
        "14": 0, "15": 10}
fixed = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 4, "10": 7, "11": 7, "12": 7, "13": 10,
         "14": 10, "15": 15, "pri": 11, "duo": 20, "tri": 28, "tet": 40, "pen": 65}
blue = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 3, "9": 6, "10": 9, "11": 10, "12": 10, "13": 15,
        "14": 15, "15": 20, "pri": 15, "duo": 20, "tri": 30, "tet": 45, "pen": 70}
boss = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 5, "9": 8, "10": 11, "11": 15, "12": 15, "13": 20,
        "14": 20, "15": 20, "pri": 20, "duo": 24, "tri": 33, "tet": 50, "pen": 100}
blueacc = {"pri": 15, "duo": 28, "tri": 35, "tet": 45, "pen": 70}
yellowacc = {"pri": 20, "duo": 35, "tri": 45, "tet": 60, "pen": 100}
startbelow = [0, 5, 3, 3, 4, 0]

failstack = [flex, fixed, blue, boss, blueacc, yellowacc]


def to_lower(argument):
    return argument.lower()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)


async def fs_error(msgchannel):
    await bot.send_message(msgchannel,"FS Usage: !?fs [grade] [Enchantment Level Trying]:")
    await bot.send_message(msgchannel,"Example: !?fs green pri")
    await bot.send_message(msgchannel,"Bot Says: Start at 9 stop at 14")
    await bot.send_message(msgchannel,"Types: flex fixed boss blueacc yellowacc")


@bot.event
async def on_message(message):
    if (message.content.startswith('!?fs')):
        print(message.author.name + " said: \"" + message.content + "\" in #" + message.channel.name + " @" + str(
            datetime.datetime.now()))

        words = to_lower(message.content).split()
        if len(words) < 3:
            await fs_error(message.channel)
        elif words[1] not in grades or failstack[grades[words[1]]] not in failstack:
            await fs_error(message.channel)
        else:
            msg = "Start at " + str(failstack[grades[words[1]]].get(words[2])- startbelow[grades[words[1]]]) + " and max chance at " + str(failstack[grades[words[1]]].get(words[2]))
            await bot.send_message(message.channel,msg)

if __name__ == '__main__':
    key = sys.argv[1]
    bot.run(key)
