import ctypes.util
import os
import discord
import asyncio
import nacl
import time
import opuslib
from methods import setTimeZone
from asyncMethods import getUTCTime, formatGivenTime, generateTTS
from asyncMethods import disconnectBot, pauseIfPlaying, playMp3
from discord.ext import commands
from discord.utils import get
from gtts import gTTS
from pathlib import Path


file = open("pass2.txt")
TOKEN = file.readline()

# Duh
setTimeZone()
bot = commands.Bot(command_prefix="$")


# Let you know when the discord bot is online and ready to work
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user} bot")


# Allows for message handeling
@bot.command(pass_context=True, aliases=["germ", "g","G","GERMANY","GERM"])
async def germany(ctx):
    # Time in Germany
    now = await getUTCTime()

    # Formatted Time in Germany
    nowDateTimeText = await formatGivenTime(now,textOrTTS = True)
    nowDateTimeTTS = await formatGivenTime(now, textOrTTS=False)
    fileName = "time"

    if ctx.message.author.voice == None:
        await ctx.send(f"It is currently {nowDateTimeText} in Germany")
    else:
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)
        voice.Activity(type = "Time in Germany", name = nowDateTimeText)
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


# Start connection with discordbot and main.py
bot.run(TOKEN)
