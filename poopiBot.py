# poopiBot.py
import discord
import threading
import asyncio
import substring
import random
import requests 
import os
import subprocess

TOKEN = open("token.txt").read()
# api-endpoint 
meme = "https://meme-api.glitch.me/dank"
meme2 = "https://meme-api.glitch.me/sbubby"
meme3 = "https://meme-api.glitch.me/moderate"
client = discord.Client()
# gwhy=True
music=False
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
    if '!play' in message.content.lower():
        await message.channel.send(';;play'+" " +message.content[7:] )
        music=True
        return
    if message.author.id == 184405311681986560 and music:
        music=False
        await message.channel.send(';;play'+" 1")
        return



@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, poopi welcoms you!'
    )
client.run(TOKEN)
