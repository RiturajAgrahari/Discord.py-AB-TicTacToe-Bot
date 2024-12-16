import discord
from discord.ui import Button, View
from ui import tic_tac_toe_embed, ttt_game_embed
from dotenv import load_dotenv
from models import TicTacToeGame, Profile

load_dotenv()

players_discord_id = []                                         # <:@656565543544534544:>
List = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


async def clear_data():
    players_discord_id.clear()
    List.clear()
    for i in range(0, 10):
        List.append(i)


async def tictactoe(interaction):
    await clear_data()

    embed = await tic_tac_toe_embed(interaction)

    class MyView(View):
        def __init__(self):
            super().__init__(timeout=None)
            self.response = None
            self.click_count = 0

        @discord.ui.button(label='Join', style=discord.ButtonStyle.blurple, custom_id="my_button")
        async def ttt(self, interaction: discord.Interaction, button: discord.ui.Button):
            user = await Profile.get_or_none(discord_id=interaction.user.mention)
            if not user:
                u = Profile(discord_id=interaction.user.mention, discord_name=interaction.user.name)
                await u.save()

            if self.click_count == 0:
                self.click_count += 1
                # client1 = str(interaction.user)
                await interaction.response.send_message(f'{interaction.user.mention} Joined!', ephemeral=True)
                # player_name.append(client1)
                players_discord_id.append(str(interaction.user.mention))
                # Player.append(client1.split('#')[0])

            elif self.click_count == 1 and str(interaction.user.mention) not in players_discord_id:
                self.click_count += 1
                # client2 = str(interaction.user)
                # player_name.append(client2)
                # Player.append(client2.split('#')[0])
                players_discord_id.append(interaction.user.mention)
                button.disabled = True
                await interaction.response.edit_message(view=self)
                await interaction.followup.send(f'Match is started!\n{players_discord_id[0]} V/S {players_discord_id[1]}')
                await game(interaction, players_discord_id[0], players_discord_id[1])
            else:
                if interaction.user.mention in players_discord_id:
                    await interaction.response.send_message(f'You already joined the match!', ephemeral=True)
                else:
                    await interaction.response.send_message(f'Match Ended!', ephemeral=True)

    view = MyView()
    view.response = await interaction.response.send_message(embed=embed, view=view)


async def game(interaction, player1, player2):
    embed = await ttt_game_embed(player1, player2)

    class YourView(View):
        def __init__(self):
            super().__init__(timeout=None)
            self.response = None
            self.click_count = 0

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=0)
        async def a11(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 0
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=0)
        async def a12(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 1
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=0)
        async def a13(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 2
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=1)
        async def a21(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 3
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=1)
        async def a22(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 4
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=1)
        async def a23(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 5
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=2)
        async def a31(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 6
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=2)
        async def a32(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 7
            await move(self, interaction, button, value)

        @discord.ui.button(label='-', style=discord.ButtonStyle.blurple, row=2)
        async def a33(self, interaction: discord.Interaction, button: discord.ui.Button):
            value = 8
            await move(self, interaction, button, value)

    view = YourView()
    view.response = await interaction.followup.send(embed=embed, view=view)


async def move(self, interaction, button, given):
    try:
        if self.click_count == 8:
            button.label = '❌'
            button.disabled = True
            self.click_count += 1
            await interaction.response.edit_message(view=self)
            player_move = "cross"
            await results(interaction, given, player_move, None, self)
            if len(players_discord_id) == 0:
                print("someone won!")
            else:
                # TIE
                await interaction.followup.send(f"{players_discord_id[0]} and {players_discord_id[1]} it's a tie")
                for user_discord_id in players_discord_id:
                    user = await Profile.get_or_none(discord_id=user_discord_id)
                    if user:
                        tictactoestat = await TicTacToeGame.get_or_none(uid=user.id)
                        if tictactoestat:
                            tictactoestat.tie = tictactoestat.tie + 1
                            await tictactoestat.save()
                        else:
                            new_stat = TicTacToeGame(uid=user.id, tie=1)
                            await new_stat.save()
                    else:
                        print("user doesn't exist? why it gets created just above!")

        elif self.click_count % 2 == 0 and str(interaction.user.mention) == players_discord_id[0]:
            button.label = '❌'
            button.disabled = True
            self.click_count += 1
            await interaction.response.edit_message(view=self)
            player_move = "cross"
            await results(interaction, given, player_move, players_discord_id[1], self)
        elif self.click_count % 2 != 0 and str(interaction.user.mention) == players_discord_id[1]:
            button.label = '⭕'
            button.disabled = True
            self.click_count += 1
            await interaction.response.edit_message(view=self)
            player_move = "circle"
            await results(interaction, given, player_move, players_discord_id[0], self)
        else:
            if interaction.user.mention in players_discord_id:
                await interaction.response.send_message(f'This is not your turn!', ephemeral=True)
            else:
                await interaction.response.send_message(f'The game is already ended!', ephemeral=True)
    except:
        await interaction.response.send_message('Match is over!, use </play:1123130558768238665> to play!', ephemeral=True)


async def results(interaction, value, player_move, turn, self):
    List.insert(value, player_move)
    List.remove(value)
    if List[0] == List[3] == List[6]:
        position = 0
        await winner(interaction, position, self)
    elif List[1] == List[4] == List[7]:
        position = 1
        await winner(interaction, position, self)
    elif List[2] == List[5] == List[8]:
        position = 2
        await winner(interaction, position, self)
    elif List[0] == List[1] == List[2]:
        position = 0
        await winner(interaction, position, self)
    elif List[3] == List[4] == List[5]:
        position = 3
        await winner(interaction, position, self)
    elif List[6] == List[7] == List[8]:
        position = 6
        await winner(interaction, position, self)
    elif List[0] == List[4] == List[8]:
        position = 0
        await winner(interaction, position, self)
    elif List[2] == List[4] == List[6]:
        position = 2
        await winner(interaction, position, self)
    else:
        pass
        # if turn is not None:
        #     await interaction.followup.send(f'{turn} Your turn')
        # else:
        #     pass


async def winner(interaction, position, self):
    # for child in self.children:
    #     if type(child) == discord.ui.Button:
    #         child.disabled = True
    # await response.edit(view=self)
    self.click_count = "exit"
    await interaction.followup.send(f'{interaction.user.mention} you won!<:H37sneer:997036721843736637>')
    if List[position] == "cross":
        for user_discord_id in players_discord_id:
            user = await Profile.get_or_none(discord_id=user_discord_id)
            if user:
                tictactoestat = await TicTacToeGame.get_or_none(uid=user)
                if tictactoestat:
                    if players_discord_id[0] == user.discord_id:
                        tictactoestat.win = tictactoestat.win + 1
                    else:
                        tictactoestat.loss = tictactoestat.loss + 1
                    await tictactoestat.save()
                else:
                    if players_discord_id[0] == user.discord_id:
                        new_stat = TicTacToeGame(uid=user, win=1)
                    else:
                        new_stat = TicTacToeGame(uid=user, loss=1)
                    await new_stat.save()
            else:
                print("user doesn't exist? why it gets created just above!")

    else:
        for user_discord_id in players_discord_id:
            user = await Profile.get_or_none(discord_id=user_discord_id)
            if user:
                tictactoestat = await TicTacToeGame.get_or_none(uid=user)
                if tictactoestat:
                    if players_discord_id[1] == user.discord_id:
                        tictactoestat.win = tictactoestat.win + 1
                    else:
                        tictactoestat.loss = tictactoestat.loss + 1
                    await tictactoestat.save()
                else:
                    if players_discord_id[1] == user.discord_id:
                        new_stat = TicTacToeGame(uid=user, win=1)
                    else:
                        new_stat = TicTacToeGame(uid=user, loss=1)
                    await new_stat.save()
            else:
                print("user doesn't exist? why it gets created just above!")
                await clear_data()
