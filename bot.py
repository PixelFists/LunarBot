import discord, json, os
from discord.ext import commands

def config():
    with open('config.json') as f:
        return json.load(f)
