import discord
from discord.ext import commands
import logging
import random
import asyncio
import os

#client = discord.Client()
#bot = commands.Bot(command_prefix='$')
client = commands.Bot(command_prefix='==')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def hello(ctx):
    hellos = ['Hello', 'Sup', "Don't talk to me", 'Hi', 'Bonjour', 'Holla', 'Guten Tag', 'Anand']
    await ctx.channel.send(hellos[random.randint(0, int(len(hellos) - 1))])

@client.command()
async def say(ctx,arg):
    await ctx.channel.send(arg)

@commands.cooldown(1, 30, commands.BucketType.user)
@client.command()
async def vibe(ctx):
    score = random.randint(0,100)
    if ctx.message.author == 'FruityBooty#3514':
        score = score//5
    result = str(ctx.message.author) + '\n'
    if score == 0:
        result += f":scream: : {score}\n I'M CALLING THE FUCKING VIBE POLICE!"
    elif score <= 20:
        result += f':nauseated_face: : {score}\n Your vibe is way the fuck off. Leave.'
    elif score <= 40:
        result += f':face_vomiting: : {score}\n Your vibe is off my guy.'
    elif score <= 50:
        result += f":slight_frown: : {score}\n Your vibe ain't it chief."
    elif score <= 60:
        result += f':smiley: : {score}\n Your vibe is big chillin. Stay safe.'
    elif score <= 80:
        result += f':sunglasses: : {score}\n Vibe Pogger!'
    elif score <= 99:
        result += f":innocent: : {score}\n That's a vibe and a half my guy Mashallah"
    elif score == 100:
        result += f':heart_eyes: : {score}\n 6 FREQUNCIES, BUNCH OF FUCKING VIBES DOG CAM CAT CAM'
    await ctx.channel.send(result)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'Get off my dick for like: {:.2f}s'.format(error.retry_after)
        await ctx.channel.send(msg)
    else:
        raise error

@client.command()
async def ping(ctx):
    await ctx.channel.send(str(round(client.latency*1000))+'ms')

@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect(timeout=60)

@client.command()
async def play(ctx):
    audio = os.listdir('./audio clips')
    clip = audio[random.randint(0, int(len(audio)-1))]
    channel = ctx.message.author.voice.channel
    vc = await channel.connect(timeout=60)
    vc.play(discord.FFmpegPCMAudio('audio clips/' + clip,executable='ffmpeg.exe'), after=lambda e: print('done',e))
    while vc.is_playing() == True:
        pass
    if vc.is_playing() != True:
        await ctx.message.guild.voice_client.disconnect()

@client.command()
async def list(ctx):
    audio = os.listdir('./audio clips')
    string = '```'
    for i in range(0,len(audio)):
        string = string + str(i+1) + '.' + str(audio[i]) + '\n'
    string = string + '```'
    await ctx.author.send(string)

@client.command()
async def choose(ctx, arg):
    audio = os.listdir('./audio clips')
    channel = ctx.message.author.voice.channel
    vc = await channel.connect(timeout=60)
    if str.isdigit(arg) == True and int(arg) >= 1 and int(arg) <= len(audio):
        vc.play(discord.FFmpegPCMAudio('audio clips/' + audio[int(arg) - 1], executable='ffmpeg.exe'), after=lambda e: print('done', e))
        while vc.is_playing() == True:
            pass
        if vc.is_playing() != True:
            await ctx.message.guild.voice_client.disconnect()
    else:
        await ctx.channel.send('Enter an integer between 1 and ' + str(len(audio)))
        await ctx.message.guild.voice_client.disconnect()

@client.command()
async def leave(ctx):
    await ctx.message.guild.voice_client.disconnect()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

f = open('info.txt')
token = ''
for x in f:
    if x.__contains__('Token: ') == True:
        token = x[7:]
token = token.strip()
client.run(token)