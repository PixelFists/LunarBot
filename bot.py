import discord, json, os
from discord.ext import commands

def config():
    with open('token.json') as f:
        return json.load(f)['token']
token = config()
client = commands.Bot(command_prefix=["lunar ", 'l!', ';'])

for cog in os.listdir("./cogs"):
    if cog.endswith('.py'):
        cog = cog[:-3]
        client.load_extension(f'cogs.{cog}')

client.load_extension("manager")
client.run(token)
