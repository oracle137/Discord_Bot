import asyncio
import sys
import discord
from discord.ext import commands
import datetime
import webscrapper
import pickle


bot = commands.Bot(command_prefix='!?', description='Ghosts Bot')

grades = {"flex":0,"fixed":1,"blue":2,"boss":3,"blueacc":4,"yellowacc":5}
flex = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":5,"11":5,"12":5,"13":10,"14":0,"15":10}
fixed = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":4,"10":7,"11":7,"12":7,"13":10,"14":10,"15":15,"pri":11,"duo":20,"tri":28,"tet":40,"pen":65}
blue = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":3,"9":6,"10":9,"11":10,"12":10,"13":15,"14":15,"15":20,"pri":15,"duo":20,"tri":30,"tet":45,"pen":70}
boss = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":5,"9":8,"10":11,"11":15,"12":15,"13":20,"14":20,"15":20,"pri":20,"duo":24,"tri":33,"tet":50,"pen":100}
blueacc = {"pri":15,"duo":28,"tri":35,"tet":45,"pen":70}
yellowacc = {"pri":20,"duo":35,"tri":45,"tet":60,"pen":100}
startbelow = [0,5,3,3,4,0]

failstack = [flex,fixed,blue,boss,blueacc,yellowacc]


def to_lower(argument):
    return argument.lower()


async def my_background_task():
    await bot.wait_until_ready()
    counter = 0
    while not bot.is_closed:
        counter += 1
        print("Refreshing boss status channel", counter, datetime.datetime.now())
        channels = bot.get_all_channels()
        for channel in channels:
            if channel.name == "boss-status":
                await boss_status_update(channel)
        await asyncio.sleep(60) # task runs every 60 seconds


async def boss_status_update(boss_channel):
    bosses = webscrapper.start()
    inwindowmsg = ""
    msg = ""
    for key, value in bosses.items():

        name = key.replace(" (World Boss)", '')
        name = name.replace(" (Field Boss)", '')
        name = name.replace(" aka Bastard Bheg", '')
        if value.in_window == True:
            inwindowmsg += "%-20s %-50s\n" % (name, " | In Window: " + "%s:%s" % (value.dt_first.hour,value.dt_first.minute) + " - " +
                "%s:%s" % (value.dt_last.hour, value.dt_last.minute))
        else:
            msg += "%-20s %-50s\n" % (name, " | Time to Window: " + str(value.time_to_window))
    try:
        async for m in bot.logs_from(boss_channel):
            try:

                await bot.delete_message(m)
            except:
                pass
        await bot.send_message(boss_channel, content="```" + inwindowmsg + msg + "```")
    except:
        pass


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)


@bot.command()
async def hello():
    await bot.say('Hello!')



@bot.command()
async def fs(ctx,arg: to_lower):
    words = arg.split()
    msg = "Start at " + str(failstack[grades[words[0]]].get(words[1])- startbelow[grades[words[0]]]) + " and max chance at " + str(failstack[grades[words[0]]].get(words[1]))
    await bot.say(msg)


@fs.error
async def error(error,ctx):
    if type(error) == discord.ext.commands.errors.MissingRequiredArgument:
        await bot.say("FS Usage: !?fs [grade] [Enchantment Level Trying]:")
        await bot.say("Example: !?fs green pri")
        await bot.say("Bot Says: Start at 9 stop at 14")


if __name__ == '__main__':
    key = sys.argv[1]
    bot.loop.create_task(my_background_task())
    bot.run(key)
