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
        """Generates Inspiration using the Inspirobot API or loads in an existing inspiration from the database.
        """
        if name:
            session = self.interface.database.Session()
            try:
                inspirations = self.interface.find_items_by_name(session,name,item_type=Inspiration)
                if len(inspirations) > 1:
                    await ctx.send(f'Multiple inspirations found, please be more specific')
                    raise Exception()
                inspo = inspirations[0]
                await ctx.send(f'Loaded saved inspiration: {inspo.name}')
                await ctx.send(inspo.url)
            except Exception as e:
                await ctx.send(f'Could not load saved inspiration with keyword {name}')
                print(e)
            finally:
                session.close()
        else:
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
        '''Stores an inspiration for later retrieval.
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

    @commands.command()
    async def delete_inspiration(self, ctx, name):
        '''Delete an inspiration from the database.
        '''
        author = ctx.message.author
        member_id = ctx.message.author.id

        session = self.interface.database.Session()

        try:
            if author.guild_permissions.administrator:
                inspos = self.interface.find_items_by_name(session, name=name, item_type=Inspiration, exact_match=True)
                if len(inspos) > 1:
                    raise('Need to make Name Unique')
                self.interface.delete_item_by_id(session,id=inspos[0].id,item_type=Inspiration)
                await ctx.send(f'Inspiration with name {name} successfully deleted')
            else:
                inspos = self.interface.find_items_by_member(session,member_id,item_type=Inspiration,sort=Inspiration.id)
                for inspo in inspos:
                    if inspo.name == name:
                        self.interface.delete_item_by_id(session,id=inspo.id,item_type=Inspiration)
                        session.commit()
                        await ctx.send(f'Inspiration with name {name} successfully deleted')
        except Exception as e:
            await ctx.send('Could not complete command')
            print(e)
        finally:
            session.close()

def setup(bot):
    bot.add_cog(InspiroBot(bot))