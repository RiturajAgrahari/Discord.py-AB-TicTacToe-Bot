import os
import sys
from dotenv import load_dotenv
from typing import Literal
import uuid

import discord
from discord import app_commands
from discord.errors import Forbidden

from ttt import challenge
from models import Profile
from db import db_init

# LOADING ENV
load_dotenv()


# INITIALIZING
MY_GUILD = int(os.getenv("MY_GUILD"))
TEST_GUILD = int(os.getenv("TEST_GUILD"))
MAIN_GUILD = int(os.getenv("MAIN_GUILD"))
guilds = [MY_GUILD, TEST_GUILD, MAIN_GUILD]

permitted_users = ['<@568179896459722753>']

responses = [
    "_magic 🪄... try the command again </play:1302652188148891690>_",
    "_ghost came into the way 👻... try the command again </play:1302652188148891690>_",
    "_ uf! high traffic  🚦... try the command again </play:1302652188148891690>_",
    "_ is this your parcel?  📦... try the command again </play:1302652188148891690>_"
]


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """
        Initializing guilds and connecting it to the bot.
        :return:
        """
        for guild in guilds:
            main_guild = discord.Object(id=guild)
            try:
                self.tree.copy_global_to(guild=main_guild)
                await self.tree.sync(guild=main_guild)
            except Forbidden:
                print(f"UNABLE TO CONNECT TO GUILD-ID : {guild}")


# Running the client with specific permissions
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Your Tic Tac Toe bot in successfully started as {client.user} (ID: {client.user.id})')
    print('-----')
    await db_init()
    await client.change_presence(activity=discord.Game(name="/play-games"))


@client.event
async def on_message(message):
    # Check if the message author is not client itself
    if message.author == client.user:
        pass

    # Checks if the message is recieved in DM
    elif message.channel.type == discord.ChannelType.private:
        print(f'Bot DM --> [{message.author}] : {message.content}')

    # Message in server channels
    else:
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        guild_name = message.guild.name
        # print(f'[channel: {channel}] --> {username}: {user_message}')

        if message.author.mention in permitted_users:
            if user_message == "tommy!":
                await message.reply(content="wuff wuff!")

            # elif user_message == "$config":
            #     await config_bot(message, luck, client)


@client.tree.command(name="play-games", description="Choose a game to play!")
async def play(interaction: discord.Interaction, games: Literal['tic tac toe'], member: discord.Member = None):
    uid = uuid.uuid4()
    if interaction.user != member:
        # Creating profiles in DB
        users = [
            (str(interaction.user.mention), str(interaction.user.name)),
            (str(member.mention), str(member.name)) if member else None
        ]
        for user in users:
            if user:
                user_exist = await Profile.get_or_none(discord_id=user[0])
                if not user_exist:
                    # Creating user
                    new_user = Profile(discord_id=user[0], discord_name=user[1])
                    await new_user.save()

        # Play games
        if games == 'tic tac toe':
            await challenge(interaction, member, str(uid))

        else:
            await send_error(__file__, '/play', 'user trying to play unknown game!', server="Arena Breakout")
            print(games)
    else:
        await interaction.response.send_message("> You can't play with yourself!", ephemeral=True)


# @client.tree.command(name="statistics", description="Choose a game to check the statistics of a specific player!")
# async def stat(interaction: discord.Interaction, games: Literal['rock paper scissor'],
#                member: discord.Member = None):
#     uid = await check_profile(interaction)
#     await bot_uses(datetime.date.today())
#     avatar_url = await get_avatar_url(interaction)
#     game = games.replace(' ', '_')
#     print(f'{interaction.user.name} checking {member if member else "his own"} statistics in {games}')
#     if games == 'rock paper scissor':
#         await rps_stat(uid, interaction, game, member, avatar_url)
#     # elif game == 'guess_the_number':
#     #     await guess_stat(uid, interaction, game, member, avatar_url)
#     else:
#         await send_error(__file__, '/statistics', 'user trying to check stat of unknown game!')
#         print(games)


# @client.tree.command(name="leaderboard", description="Which game leaderboard you want to check!")
# async def leaderboard(interaction: discord.Interaction, games: Literal['rock paper scissor', 'koens']):
#     await bot_uses(datetime.date.today())
#     if games == 'rock paper scissor':
#         data = Leaderboard('rock_paper_scissor')
#         win_data = data.win_board()
#         await rps_leaderboard(interaction, games, win_data)
#     # elif games == 'guess the number':
#     #     data = Leaderboard('guess_the_number')
#     #     win_data = data.win_board()
#     #     await gtn_leaderboard(interaction, games, win_data)
#     elif games == 'koens':
#         await interaction.response.defer()
#         data = Leaderboard('inventory')
#         koens = data.koens()
#         embed = await koens_leaderboard(interaction, koens)
#         await interaction.followup.send(embed=embed)
#     else:
#         print('under development!')


async def send_error(file, function_name, error, server='Arena Breakout'):
    embed = discord.Embed(title=f'{server} Server', description=file, color=discord.Color.red())
    embed.add_field(name=function_name, value=error, inline=False)
    user = await client.fetch_user(568179896459722753)
    await user.send(embed=embed)


@client.event
async def on_error(event, *args, **kwargs):
    error = str(sys.exc_info())
    error = error.replace(',', '\n')
    await send_error(__file__, event, error)


client.run(token=os.getenv("TOKEN"))





