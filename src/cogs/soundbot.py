"""Base voice code leveraged from Rapptz/discord.py examples

https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
"""

import discord
import requests
import youtube_dl
import asyncio
import os

from dotenv import load_dotenv
from discord.ext import commands
from requests.exceptions import RequestException
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from db.models import Member, Sound
from db.interface import MaxBotDBInterface

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class SoundBot(commands.Cog):
    def __init__(self, bot):
        load_dotenv()

        self.bot = bot
        self.interface = MaxBotDBInterface()
        self.SOUND_DIRECTORY = os.getenv("SOUND_DIRECTORY")

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, command):
        """Plays a file associated with the command"""

        session = self.interface.database.Session()
        sound_file_path = ''
        try:
            sounds = self.interface.find_sound_by_command(session,command)[0]
            sound_file_path = f'{self.SOUND_DIRECTORY}/{sound.file_name}'
        except Exception as e:
            await ctx.send(f'Could not find saved sound with command {command}')
            print(e)
        finally:
            session.close()

        if os.path.isfile(sound_file_path):
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path))
            ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
            await ctx.send(f'Now playing: {command}')


    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @commands.command()
    async def list(self, ctx):
        """Sends the user a DM with the list of available sounds"""
        session = self.interface.database.Session()

        try:
            sounds = self.interface.get_all_items(session, Sound, "command")
        except Exception as e:
            print(e)
        finally:
            session.close()
        sound_chunks = [sounds[i:i + 100] for i in range(0,len(sounds), 100)]
        for chunk in sound_chunks:
            await ctx.message.author.send('`' + ', '.join([sound.command for sound in chunk]) + '`')

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(SoundBot(bot))            