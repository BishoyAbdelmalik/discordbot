# poopiBot.py
import discord
import threading
import asyncio
from discord import channel
import substring
import random
import requests
import os
import subprocess
from discord.ext import commands
import aiohttp
from io import BytesIO
from requests.sessions import session
import youtube_dl
import validators
from collections import deque
from util import get_yt_url, get_url
from constants import emojiThumbsUp,meme,meme2,meme3,meme4,meme5,meme6
from tutoring import tutoring_server
os.chdir(os.path.realpath(__file__)[:-len(os.path.basename(__file__))])

TOKEN = open("token.txt").read()

print(os.system("node /bot/memeAPI/server.js &"))
servers = {}
# client = discord.Client()


def endSong(guild: str, path: str):
    if not servers[guild]["voice_client"].is_connected():
        servers[guild] = {}
    else:
        servers[guild]["song_count"][path] = servers[guild]["song_count"][path]-1
        if servers[guild]["song_count"][path] == 0:
            os.remove(path)
            servers[guild]["song_count"].pop(path)

        if len(servers[guild]["music_queue"]) != 0:
            playMusic(guild)


def download_song(v_id: str):
    os.system(f'yt-dlp --extract-audio -o \'%(id)s.mp3\' --audio-format mp3 {get_yt_url(v_id)}')
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download([get_yt_url(v_id)])


def playMusic(guild: str):
    if servers[guild]["voice_client"].is_playing():
        return
    if len(servers[guild]["music_queue"]) != 0:
        path = servers[guild]["music_queue"].pop()
        servers[guild]["current_playing"] = path[:-4]
        download_song(path[:-4])
        servers[guild]["voice_client"].play(discord.FFmpegPCMAudio(
            path), after=lambda x: endSong(guild, path))
        servers[guild]["voice_client"].source = discord.PCMVolumeTransformer(
            servers[guild]["voice_client"].source, 1)
        if len(servers[guild]["music_queue"]) != 0:
            download_song(servers[guild]["music_queue"][0][:-4])

class MyClient(discord.Client):
    async def music_skip(self, message):
        global servers

        guild = message.guild
        if len(servers[guild]["music_queue"]) == 0:
            await message.channel.send("No more files in queue")
        servers[guild]["voice_client"].stop()
        return

    async def music_now_playing(self, message):
        global servers
        guild = message.guild

        if not servers[guild]["voice_client"].is_playing():
            await message.channel.send("Nothing is playing")
        else:
            await message.channel.send(get_yt_url(servers[guild]["current_playing"]))
        return

    async def music_player(self, message, location):
        if not message.author.voice:
            await message.channel.send("join vc first")

        else:
            global servers
            guild = message.guild

            channel = message.author.voice.channel
            if not guild in servers:
                servers[guild] = {}
            if not "music_queue" in servers[guild]:
                music_queue = deque()
                servers[guild]["music_queue"] = music_queue

            try:
                servers[guild]["voice_client"] = await channel.connect()
            except:
                print("already in vc add music")
                if(servers[guild]["voice_client"] == None):
                    await message.channel.send("error")
                    return

            msg = message.content
            for attachment in message.attachments:
                m3u_url = attachment.url
                print(m3u_url)
                if m3u_url.endswith(".m3u") or m3u_url.endswith(".txt"):
                    response = requests.get(m3u_url)
                    links = response.text.split()
                    print(links)
                    for link in links:
                        if validators.url(link):
                            msg += " " + link
            possible_urls = msg.split()[1:]
            a_url = ""
            urls = []
            for url in possible_urls:
                if validators.url(url):
                    if len(a_url.strip()) > 0:
                        urls.append(get_url(a_url.strip()))
                        a_url = ""
                    urls.append(get_url(url))
                else:
                    a_url += " "+url
            if len(a_url.strip()) > 0:
                urls.append(get_url(a_url.strip()))
                a_url = ""

            print(urls)
            for url in urls:
                print(url)
                path = url[url.index("v=")+2:] + ".mp3"
                if location == 0:
                    servers[guild]["music_queue"].appendleft(path)
                else:
                    servers[guild]["music_queue"].append(path)
                if not "song_count" in servers[guild]:
                    servers[guild]["song_count"] = {}
                if not path in servers[guild]["song_count"]:
                    servers[guild]["song_count"][path] = 0
                servers[guild]["song_count"][path] = servers[guild]["song_count"][path]+1
                if len(urls) < 2:
                    await message.channel.send(url+"\nAdded to the queue")

            if len(urls) > 1:
                await message.channel.send(str(len(urls))+" songs added to the queue")
            playMusic(guild)
            await message.delete()
        return

    async def music_play(self, message):
        await self.music_player(message, 0)

    async def music_play_top(self, message):
        await self.music_player(message, 1)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print('Servers connected to:')
        for server in client.guilds:
            print(server)

    async def on_member_join(self, member):
        print("hello "+member)
        if str(member.guild) == "CS/CIT Tutoring":
            await self.add_student_role(member)

        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, poopi welcomes you!'
        )
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        user = ""
        isAdmin = message.channel.permissions_for(message.author).administrator
        print(message.guild)
        print(message.content)
        msgs = ["aha", "sure", "why not", "why", "mmm why", "tell me more", "yeah", "I see",
                "I guess", "IDK", "lamo", "lol", "ok boomer", "good point", "no", "yes", "Awwww"]
        if message.guild == None:
            await message.channel.send(random.choice(msgs))
        if message.guild.id != 690308124808183859:
            if str(message.guild) == "CS/CIT Tutoring":
                await tutoring_server(message)
                return
            if '!setPin' in message.content:
                if isAdmin:
                    try:
                        f = open(str(message.guild.id)+"_Pins", "x")
                        f.write(str(message.channel.id))
                        f.close()
                        await message.add_reaction(emojiThumbsUp)
                    except:
                        await message.channel.send("unset pin channel first")
                else:
                    await message.channel.send("Only admins can set pins channel")

                return
            if '!unsetPin' in message.content:
                if isAdmin:
                    try:
                        os.remove(str(message.guild.id)+"_Pins")
                    except:
                        print()
                else:
                    await message.channel.send("Only admins can unset pins channel")
                return
            try:
                if message.channel.id == int(open(str(message.guild.id)+"_Pins").read()):
                    await message.delete()
                    user = message.author
                    await user.create_dm()
                    await user.dm_channel.send("Hey, don't send messages in pins channel 😡 😡 😡")
                    return
            except:
                print("no pins channel")
            pick = random.randint(1, 100)
            if pick == 5:
                await message.channel.send('mmmm'+" <@" + str(message.author.id)+">")
            if '!pin' in message.content.lower():
                # print(open(str(message.guild)+"_Pins").read())
                try:
                    channelID = int(open(str(message.guild.id)+"_Pins").read())
                except:
                    channelID = -1
                if channelID == -1:
                    await message.channel.send("set pin channel first")
                else:
                    pinChannel = client.get_channel(channelID)
                    await pinChannel.send(message.content.replace('!pin', '').strip()+"\n\nPinned by"+" <@" + str(message.author.id)+">")
                    await message.channel.send('Pinned ```'+message.content.replace('!pin', '').strip()+'```')
                    await message.delete()
                return
            if '!!pt' in message.content.lower():
                await self.music_play_top(message)
                return
            if '!!p' in message.content.lower():
                await self.music_play(message)
                return
            if '!!skip' in message.content.lower() or '!!s' in message.content.lower():
                await self.music_skip(message)
                return
            if '!!np' in message.content.lower():
                await self.music_now_playing(message)
                return
            if '!bugs' in message.content.lower():
                await message.channel.send("https://media.discordapp.net/attachments/538955632951296010/771989679713157140/db1.png")
                return
            if message.mention_everyone:
                await message.channel.send('mmmm maybe'+" <@" + str(message.author.id)+">")
                return
            if '!start 380' in message.content:
                subprocess.Popen(["sh", "/380/server/start.sh"], shell=False,
                                 stdin=None, stdout=None, stderr=None, close_fds=True)
                return
            if '!stop 380' in message.content:
                subprocess.Popen(["pkill", "-9", "-f", "server.py"], shell=False,
                                 stdin=None, stdout=None, stderr=None, close_fds=True)

                return
            if '@' in message.content:
                user = substring.substringByChar(
                    message.content, startChar="<", endChar=">")
            if 'gWhy' in message.content:
                await message.channel.send('CANBAS'+" " + user)
                return
            if 'CANBAS'.lower() in message.content.lower():
                await message.channel.send('gWhy'+" " + user)
                return
            if 'why not' in message.content.lower():
                if bool(random.getrandbits(1)):
                    await message.channel.send('Gwacause not'+" <@" + str(message.author.id)+">")
                return
            if 'why' in message.content.lower():
                if bool(random.getrandbits(1)):
                    await message.channel.send('Gwacause'+" <@" + str(message.author.id)+">")
                return
            if 'user' in message.content.lower():
                if bool(random.getrandbits(1)):
                    await message.channel.send('Jyuicerr'+" <@" + str(message.author.id)+">")
                return
            if '!pathetic' in message.content.lower():
                pathetic_arr = ["https://media.discordapp.net/attachments/699127599817031700/724169633262862356/pathetic-56074431.png",
                                "https://media.discordapp.net/attachments/699127599817031700/724168345154224140/unknown.png",
                                "https://media.discordapp.net/attachments/699127599817031700/724168083782238208/aexeoj2Y_700w_0.png",
                                "https://media.discordapp.net/attachments/699127599817031700/724168065666908190/D-WdtJ9UwAAGkY3.png",
                                "https://media.discordapp.net/attachments/699127599817031700/724161695487885322/447.png",
                                "https://media.discordapp.net/attachments/699127599817031700/724711838813651014/unknown.png",
                                "https://media.discordapp.net/attachments/699127599817031700/724713507039215646/pathetic.jpeg",
                                "https://cdn.discordapp.com/attachments/678381326533132324/739654715268137071/unknown_3.png"]
                check = random.randint(0, 1)  # whatever percentage
                if not check:
                    query = "pathetic meme"

                    r = requests.get("https://api.qwant.com/api/search/images",
                                     params={
                                         'count': 50,
                                         'q': query,
                                         't': 'images',
                                         'locale': 'en_US',
                                         'uiv': 4
                                     },
                                     headers={
                                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
                                     }
                                     )

                    response = r.json().get('data').get('result').get('items')
                    urls = [r.get('media') for r in response]
                    url = random.choice(urls)
                else:
                    check = random.randint(0, 1)
                    if not check:
                        url = pathetic_arr[7]
                    else:
                        url = random.choice(pathetic_arr)

                response = requests.get(url, stream=True)
                # filename=data["meme"][data["meme"].index("m/")+2:]
                # print(filename[filename.index("."):])
                header = response.headers
                print(header)
                if int(response.headers["Content-Length"]) < 8000000:
                    # extenstion=filename[filename.index("."):]
                    extenstion = "."+header["Content-Type"].split("/")[1]
                    filename = "pathetic"+extenstion
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    await message.channel.send(file=discord.File(filename))
                    os.remove(filename)
                else:
                    await message.channel.send(pathetic_arr[pick])
                return
            if '!meme' in message.content.lower():
                pick = random.randint(1, 7)
                link = meme
                if pick == 1:
                    link = meme
                if pick == 2:
                    link = meme2
                if pick == 3:
                    link = meme3
                if pick == 4:
                    link = meme4
                if pick == 5:
                    link = meme5
                if pick == 6:
                    link = meme6
                r = requests.get(url=link)
                # extracting data in json format
                data = r.json()
                response = requests.get(data["meme"], stream=True)
                filename = data["meme"][data["meme"].index("m/")+2:]
                # print(filename[filename.index("."):])
                print(response.headers)
                if int(response.headers["Content-Length"]) < 8000000:
                    extenstion = filename[filename.index("."):]
                    filename = "meme"+extenstion
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    await message.channel.send(file=discord.File(filename))
                    os.remove(filename)
                else:
                    await message.channel.send(data["meme"])
                return
            if '!joke' in message.content.lower():
                headers = {'Accept': 'application/json'}
                joke = "https://icanhazdadjoke.com/"
                r = requests.get(url=joke, headers=headers)
                data = r.json()
                await message.channel.send(data["joke"])
                return
            if '!potato' in message.content.lower():
                pick = random.randint(1, 7)
                link = "http://localhost:956/potato"
                r = requests.get(url=link)
                # extracting data in json format
                data = r.json()
                response = requests.get(data["meme"], stream=True)
                filename = data["meme"][data["meme"].index("m/")+2:]
                # print(filename[filename.index("."):])
                print(response.headers)
                if int(response.headers["Content-Length"]) < 8000000:
                    extenstion = filename[filename.index("."):]
                    filename = "potato"+extenstion
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    await message.channel.send(file=discord.File(filename))
                    os.remove(filename)
                else:
                    await message.channel.send(data["meme"])
                return
            if 'success' in message.content.lower():
                if '@' in message.content:
                    await message.channel.send('Perfect'+" " + user)
                else:
                    await message.channel.send('Perfect'+" <@" + str(message.author.id)+">")
                return
            if 'perfect' in message.content.lower():
                if '@' in message.content:
                    await message.channel.send('Beautiful'+" " + user)
                else:
                    await message.channel.send('Beautiful'+" <@" + str(message.author.id)+">")
                return
            if '!ping' in message.content.lower():
                await message.channel.send(client.latency)
        elif message.guild.id == 690308124808183859:  # republic city
            if '!bugs' in message.content.lower():
                await message.channel.send("https://media.discordapp.net/attachments/538955632951296010/771989679713157140/db1.png")
                return
        # for all servers poopie is in
        if message.content.lower().startswith('@vc') and not message.mentions:
            voice = message.author.voice
            if voice and message.content.lower().startswith('@vcs'):
                await message.channel.send(', '.join(f"<@!{u}>" for u in voice.channel.voice_states.keys()))
                return
            elif voice and message.content.lower().startswith('@vc'):
                await message.channel.send(', '.join(f"<@!{u}>" for u in voice.channel.voice_states.keys()), delete_after=5)
                return


client = MyClient()


client.run(TOKEN)
