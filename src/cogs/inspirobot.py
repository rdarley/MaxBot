import discord
import requests

from discord.ext import commands
from requests.exceptions import RequestException

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

def setup(bot):
    bot.add_cog(InspiroBot(bot))