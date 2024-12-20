import discord
import random
from datetime import datetime, timedelta
from discord.ui import Button, View

from constant import WIN_RESPONSE
from ui import ttt_game_embed, game_embed
from models import TicTacToeGame, Profile

players_discord_id = []                                         # <:@656565543544534544:>
List = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


async def clear_data():
    players_discord_id.clear()
    List.clear()
    for i in range(0, 10):
        List.append(i)


async def tictactoe(main_interaction, member):
    await clear_data()

    # embed = await tic_tac_toe_embed(interaction)
    embed = await ttt_game_embed(main_interaction.user.mention, member.mention)
    players_discord_id.append(main_interaction.user.mention)
    players_discord_id.append(member.mention)

    class YourView(View):
        # button properties
        button_label = '\u200b'
        button_color = discord.ButtonStyle.gray

        def __init__(self):
            super().__init__(timeout=60)
            self.response = None
            self.click_count = 0
            self.match_complete_status = False

        @discord.ui.button(label=button_label, style=button_color, row=0)
        async def a11(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 0
            await move(self, interaction, button, value, embed)

        @discord.ui.button(label=button_label, style=button_color, row=0)
        async def a12(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 1
            await move(self, interaction, button, value, embed)

        @discord.ui.button(label=button_label, style=button_color, row=0)
        async def a13(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 2
            await move(self, interaction, button, value, embed)

        @discord.ui.button(label=button_label, style=button_color, row=1)
        async def a21(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 3
            await move(self, interaction, button, value, embed)

        @discord.ui.button(label=button_label, style=button_color, row=1)
        async def a22(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 4
            await move(self, interaction, button, value, embed)

        @discord.ui.button(label=button_label, style=button_color, row=1)
        async def a23(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 5
            await move(self, interaction, button, value, embed)

        @discord.ui.button(label=button_label, style=button_color, row=2)
        async def a31(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 6
            await move(self, interaction, button, value, embed)

        @discord.ui.button(label=button_label, style=button_color, row=2)
        async def a32(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 7
            await move(self, interaction, button, value, embed)

        @discord.ui.button(label=button_label, style=button_color, row=2)
        async def a33(self, interaction: discord.Interaction, button: discord.ui.Button):
            self.timeout = 60
            value = 8
            await move(self, interaction, button, value, embed)

        async def on_timeout(self) -> None:
            for i, child in enumerate(self.children):
                if type(child) == discord.ui.Button:
                    child.disabled = True

            random_win_message = random.choice(WIN_RESPONSE)
            if self.click_count % 2 == 0:
                idle = players_discord_id[0]
                winner = players_discord_id[1]

            else:
                idle = players_discord_id[1]
                winner = players_discord_id[0]

            new_embed = await game_embed(
                embed=embed,
                msg=f"{idle} you didn't responded for a long time\n{winner} you won!",
                time=False,
                result=True
            )
            # Editing the result response
            await main_interaction.edit_original_response(embed=new_embed, view=self)

    view = YourView()
    view.response = await main_interaction.response.send_message(embed=embed, view=view)


async def move(self, interaction, button, given, embed):
    try:
        if self.click_count == 8:  # TIE OR WIN
            button.label = '❌'
            button.disabled = True
            self.click_count += 1
            is_someone_win = await results(interaction, given, "cross", self, embed)

            # For tie
            if not is_someone_win:
                embed = await game_embed(embed, msg="It is a Tie", result=True)
                # Editing the result response
                await interaction.edit_original_response(embed=embed, view=self)

            for discord_id in players_discord_id:
                ttt_stat = await get_ttt_stat(discord_id)
                if ttt_stat:
                    ttt_stat.tie = ttt_stat.tie + 1
                    await ttt_stat.save()

        # When first player moves
        elif self.click_count % 2 == 0 and str(interaction.user.mention) == players_discord_id[0]:
            button.label = '❌'
            button.disabled = True
            await results(interaction, given, "cross", self, embed)
            self.click_count += 1

        # When second player moves
        elif self.click_count % 2 != 0 and str(interaction.user.mention) == players_discord_id[1]:
            button.label = '⭕'
            button.disabled = True
            await results(interaction, given, "circle", self, embed)
            self.click_count += 1

        # When someone else moves, or player moves in opponents turn
        else:
            if interaction.user.mention in players_discord_id:
                await interaction.response.send_message(f'> This is your opponent\'s turn!', ephemeral=True)
            else:
                await interaction.response.send_message(f'> You can\'t play someone else\'s match!', ephemeral=True)

    except Exception as e:
        print(e)
        await interaction.response.send_message('Match is over!, use </play:1123130558768238665> to play!', ephemeral=True)


async def results(interaction, value, player_move, self, embed):
    List.insert(value, player_move)
    List.remove(value)
    if List[0] == List[3] == List[6]:
        position = 0
        pattern = [0, 3, 6]
        await winner(interaction, position, self, embed, pattern)
        return True
    elif List[1] == List[4] == List[7]:
        position = 1
        pattern = [1, 4, 7]
        await winner(interaction, position, self, embed, pattern)
        return True
    elif List[2] == List[5] == List[8]:
        position = 2
        pattern = [2, 5, 8]
        await winner(interaction, position, self, embed, pattern)
        return True
    elif List[0] == List[1] == List[2]:
        position = 0
        pattern = [0, 1, 2]
        await winner(interaction, position, self, embed, pattern)
        return True
    elif List[3] == List[4] == List[5]:
        position = 3
        pattern = [3, 4, 5]
        await winner(interaction, position, self, embed, pattern)
        return True
    elif List[6] == List[7] == List[8]:
        position = 6
        pattern = [6, 7, 8]
        await winner(interaction, position, self, embed, pattern)
        return True
    elif List[0] == List[4] == List[8]:
        position = 0
        pattern = [0, 4, 8]
        await winner(interaction, position, self, embed, pattern)
        return True
    elif List[2] == List[4] == List[6]:
        position = 2
        pattern = [2, 4, 6]
        await winner(interaction, position, self, embed, pattern)
        return True
    else:
        embed = await game_embed(embed, time=True)
        await interaction.response.edit_message(embed=embed, view=self)
        return False


async def winner(interaction, position, self, embed, pattern):
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
    if List[position] == "cross":
        win_message = str(random_win_message).replace("X", players_discord_id[0]).replace("Y", players_discord_id[1])
    else:
        win_message = str(random_win_message).replace("X", players_discord_id[1]).replace("Y", players_discord_id[0])

    embed = await game_embed(embed, msg=win_message, result=True)
    # Editing the result response
    await interaction.edit_original_response(embed=embed, view=self)

    # Storing stats in DB
    for discord_id in players_discord_id:
        ttt_stat = await get_ttt_stat(discord_id)
        if List[position] == "cross" and discord_id == players_discord_id[0]:
            ttt_stat.win = ttt_stat.win + 1
            await ttt_stat.save()
        elif List[position] != "cross" and discord_id == players_discord_id[1]:
            ttt_stat.win = ttt_stat.win + 1
            await ttt_stat.save()
        else:
            ttt_stat.win = ttt_stat.loss + 1
            await ttt_stat.save()
    else:
        await clear_data()

    # if List[position] == "cross":
    #     for user_discord_id in players_discord_id:
    #         user = await Profile.get_or_none(discord_id=user_discord_id)
    #         if user:
    #             tictactoestat = await TicTacToeGame.get_or_none(uid=user)
    #             if tictactoestat:
    #                 if players_discord_id[0] == user.discord_id:
    #                     tictactoestat.win = tictactoestat.win + 1
    #                 else:
    #                     tictactoestat.loss = tictactoestat.loss + 1
    #                 await tictactoestat.save()
    #             else:
    #                 if players_discord_id[0] == user.discord_id:
    #                     new_stat = TicTacToeGame(uid=user, win=1)
    #                 else:
    #                     new_stat = TicTacToeGame(uid=user, loss=1)
    #                 await new_stat.save()
    #         else:
    #             print("user doesn't exist? why it gets created just above!")
    #
    # else:
    #     for user_discord_id in players_discord_id:
    #         user = await Profile.get_or_none(discord_id=user_discord_id)
    #         if user:
    #             tictactoestat = await TicTacToeGame.get_or_none(uid=user)
    #             if tictactoestat:
    #                 if players_discord_id[1] == user.discord_id:
    #                     tictactoestat.win = tictactoestat.win + 1
    #                 else:
    #                     tictactoestat.loss = tictactoestat.loss + 1
    #                 await tictactoestat.save()
    #             else:
    #                 if players_discord_id[1] == user.discord_id:
    #                     new_stat = TicTacToeGame(uid=user, win=1)
    #                 else:
    #                     new_stat = TicTacToeGame(uid=user, loss=1)
    #                 await new_stat.save()
    #         else:
    #             print("user doesn't exist? why it gets created just above!")
    #             await clear_data()


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



#
# class TicTacToe():
#     def __init__(self, member: discord.Member):
#         self.players_discord_id = []
#         self.list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#         self.embed = None
#
#     async def play(self, main_interaction, member):
#         self.embed = ttt_game_embed(main_interaction.user.mention, member.mention)
#         class YourView(View):
#             # button properties
#             button_label = '\u200b'
#             button_color = discord.ButtonStyle.gray
#
#             def __init__(self):
#                 super().__init__(timeout=None)
#                 self.response = None
#                 self.click_count = 0
#                 self.match_complete_status = False
#
#             @discord.ui.button(label=button_label, style=button_color, row=0)
#             async def a11(self, interaction: discord.Interaction, button: discord.ui.Button):
#                 value = 0
#                 await move(self, interaction, button, value, embed)
#
#             @discord.ui.button(label=button_label, style=button_color, row=0)
#             async def a12(self, interaction: discord.Interaction, button: discord.ui.Button):
#                 value = 1
#                 await move(self, interaction, button, value, embed)
#
#             @discord.ui.button(label=button_label, style=button_color, row=0)
#             async def a13(self, interaction: discord.Interaction, button: discord.ui.Button):
#                 value = 2
#                 await move(self, interaction, button, value, embed)
#
#             @discord.ui.button(label=button_label, style=button_color, row=1)
#             async def a21(self, interaction: discord.Interaction, button: discord.ui.Button):
#                 value = 3
#                 await move(self, interaction, button, value, embed)
#
#             @discord.ui.button(label=button_label, style=button_color, row=1)
#             async def a22(self, interaction: discord.Interaction, button: discord.ui.Button):
#                 value = 4
#                 await move(self, interaction, button, value, embed)
#
#             @discord.ui.button(label=button_label, style=button_color, row=1)
#             async def a23(self, interaction: discord.Interaction, button: discord.ui.Button):
#                 value = 5
#                 await move(self, interaction, button, value, embed)
#
#             @discord.ui.button(label=button_label, style=button_color, row=2)
#             async def a31(self, interaction: discord.Interaction, button: discord.ui.Button):
#                 value = 6
#                 await move(self, interaction, button, value, embed)
#
#             @discord.ui.button(label=button_label, style=button_color, row=2)
#             async def a32(self, interaction: discord.Interaction, button: discord.ui.Button):
#                 value = 7
#                 await move(self, interaction, button, value, embed)
#
#             @discord.ui.button(label=button_label, style=button_color, row=2)
#             async def a33(self, interaction: discord.Interaction, button: discord.ui.Button):
#                 value = 8
#                 await move(self, interaction, button, value, embed)
#
#         view = YourView()
#         view.response = await main_interaction.response.send_message(embed=embed, view=view)
#
#
