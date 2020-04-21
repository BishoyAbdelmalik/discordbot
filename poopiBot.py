# poopiBot.py
import discord
import threading
import asyncio
import substring
import random
import requests 
import os
import subprocess

import youtube_dl

from discord.ext import commands

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


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

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
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')


TOKEN = open("token.txt").read()
# api-endpoint 
meme = "https://meme-api.glitch.me/dank"
meme2 = "https://meme-api.glitch.me/sbubby"
meme3 = "https://meme-api.glitch.me/moderate"
client = discord.Client()
# gwhy=True
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    user=""
    if '!start 380' in message.content:
        subprocess.Popen(["sh", "/380/start.sh"], shell=False,stdin=None, stdout=None, stderr=None, close_fds=True)
        return
    if '!stop 380' in message.content:
        subprocess.Popen(["pkill", "-9" , "-f" , "server.py"], shell=False,stdin=None, stdout=None, stderr=None, close_fds=True)

        return
    if '!drive arian crazy' in message.content:
        await message.channel.send('One day I will be able to' )             
        return
    if '@' in message.content:
        user=substring.substringByChar(message.content, startChar="<", endChar=">")
    if 'gWhy' in message.content:
        # gwhy=True
        await message.channel.send('CANBAS'+" "+ user )
        # while True:
            # await message.channel.send('CANBAS')
            # await asyncio.sleep(10)
            # await asyncio.sleep(10)
            # if not gwhy:
            #     return
        return
    if 'CANBAS'.lower() in message.content.lower():
        #print("stop canbas")
        # gwhy=False
        await message.channel.send('gWhy'+" "+ user )
        return
    if 'why not' in message.content.lower():
        if bool(random.getrandbits(1)):
            await message.channel.send('Gwacause not'+" <@"+ str(message.author.id)+">")
        return
    if 'why' in message.content.lower():
        if bool(random.getrandbits(1)):
            await message.channel.send('Gwacause'+" <@"+ str(message.author.id)+">")
        return
    if '!meme' in message.content.lower():
        pick=random.randint(1,4)
        link=meme
        if pick==1:
            link=meme
        if pick==2:
            link=meme2
        if pick==3:
            link=meme3
        r = requests.get(url = link)
        # extracting data in json format 
        data = r.json() 
        await message.channel.send(data["meme"])
        return
    if '!joke' in message.content.lower():
        headers = {'Accept': 'application/json'}
        joke="https://icanhazdadjoke.com/"
        r = requests.get(url = joke, headers=headers)
        data = r.json() 
        await message.channel.send(data["joke"])
        return
    if 'success' in message.content.lower():
        if '@' in message.content:
            await message.channel.send('Perfect'+" "+ user )
        else:
            await message.channel.send('Perfect'+" <@"+ str(message.author.id)+">")
        return
    if 'perfect' in message.content.lower():
        if '@' in message.content:
            await message.channel.send('Beautiful'+" "+ user )
        else:
            await message.channel.send('Beautiful'+" <@"+ str(message.author.id)+">")
        return
    pick=random.randint(1,100)
    if pick==5:
        await message.channel.send('mmmm'+" <@"+ str(message.author.id)+">")
        return



@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, poopi welcoms you!'
    )
client.add_cog(Music(bot))
client.run(TOKEN)