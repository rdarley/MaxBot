import discord
import random
import os
import requests

from discord.ext import commands
from dotenv import load_dotenv
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, Inspiration, Member
from datetime import datetime
from requests.exceptions import RequestException

engine = create_engine('sqlite:///maxbot.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# If table doesn't exist, Create the database
if not engine.dialect.has_table(engine, 'member'):
    Base.metadata.create_all(engine)

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

@bot.command()
async def inspire(ctx):
    """Generates Inspiration using the Inspirobot API"""
    try:
        url = 'http://inspirobot.me/api'
        params = {'generate':'true'}
        response = requests.get(url, params, timeout=10)
        image = response.text
        await ctx.send(image)
        
    except RequestException:
        await ctx.send('Inspirobot is non-responsive, there is no light in the darkness.')

@bot.command()
async def save(ctx, name, url):
    '''Creates an event with specified name and date
        example: ?create party 12/22/2017 1:40pm
    '''
    server = ctx.guild.name
    author = ctx.message.author.name
    member_id = ctx.message.author.id

    try:
        count = session.query(Member).filter(Member.id == member_id).count()

        # Create member if they do not exist in our database
        if count < 1:
            member = Member(id=member_id, name=author)
            session.add(member)

        inspo = Inspiration(name=name, server=server, url=url, member_id=member_id)
        session.add(inspo)
        session.commit()
        await ctx.send(f'Image saved as {name}')
    except Exception as e:
        await ctx.send('Could not complete your command')
        print(e)

# for f in os.listdir('./cogs'):
#     file_name, file_extension = os.path.splitext(f)
#     if file_extension == '.py':
#         bot.load_extension(f'cogs.{file_name}')

if __name__ == '__main__':
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        print('Could Not Start Bot')
        print(e)
    finally:
        print('Closing Session')
        session.close()