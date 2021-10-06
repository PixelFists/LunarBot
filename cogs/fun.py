from discord.ext.commands import Cog, Bot, command, Context
from aiohttp import ClientSession
from discord import Embed, Message
from random import randint
from asyncio import TimeoutError

class Fun(Cog,
          name="Fun", description="Fun commands."):
    def __init__(self, client: Bot):
        self.client = client

    @command(name="joke", aliases=["j", "jok"], help="Sends a joke.")
    async def joke(self, ctx: Context):
        async with ClientSession() as cs:
            async with cs.get("https://v2.jokeapi.dev/joke/Any?safe-mode") as resp:
                data = await resp.json()

        embed = Embed(title=data['joke'] if data['type'] == "single" else data['setup'], description=data['delivery'] if data['type'] == 'twopart' else '')
        embed.set_footer(text="powered by -> jokeapi.dev\nThe developer(s) don't make these jokes.")
        await ctx.send(embed=embed)

    @command(name="darkjoke", aliases=["dj"], help="Sends a dark joke.")
    async def dark_joke(self, ctx: Context):
        async with ClientSession() as cs:
            async with cs.get("https://v2.jokeapi.dev/joke/Dark") as resp:
                data = await resp.json()
                keys = []
                for key, item in data["flags"].items():
                    if item:
                        keys.append(key)

        triggers = ', '.join(keys) if keys else ""
        embed = Embed(title=f"Warning: {triggers}\n\n||{data['joke'] if data['type'] == 'single' else data['setup']}||" \
                      if triggers else f"{data['joke'] if data['type'] == 'single' else data['setup']}",
                      description=f"{data['delivery'] if data['type'] == 'twopart' else ''}" if not triggers \
                      else f"||{data['delivery'] if data['type'] == 'twopart' else ''}||")
        embed.set_footer(text="powered by -> jokeapi.dev\nThe developer(s) don't make these jokes.")
        await ctx.send(embed=embed)

    @command(name="gtn", aliases=['guessthenumber'], help="Guess the number minigame")
    async def guess_the_number(self, ctx: Context, limit=None):
        start = 1
        if not isinstance(limit, int) or limit < start or limit is None:
            limit = 100
        num = randint(start, limit)
        await ctx.send(f"Guess the number from {start} to {limit}")
        try:
            while True:
                message: Message = await self.client.wait_for('message',
                                           check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                           timeout=60.0)
                try:
                    guess = int(message.content)
                    if guess == num:
                        return await ctx.send("Correct!")
                    elif guess > num:
                        await ctx.send("Too high")
                    else:
                        await ctx.send("Too low")
                except (SyntaxError, ValueError):
                    return await ctx.send("Guess should be a valid number.")
        except TimeoutError:
            await ctx.send(f"Timout")

def setup(client: Bot):
    client.add_cog(Fun(client))
