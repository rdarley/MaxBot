import discord
import requests

from discord.ext import commands
from requests.exceptions import RequestException
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from db.models import Inspiration, Member
from db.interface import MaxBotDBInterface

class InspiroBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.interface = MaxBotDBInterface()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command()
    async def inspire(self, ctx, name=None):
        """Generates Inspiration using the Inspirobot API"""
        if name:
            try:
                inspo = self.interface.
                self.interface.database.add_object(session,inspo)
                session.commit()
            await ctx.send(f'Image saved as {name}')
            except Exception as e:
                await ctx.send('Could not complete your command')
                print(e)
            finally:
                session.close()
        try:
            url = 'http://inspirobot.me/api'
            params = {'generate':'true'}
            response = requests.get(url, params, timeout=10)
            image = response.text
            await ctx.send(image)
            
        except RequestException:
            await ctx.send('Inspirobot is non-responsive, there is no light in the darkness.')

    @commands.command()
    async def save_inspiration(self, ctx, name, url):
        '''Creates an event with specified name and date
            example: ?create party 12/22/2017 1:40pm
        '''
        server = ctx.guild.name
        author = ctx.message.author.name
        member_id = ctx.message.author.id

        session = self.interface.database.Session()

        try:
            member = self.interface.find_member(session,member_id)
        except Exception as e:
            # Create member if they do not exist in our database
            member = Member(id=member_id, name=author, server=server)
            self.interface.database.add_object(session,member)

        try:
            inspo = Inspiration(name=name, server=server, url=url, member_id=member_id)
            self.interface.database.add_object(session,inspo)
            session.commit()
            await ctx.send(f'Image saved as {name}')
        except Exception as e:
            await ctx.send('Could not complete your command')
            print(e)
        finally:
            session.close()

def setup(bot):
    bot.add_cog(InspiroBot(bot))