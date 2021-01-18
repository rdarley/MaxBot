import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Greetings, I am MaxBot')

client.run('ODAwMTMyOTY3MzMwNjExMjQx.YANr5Q.ivKjqUPtWgMIiK7w0cOffVCsJCQ')