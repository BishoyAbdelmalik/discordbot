import discord
from util import is_url_image
from constants import emojiThumbsUp

async def add_110_role(member):
    role = discord.utils.get(member.guild.roles, id=809577623126409240)
    print(role)
    await member.add_roles(role)

async def add_182_role(member):
    role = discord.utils.get(member.guild.roles, id=809577657398198322)
    print(role)
    await member.add_roles(role)

async def add_122_role(member):
    role = discord.utils.get(member.guild.roles, id=809577695586549793)
    print(role)
    await member.add_roles(role)

async def add_282_role(member):
    role = discord.utils.get(member.guild.roles, id=809577733020581898)
    print(role)
    await member.add_roles(role)

async def add_160_role(member):
    role = discord.utils.get(member.guild.roles, id=809577851292090368)
    print(role)
    await member.add_roles(role)
async def add_student_role(member):
    role = discord.utils.get(member.guild.roles, id=805898946434170900)
    print(role)
    await member.add_roles(role)
async def add_108_role(member):
    role = discord.utils.get(member.guild.roles, id=809577813354872883)
    print(role)
    await member.add_roles(role)

async def tutoring_server(message):
    await add_student_role(message.author)
    themsg = message.content.lower()
    if "tutor" in themsg and ("today" in themsg or "right now" in themsg or "now" in themsg or "online" in themsg) and "?" in themsg:
        with open(str(message.guild.id)+"_Schedule", "r") as content_file:
            link = content_file.read()
            await message.channel.send(str(link))
    if themsg.startswith("-join"):
        join = int(message.content[5:])
        if join == 110:
            await add_110_role(message.author)
            await message.add_reaction(emojiThumbsUp)
        elif join == 108:
            await add_108_role(message.author)
            await message.add_reaction(emojiThumbsUp)
        elif join == 182:
            await add_182_role(message.author)
            await message.add_reaction(emojiThumbsUp)
        elif join == 282:
            await add_282_role(message.author)
            await message.add_reaction(emojiThumbsUp)
        elif join == 160:
            await add_160_role(message.author)
            await message.add_reaction(emojiThumbsUp)
        elif join == 122:
            await add_122_role(message.author)
            await message.add_reaction(emojiThumbsUp)
    if themsg.startswith("-setschedule"):
        urls = themsg.split()
        print(urls[1])
        if is_url_image(urls[1]):
            try:
                f = open(str(message.guild.id)+"_Schedule", "w")
                f.write(str(urls[1]))
                f.close()
                await message.add_reaction(emojiThumbsUp)
            except:
                await message.channel.send("unable to save link")
        else:
            print('error')
            await message.channel.send("Error")