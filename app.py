import os
import platform
import discord
from discord.ext import commands
from colorama import Back, Fore, Style
from datetime import datetime
import json

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.all()) #you must enable ALL intents
        self.cogslist = ['kick_all'] #add cog files name in here

    async def setup_hook(self):
        if self.cogslist:
            for ext in self.cogslist:
                await self.load_extension(ext)

    async def on_ready(self):
        prfx = (Fore.RESET + Style.RESET_ALL + Back.BLACK + Fore.GREEN + datetime.now().strftime(r'%Y-%m-%d %H:%M:%S') + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await self.tree.sync()
        print(prfx + " Slash Commands Synced " + Fore.YELLOW + str(len(synced)) + " Commands")

client = Client()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

client.run(TOKEN)
