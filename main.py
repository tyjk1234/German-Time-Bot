import ctypes.util
import os
import discord
import asyncio
import nacl
import time
from discord.ext import commands
from discord.utils import get
from gtts import gTTS
from pathlib import Path
import opuslib

file = open("pass.txt")
TOKEN = file.readline()

# Set the timezone to German timezone with respect to DST
def setTimeZone():
    """
    set the timezone to German Timezone with respect to DST. If not on windows remove time.tzset() as it is not part of
    time module in windows python

    Note: UTC-01UTC-02. This seems backwards as Germany's timezone is UTC+01 normally and UTC+02 during DST. This is how
    the time module in python requires +01 and +02 to be written as in the documentation
    """
    os.environ['TZ'] = "UTC-01UTC-02,M3.5.0,M10.5.0"
    time.tzset()


async def getUTCTime():
    """
    Gets UTC/GMT time
    :return: UTC/GMT time
    """
    return time.localtime()

#
async def formatGivenTime(dateAndTime, textOrTTS = True):
    """:
    textOrTTS should be True for text or False for TTS
    """
    formattedDateAndTime = time.strftime("%I:%M %p on %a %b %d %Y", dateAndTime)
    if textOrTTS:
        return formattedDateAndTime
    else:
        return f"It is currently {formattedDateAndTime} in Germany"


async def generateTTS(message, fileName = "default"):
    """
    Generates as TTS mp3 file of given message with name of "fileName"
    :param message: any given string
    :param fileName: any given string fileName, is "default" by default
    """
    timeTTS = gTTS(message)
    timeTTS.save(f"{fileName}.mp3")


async def disconnectBot(botVoice):
    """
    Disconnect the bot if it is connected to a voice channel. If it is not it will tell you in the terminal/output file
    that it is not in a channel
    :param botVoice: discord command.Bot object
    """
    if botVoice and botVoice.is_connected():
        await botVoice.disconnect()
    else:
        print("I was told to leave a channel but was not in one")


async def pauseIfPlaying(botVoice):
    """
    Waits until bot is done playing to continue with code exicution. If this is left out bot could possibly leave before
     playing any audio
    :param botVoice: discord command.Bot object
    """
    while botVoice.is_playing():
        await asyncio.sleep(1)


async def playMp3(botVoice,fileName = "default"):
    """
    PLays given fileName through
    :param botVoice: discord command.Bot object
    :param fileName: any given string fileName, is "default" by default
    """
    fileNameMP3 = f"{fileName}.mp3"
    if Path(fileNameMP3).is_file():
        botVoice.play(discord.FFmpegPCMAudio(fileNameMP3), after=lambda e: print("Done"))
    else:
        print("This file does not exist. :(")


setTimeZone()



# Duh
bot = commands.Bot(command_prefix="$")




# Let you know when the discord bot is online and ready to work
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user} bot")

# Allows for message handeling
@bot.command(pass_context=True, aliases=["germ", "g"])
async def germany(ctx):
    # Time in Germany
    now = getUTCTime()

    # Formatted Time in Germany
    nowDateTimeText = formatGivenTime(now,textOrTTS = True)
    nowDateTimeTTS = formatGivenTime(now, textOrTTS=False)
    fileName = "time"


    if ctx.message.author.voice == None:
        await ctx.send(f"It is currently {nowDateTimeText} in Germany")
    else:
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)

        # joins the channel
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        # is the bot already in the channel playing music?
        if not voice.is_playing():
            await generateTTS(nowDateTimeTTS,fileName)
            await playMp3(voice,fileName)
        elif voice and voice.is_connected():
            await ctx.send("I'm already giving the time!")
        else:
            print("not playing, but in voice")

        await pauseIfPlaying(voice)

        # leaves the channel
        await disconnectBot(voice)



    #except AttributeError:
    #    await ctx.send(f"It is currently {nowDateTime} in Germany")
    #return


# Start connection with discordbot and main.py
bot.run(TOKEN)
