import discord
import requests

from discord.ext import commands
from requests.exceptions import RequestException
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from db.models import Inspiration, Member
from db.interface import MaxBotDBInterface

class SoundBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.interface = MaxBotDBInterface()