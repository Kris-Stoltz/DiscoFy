import discord
from discord.ext import commands
import bot

cogs = [bot]

client = commands.Bot(command_prefix='>', intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)


client.run('ODk4NzUyNTc5MDgzODMzMzY0.YWoykA.owAZIUS6dxtR0_1PXlTREBtCtuU')