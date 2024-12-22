import discord
import random

from discord import Interaction
from discord.ui import Button, View

from constant import WIN_RESPONSE
from ui import ttt_game_embed, game_embed, get_countdown
from models import TicTacToeGame, Profile

matches = {}


# Asking for challenge acceptance and refusal to the opponent
async def challenge(main_interaction, member, uid):
    matches[uid] = {
        "players_discord_id": [main_interaction.user.mention, member.mention],
        "List": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    }

    class MyView(View):
        def __init__(self):
            super().__init__(timeout=120)
            self.response = None
            self.challenge_status = False

        # Accepting challenge
        @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, row=0)
        async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
            await tictactoe(interaction, main_interaction, uid)

        # Refusing challenge
        @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, row=0)
        async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Disabling button and changing Accept button style to gray
            for i, child in enumerate(self.children):
                if type(child) == discord.ui.Button:
                    child.disabled = True
                    if i == 0:
                        child.style = discord.ButtonStyle.gray

            # Removing match
            matches.pop(uid)

            # Editing response
            await main_interaction.edit_original_response(
                content=f"{interaction.user.mention} has declined your tic tac toe challenge! {main_interaction.user.mention}",
                view=self
            )

            # Sending interaction response as it is necessary to do so
            await interaction.response.send_message("> Challenge Declined!", ephemeral=True)

        # Interaction check
        async def interaction_check(self, interaction: Interaction, /) -> bool:
            # Check whether the challenged player is responding or not
            if interaction.user.mention == member.mention:
                self.challenge_status = True
                return True
            await interaction.response.send_message(
                f"> Only the challenged player can accept or decline the invitation",
                ephemeral=True
            )

        # When challenge is expired
        async def on_timeout(self) -> None:
            if not self.challenge_status:
                # Disabling button
                for child in self.children:
                    if type(child) == discord.ui.Button:
                        child.disabled = True

                # Removing match
                matches.pop(uid)

                # Editing response
                await main_interaction.edit_original_response(
                    content=f'> {member.mention} didn\'t responded to the challenge invitation by'
                            f' {main_interaction.user.mention}\n'
                            f'> The challenge is expired!',
                    view=self
                )

    # Sending challenge invitation
    countdown = await get_countdown(seconds=120)

    # Check for match reports
    for match in matches.keys():
        # This is your match.
        if match == uid:
            continue
        else:
            # [Message] Finish your match before challenging for a new match.
            if main_interaction.user.mention in matches[match]["players_discord_id"]:
                matches.pop(uid)
                await main_interaction.response.send_message(
                    content=f"> You are already in a game. Please finish it before starting new",
                    ephemeral=True
                )
                break

            # [Message] Other player is already in challenge with someone.
            elif member.mention in matches[match]["players_discord_id"]:
                matches.pop(uid)
                await main_interaction.response.send_message(
                    content=f"> The opponent is already in a match with someone, Kindly wait for his/her match to end",
                    ephemeral=True
                )
                break

    # If there is no match with any one of the user then.
    else:
        view = MyView()
        view.response = await main_interaction.response.send_message(
            content=f'> {main_interaction.user.mention} challenged {member.mention} in tic tac toe, would you like to'
                    f' accept the challenge?\n> The invitation will expire {countdown}',
            view=view
        )


async def tictactoe(main_interaction, member, uid):
    # Match Board Embed
    embed = await ttt_game_embed(member.user.name, main_interaction.user.name)

    class YourView(View):
        # Button properties
        button_label = '-'
        # button_label = '\u200b'
        button_color = discord.ButtonStyle.gray

        def __init__(self):
            super().__init__(timeout=60)
            self.response = None
            self.click_count = 0
            self.match_complete_status = False
            self.value = None

        @discord.ui.button(label=button_label, style=button_color, row=0)
        async def a11(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 0
            await move(self, interaction, button, value, embed, uid)

        @discord.ui.button(label=button_label, style=button_color, row=0)
        async def a12(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 1
            await move(self, interaction, button, value, embed, uid)

        @discord.ui.button(label=button_label, style=button_color, row=0)
        async def a13(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 2
            await move(self, interaction, button, value, embed, uid)

        @discord.ui.button(label=button_label, style=button_color, row=1)
        async def a21(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 3
            await move(self, interaction, button, value, embed, uid)

        @discord.ui.button(label=button_label, style=button_color, row=1)
        async def a22(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 4
            await move(self, interaction, button, value, embed, uid)

        @discord.ui.button(label=button_label, style=button_color, row=1)
        async def a23(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 5
            await move(self, interaction, button, value, embed, uid)

        @discord.ui.button(label=button_label, style=button_color, row=2)
        async def a31(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 6
            await move(self, interaction, button, value, embed, uid)

        @discord.ui.button(label=button_label, style=button_color, row=2)
        async def a32(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 7
            await move(self, interaction, button, value, embed, uid)

        @discord.ui.button(label=button_label, style=button_color, row=2)
        async def a33(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 8
            await move(self, interaction, button, value, embed, uid)

        async def on_timeout(self) -> None:
            if not self.match_complete_status:
                for i, child in enumerate(self.children):
                    if type(child) == discord.ui.Button:
                        child.disabled = True

                if self.click_count % 2 == 0:
                    idle = matches[uid]["players_discord_id"][0]
                    winner = matches[uid]["players_discord_id"][1]

                else:
                    idle = matches[uid]["players_discord_id"][1]
                    winner = matches[uid]["players_discord_id"][0]

                new_embed = await game_embed(
                    embed=embed,
                    msg=f"{idle} you didn't respond for a long time\n{winner} you won!",
                    time=False,
                    result=True
                )
                # Editing the result response
                await main_interaction.edit_original_response(embed=new_embed, view=self)

                # Removing match
                matches.pop(uid)

    view = YourView()
    view.response = await main_interaction.response.edit_message(
        content=f'> {main_interaction.user.mention} accepted {matches[uid]["players_discord_id"][0]} challenge!',
        embed=embed,
        view=view
    )


async def move(self, interaction, button, given, embed, uid):
    try:
        if self.click_count == 8:  # TIE OR WIN
            button.label = '❌'
            button.disabled = True
            self.click_count += 1
            is_someone_win = await results(interaction, given, "cross", self, embed, uid)
            self.match_complete_status = True
            # For tie
            if not is_someone_win:
                embed = await game_embed(embed, msg="It is a Tie", result=True)
                # Editing the result response
                await interaction.edit_original_response(embed=embed, view=self)

            # for discord_id in players_discord_id:
            for discord_id in matches[uid]["players_discord_id"]:
                ttt_stat = await get_ttt_stat(discord_id)
                if ttt_stat:
                    ttt_stat.tie = ttt_stat.tie + 1
                    await ttt_stat.save()

            # Removing match
            matches.pop(uid)

        # When first player moves
        elif self.click_count % 2 == 0 and str(interaction.user.mention) == matches[uid]["players_discord_id"][0]:
            button.label = '❌'
            button.disabled = True
            await results(interaction, given, "cross", self, embed, uid)
            self.click_count += 1

        # When second player moves
        elif self.click_count % 2 != 0 and str(interaction.user.mention) == matches[uid]["players_discord_id"][1]:
            button.label = '⭕'
            button.disabled = True
            await results(interaction, given, "circle", self, embed, uid)
            self.click_count += 1

        # When someone else moves, or player moves in opponents turn
        else:
            if interaction.user.mention in matches[uid]["players_discord_id"]:
                await interaction.response.send_message(f'> This is your opponent\'s turn!', ephemeral=True)
            else:
                await interaction.response.send_message(f'> You can\'t play someone else\'s match!', ephemeral=True)

    except Exception as e:
        print(e)
        await interaction.response.send_message('Match is over!, use </play:1123130558768238665> to play!', ephemeral=True)


async def results(interaction, value, player_move, self, embed, uid):
    matches[uid]["List"].insert(value, player_move)
    matches[uid]["List"].remove(value)
    if matches[uid]["List"][0] == matches[uid]["List"][3] == matches[uid]["List"][6]:
        position = 0
        pattern = [0, 3, 6]
        await winner(interaction, position, self, embed, pattern, uid)
        return True
    elif matches[uid]["List"][1] == matches[uid]["List"][4] == matches[uid]["List"][7]:
        position = 1
        pattern = [1, 4, 7]
        await winner(interaction, position, self, embed, pattern, uid)
        return True
    elif matches[uid]["List"][2] == matches[uid]["List"][5] == matches[uid]["List"][8]:
        position = 2
        pattern = [2, 5, 8]
        await winner(interaction, position, self, embed, pattern, uid)
        return True
    elif matches[uid]["List"][0] == matches[uid]["List"][1] == matches[uid]["List"][2]:
        position = 0
        pattern = [0, 1, 2]
        await winner(interaction, position, self, embed, pattern, uid)
        return True
    elif matches[uid]["List"][3] == matches[uid]["List"][4] == matches[uid]["List"][5]:
        position = 3
        pattern = [3, 4, 5]
        await winner(interaction, position, self, embed, pattern, uid)
        return True
    elif matches[uid]["List"][6] == matches[uid]["List"][7] == matches[uid]["List"][8]:
        position = 6
        pattern = [6, 7, 8]
        await winner(interaction, position, self, embed, pattern, uid)
        return True
    elif matches[uid]["List"][0] == matches[uid]["List"][4] == matches[uid]["List"][8]:
        position = 0
        pattern = [0, 4, 8]
        await winner(interaction, position, self, embed, pattern, uid)
        return True
    elif matches[uid]["List"][2] == matches[uid]["List"][4] == matches[uid]["List"][6]:
        position = 2
        pattern = [2, 4, 6]
        await winner(interaction, position, self, embed, pattern, uid)
        return True
    else:
        embed = await game_embed(embed, time=True)
        await interaction.response.edit_message(embed=embed, view=self)
        return False


async def winner(interaction, position, self, embed, pattern, uid):
    self.match_complete_status = True

    # Disabling all buttons as match is ended
    for i, child in enumerate(self.children):
        if type(child) == discord.ui.Button:
            child.disabled = True
            if i in pattern:
                child.style = discord.ButtonStyle.green

    # Implementing disabled buttons
    embed = await game_embed(embed)
    await interaction.response.edit_message(embed=embed, view=self)

    # Creating a result response message
    random_win_message = random.choice(WIN_RESPONSE)
    if matches[uid]["List"][position] == "cross":
        win_message = str(random_win_message).replace("X", matches[uid]["players_discord_id"][0]).replace("Y", matches[uid]["players_discord_id"][1])
    else:
        win_message = str(random_win_message).replace("X", matches[uid]["players_discord_id"][1]).replace("Y", matches[uid]["players_discord_id"][0])

    embed = await game_embed(embed, msg=win_message, result=True)
    # Editing the result response
    await interaction.edit_original_response(embed=embed, view=self)

    # Storing stats in DB
    for discord_id in matches[uid]["players_discord_id"]:
        ttt_stat = await get_ttt_stat(discord_id)
        if matches[uid]["List"][position] == "cross" and discord_id == matches[uid]["players_discord_id"][0]:
            ttt_stat.win = ttt_stat.win + 1
            await ttt_stat.save()
        elif matches[uid]["List"][position] != "cross" and discord_id == matches[uid]["players_discord_id"][1]:
            ttt_stat.win = ttt_stat.win + 1
            await ttt_stat.save()
        else:
            ttt_stat.win = ttt_stat.loss + 1
            await ttt_stat.save()
    else:
        matches.pop(uid)


async def get_ttt_stat(discord_id):
    user = await Profile.get_or_none(discord_id=discord_id)
    if user:
        tictactoestat = await TicTacToeGame.get_or_none(uid=user)
        if not tictactoestat:
            new_stat = TicTacToeGame(uid=user)
            await new_stat.save()
            return new_stat
        else:
            return tictactoestat
    else:
        print("user doesn't exist? why it gets created just above!")
