import ctypes.util
import os
import discord
import asyncio
import nacl
import time
from discord.ext import commands
from discord.utils import get
from gtts import gTTS
import opuslib

file = open("pass.txt")
TOKEN = file.readline()

# Set the timezone to German timezone with respect to DST
os.environ['TZ'] = "UTC-01UTC-02,M3.5.0,M10.5.0"
time.tzset()

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
    now = time.localtime()

    # Formatted Time in Germany
    nowDateTime = time.strftime("%I:%M %p on %a %b %d %Y", now)

    if ctx.message.author.voice == None:
        await ctx.send(f"It is currently {nowDateTime} in Germany")
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
                timeTTS = gTTS(f"It is currently {nowDateTime} in Germany")
                timeTTS.save("time.mp3")
                voice.play(discord.FFmpegPCMAudio("time.mp3"), after=lambda e: print("Done"))
        elif voice and voice.is_connected():
                await ctx.send("I'm already giving the time!")
        else:
                print("not playing, but in voice")

        while voice.is_playing():
                await asyncio.sleep(1)

            # leaves the channel
        if voice and voice.is_connected():
                await voice.disconnect()
        else:
                print("I was told to leave a channel but was not in one")



    #except AttributeError:
    #    await ctx.send(f"It is currently {nowDateTime} in Germany")
    #return


# Start connection with discordbot and main.py
bot.run(TOKEN)
