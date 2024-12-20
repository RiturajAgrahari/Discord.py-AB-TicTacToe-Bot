import discord
from datetime import datetime, timedelta


async def ttt_game_embed(player1, player2):
    unix_time_now = datetime.now()
    unix_future_time = unix_time_now + timedelta(seconds=60)
    countdown = unix_future_time.strftime('%s')

    embed = discord.Embed(title='Tic Tac Toe',
                          description=f'{player1} (❌) challenged {player2} (⭕) in tic tac toe',
                          colour=discord.Colour.from_rgb(51, 55, 59))
    embed.set_footer(text="By Arena Breakout")

    embed.add_field(name=f"Move within <t:{countdown}:R>", value='\u200b', inline=False)
    return embed


async def game_embed(embed, msg=None, time=False, result=False):
    embed.remove_field(0)
    # If time = True, it will reset time to 60 seconds
    if time:
        unix_time_now = datetime.now()
        unix_future_time = unix_time_now + timedelta(seconds=60)
        countdown = unix_future_time.strftime('%s')
        embed.add_field(name=f"Move within <t:{countdown}:R>", value='\u200b', inline=False)

    if result:
        if "tie" in msg:
            embed.color = discord.Color.red()
        else:
            embed.color = discord.Color.gold()
        embed.add_field(
            name="Results",
            value=msg,
            inline=False
        )
    return embed
