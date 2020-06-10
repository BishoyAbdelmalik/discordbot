# poopiBot.py
import discord
import threading
import asyncio
import substring
import random
import requests 
import os
import subprocess
from discord.ext import commands

TOKEN = open("token.txt").read()
# api-endpoint 
meme = "http://localhost:956/dank"
meme2 = "http://localhost:956/sbubby"
meme3 = "http://localhost:956/moderate"
print(os.system("node /bot/memeAPI/server.js &"))
# client = discord.Client()
class MyClient(discord.Client):
    async def addThumbUpReact(self,message):
        emoji = '\N{THUMBS UP SIGN}'
        await message.add_reaction(emoji)
        return
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print('Servers connected to:')
        for channel in client.guilds:
            print(channel)

    async def on_message(self,message):
        if message.author == self.user:
            return
        user=""
        print(message.content)
        if '!start 380' in message.content:
            subprocess.Popen(["sh", "/380/server/start.sh"], shell=False,stdin=None, stdout=None, stderr=None, close_fds=True)
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
            await message.channel.send('CANBAS'+" "+ user )
            return
        if 'CANBAS'.lower() in message.content.lower():
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
        if '!pin' in message.content.lower():
            #print(message)
            pinChannel=client.get_channel(702270613766537328)
            await pinChannel.send(message.content.replace('!pin', '').strip()+"\n\nPinned by"+" <@"+ str(message.author.id)+">")
            await message.channel.send('Pinned ```'+message.content.replace('!pin', '').strip()+'```')
            await message.delete()
            return
        if '!ping' in message.content.lower():
            await message.channel.send(client.latency)
    async def on_member_join(self,member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, poopi welcomes you!'
        )
    

client = MyClient()
# client = commands.Bot(command_prefix='!')

# @client.command()
# async def ping(ctx):
#     await ctx.send('Pong! {0}'.format(round(client.latency, 1)))


client.run(TOKEN)
