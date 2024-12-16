import discord


async def tic_tac_toe_embed(interaction):
    embed = discord.Embed(
        title="❌Tic_Tac_Toe❌",
        description=f"A game in which two players seek in alternate turns to complete a row, a column, or a diagonal"
                    f" with either three O's or three X's drawn in the spaces of a grid of nine squares.",
        color=discord.Color.green(),
    )

    embed.add_field(name="⭕Tap JOIN to get into the game⭕",
                    value="2 Players required",
                    inline=False)

    embed.set_footer(text=f"Requested By {interaction.user}")
    return embed


async def ttt_game_embed(player1, player2):
    embed = discord.Embed(title='Tic Tac Toe',
                          description='You have to complete a row,\n column, or a diagonal with your\n mark to win',
                          colour=discord.Colour.red())
    embed.add_field(name='Players Joined',
                    value=f'{player1} is ❌\n'
                          f'{player2} is ⭕',
                    inline=True)

    return embed
