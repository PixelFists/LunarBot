from discord.ext.commands import Cog, Bot, command, Context
from aiohttp import ClientSession
from discord import Embed

class Fun(Cog):
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
        triggers = ""
        async with ClientSession() as cs:
            async with cs.get("https://v2.jokeapi.dev/joke/Dark") as resp:
                data = await resp.json()
                keys = []
                for key, item in data["flags"].items():
                    if item:
                        keys.append(key)
                        triggers = ', '.join(keys)

        embed = Embed(title=f"Warning: {triggers}\n\n||{data['joke'] if data['type'] == 'single' else data['setup']}||" \
                      if triggers else f"{data['joke'] if data['type'] == 'single' else data['setup']}",
                      description=f"{data['delivery'] if data['type'] == 'twopart' else ''}" if not triggers \
                      else f"||{data['delivery'] if data['type'] == 'twopart' else ''}||")
        embed.set_footer(text="powered by -> jokeapi.dev\nThe developer(s) don't make these jokes.")
        await ctx.send(embed=embed)

def setup(client: Bot):
    client.add_cog(Fun(client))
