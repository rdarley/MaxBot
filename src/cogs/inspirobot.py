import discord
import requests

from discord.ext import commands
from requests.exceptions import RequestException
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from db.models import Base, Inspiration, Member

class InspiroBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command()
    async def inspire(self, ctx):
        """Generates Inspiration using the Inspirobot API"""
        try:
            url = 'http://inspirobot.me/api'
            params = {'generate':'true'}
            response = requests.get(url, params, timeout=10)
            image = response.text
            await ctx.send(image)
            
        except RequestException:
            await ctx.send('Inspirobot is non-responsive, there is no light in the darkness.')

    @commands.command()
    async def save(self, ctx, name, url):
        '''Creates an event with specified name and date
            example: ?create party 12/22/2017 1:40pm
        '''
        server = ctx.guild.name
        author = ctx.message.author.name
        avatar = ctx.message.author.avatar_url
        member_id = ctx.message.author.id

        try:
            count = self.bot.session.query(Member).filter(Member.id == id).count()

            # Create member if they do not exist in our database
            if count < 1:
                member = Member(id=id, name=author, avatar=avatar)
                self.bot.session.add(member)

            inspo = Inspiration(name=name, server=server, url=url, member_id=member_id)
            self.bot.session.add(inspo)
            self.bot.session.commit()
            await ctx.send(f'Image saved as {name}')
        except Exception as e:
            await ctx.send('Could not complete your command')
            print(e)

def setup(bot):
    bot.add_cog(InspiroBot(bot))