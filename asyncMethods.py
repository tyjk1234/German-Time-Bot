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


async def getUTCTime():
    """
    Gets UTC/GMT time
    :return: UTC/GMT time
    """
    return time.localtime()


async def formatGivenTime(dateAndTime, textOrTTS = True):
    """:
    textOrTTS should be True for text or False for TTS
    """
    formattedDateAndTime = time.strftime("%I:%M %p", dateAndTime)
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
