import discord
from datetime import datetime, timedelta


async def ttt_game_embed(player1, player2):
    unix_time_now = datetime.now()
    unix_future_time = unix_time_now + timedelta(seconds=60)
    countdown = unix_future_time.strftime('%s')

    embed = discord.Embed(title='Tic Tac Toe',
                          description=f'- {player1} ❌ \n- {player2} ⭕',
                          colour=discord.Colour.from_rgb(79, 80, 87))
    embed.set_footer(text="By Arena Breakout")

    embed.add_field(name=f"Mark <t:{countdown}:R>", value='\u200b', inline=False)
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
