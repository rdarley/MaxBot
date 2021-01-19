import discord
import random
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Greetings, I am MaxBot')

@bot.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(bot.latency*1000)}')

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses=['It is certain.',
               'It is decidedly so.',
               'Without a doubt.',
               'Yes – definitely.',
               'You may rely on it.',
               'As I see it, yes.',
               'Most likely.',
               'Outlook good.',
               'Yes.',
               'Signs point to yes.',
               'Reply hazy, try again.',
               'Ask again later.',
               'Better not tell you now.',
               'Cannot predict now.',
               'Concentrate and ask again.',
               "Dont count on it.",
               'My reply is no.',
               'My sources say no.',
               'Outlook not so good.',
               'Very doubtful.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

for f in os.listdir('./cogs'):
    file_name, file_extension = os.path.splitext(f)
    if file_extension == '.py':
        bot.load_extension(f'cogs.{file_name}')

bot.run(DISCORD_TOKEN)