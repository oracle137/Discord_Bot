import asyncio
import sys
import discord
from discord.ext import commands
import datetime
import webscrapper
import pickle

bot = discord.Client()



async def my_background_task():
    while True:
        print("Refreshing boss status channel", datetime.datetime.now())
        channels = bot.get_all_channels()
        for channel in channels:
            if channel.name == "boss-status":
                await boss_status_update(channel)
                print("Refresh Done")
        await asyncio.sleep(60)

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
    await my_background_task()



def start(key):
    bot.run(key)


key = None

if __name__ == '__main__':
    key = sys.argv[1]
    start(key)

