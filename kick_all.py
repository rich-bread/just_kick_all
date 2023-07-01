import json
import discord
from discord.ext import commands
from discord import app_commands

cmd_file = open('cmd_kick.json') #open command file
cmd_data = json.load(cmd_file) #load command file

class KickAll(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client
        self.cmd_data = cmd_data

    @app_commands.command(name=cmd_data['name'], description=cmd_data['description'])
    @app_commands.checks.has_role(cmd_data['checks']['role_id'])
    async def kick_all(self, interaction:discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True, thinking=True) #make interaction defer
            members = interaction.guild.members #get all members from guild
            avoids_file = open('avoids.json') #open avoid list
            avoids_data = json.load(avoids_file) #load avoid list
            members_id = avoids_data['members_id'] #get members id who you want to avoid from kicking
            roles_id = avoids_data['roles_id'] #get roles id which you want to avoid from kicking
            for member in members:
                print(f"Current subject is: {member}")
                if member.id == self.client.user.id: continue #continue if the member is this client
                if member.id == interaction.user.id: continue #continue if the member is the author of the executed command
                if member.id in members_id: continue #continue if the member is in the avoid list
                for member_role in member.roles:
                    if member_role.id in roles_id: 
                        role_bool = False #set bool as False when member has the role to be avoided
                        break
                    else: role_bool = True #set bool as True when member does not have the role to be avoided
                if role_bool != True: continue #continue if the member has the role to be avoided
                await member.kick() #kick member / if you want to add a reason, add here
                print(f"Kicked: {str(member)}")

        except Exception as e:
            emsg = self.cmd_data['messages']['error']['on_exception'].format(content=e) #error message
            await interaction.followup.send(content=emsg, ephemeral=True) #send error message as ephemeral

        else:
            smsg = self.cmd_data['messages']['success']['on_success'] #success message
            await interaction.followup.send(content=smsg, ephemeral=True) #send success message as ephemeral

    @kick_all.error
    async def on_kick_all_error(self, interaction:discord.Interaction, error:app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole): #error when command author was missing required role
            smsg = self.cmd_data['messages']['error']['on_missing_role'] #error message
            await interaction.response.send_message(content=smsg, ephemeral=True) #send success message as ephemeral


async def setup(client: commands.Bot):
    await client.add_cog(KickAll(client)) #add cog to client
