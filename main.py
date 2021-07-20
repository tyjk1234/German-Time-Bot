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

# Get the secret token :O
file = open("pass.txt")
TOKEN = file.readline()

# Duh
setTimeZone()
bot = commands.Bot(command_prefix="$")


# Let you know when the discord bot is online and ready to work
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user} bot")


# Allows for $germany command handling
@bot.command(pass_context=True, aliases=["germ","g","G","GERMANY","GERM"])
async def germany(ctx):
    # Time in Germany
    now = await getUTCTime()

    # Formatted Time in Germany
    nowDateTimeText = await formatGivenTime(now, textOrTTS = True)
    nowDateTimeTTS = await formatGivenTime(now, textOrTTS=False)
    fileName = "time"

    # Is the user not in a voice channel?
    if ctx.message.author.voice == None:
        # Send the time in text
        await ctx.send(f"It is currently {nowDateTimeText} in Germany")
    else:
        # Send the time in TTS
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild=ctx.guild)
        # Is the bot active and is it in a channel?
        if voice and voice.is_connected():
            # Move to ctx channel
            await voice.move_to(channel)
        else:
            # Connect to ctx channel
            voice = await channel.connect()

        # Is the bot not playing anything?
        if not voice.is_playing():
            # Generate TTS and play it
            await generateTTS(nowDateTimeTTS,fileName)
            await playMp3(voice,fileName)
        # Bot is already playing something
        elif voice and voice.is_connected():
            await ctx.send("I'm already giving the time!")
        # Bot isn't playing anything, but they are in the channel, shouldn't happen
        else:
            print("not playing, but in voice")

        # Make sure the whole audio file is played
        await pauseIfPlaying(voice)

        # Leaves the channel
        await disconnectBot(voice)


# Start connection with discordbot and main.py
bot.run(TOKEN)
