import discord
import random
import os
import requests
import traceback

from discord.ext import commands
from dotenv import load_dotenv
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from requests.exceptions import RequestException

class MaxBot(commands.Bot):

    def __init__(self,command_prefix):
        super().__init__(command_prefix=command_prefix)

        # Load in Cogs
        for f in os.listdir('src/cogs'):
            file_name, file_extension = os.path.splitext(f)
            if file_extension == '.py' and not file_name.startswith('__'):
                self.load_extension(f'cogs.{file_name}')

    async def on_ready(self):
        print('Greetings, I am MaxBot')

bot = MaxBot(command_prefix='!')

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

if __name__ == '__main__':

    load_dotenv()

    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    try:
      bot.run(DISCORD_TOKEN)
    except Exception as e:
        track = traceback.format_exc()
        print('Could Not Start Bot')
        print(track)
