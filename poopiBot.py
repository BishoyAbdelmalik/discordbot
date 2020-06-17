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
import aiohttp
from io import BytesIO
from requests.sessions import session

TOKEN = open("token.txt").read()
# api-endpoint 
meme = "http://localhost:956/moderate"
meme2 = "http://localhost:956/sbubby"
meme3 = "http://localhost:956/dank"
meme4 = "http://localhost:956/light"
meme5 = "http://localhost:956/hmm"
meme6 = "http://localhost:956/meme"
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
        for server in client.guilds:
            print(server)

    async def on_message(self,message):
        if message.author == self.user:
            return
        user=""
        print(message.content)
        if str(message.channel) == "pins":
            await message.delete()
            user = message.author
            await user.create_dm()
            await user.dm_channel.send("Hey, don't send messages in pins channel 😡 😡 😡")
            return

        pick=random.randint(1,100)
        if pick==5:
            await message.channel.send('mmmm'+" <@"+ str(message.author.id)+">")
        
        if message.mention_everyone:
            await message.channel.send('mmmm maybe'+" <@"+ str(message.author.id)+">")
            return
        if '!start 380' in message.content:
            subprocess.Popen(["sh", "/380/server/start.sh"], shell=False,stdin=None, stdout=None, stderr=None, close_fds=True)
            return
        if '!stop 380' in message.content:
            subprocess.Popen(["pkill", "-9" , "-f" , "server.py"], shell=False,stdin=None, stdout=None, stderr=None, close_fds=True)

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
            pick=random.randint(1,7)
            link=meme
            if pick==1:
                link=meme
            if pick==2:
                link=meme2
            if pick==3:
                link=meme3
            if pick==4:
                link=meme4
            if pick==5:
                link=meme5
            if pick==6:
                link=meme6
            r = requests.get(url = link)
            # extracting data in json format 
            data = r.json() 
            response = requests.get(data["meme"], stream=True)
            filename=data["meme"][data["meme"].index("m/")+2:]
            #print(filename[filename.index("."):])
            print(response.headers)
            if  int(response.headers["Content-Length"])<8000000:
                extenstion=filename[filename.index("."):]
                filename="meme"+extenstion
                with open(filename, 'wb') as f:
                    f.write(response.content)
                await message.channel.send(file=discord.File(filename))
                os.remove(filename)
            else:
                await message.channel.send(data["meme"])
            return
        if '!joke' in message.content.lower():
            headers = {'Accept': 'application/json'}
            joke="https://icanhazdadjoke.com/"
            r = requests.get(url = joke, headers=headers)
            data = r.json() 
            await message.channel.send(data["joke"])
            return
        if '!potato' in message.content.lower():
            pick=random.randint(1,7)
            link="http://localhost:956/potato"
            r = requests.get(url = link)
            # extracting data in json format 
            data = r.json() 
            response = requests.get(data["meme"], stream=True)
            filename=data["meme"][data["meme"].index("m/")+2:]
            #print(filename[filename.index("."):])
            print(response.headers)
            if  int(response.headers["Content-Length"])<8000000:
                extenstion=filename[filename.index("."):]
                filename="potato"+extenstion
                with open(filename, 'wb') as f:
                    f.write(response.content)
                await message.channel.send(file=discord.File(filename))
                os.remove(filename)
            else:
                await message.channel.send(data["meme"])
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



client.run(TOKEN)
