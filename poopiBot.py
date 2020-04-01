# poopiBot.py
import discord
import threading
import asyncio
import substring

TOKEN = open("token.txt").read()

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
        await message.channel.send('Gwacause not'+" <@"+ str(message.author.id)+">")
        return
    if 'why' in message.content.lower():
        await message.channel.send('Gwacause'+" <@"+ str(message.author.id)+">")
        return
  
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, poopi welcoms you!'
    )
client.run(TOKEN)