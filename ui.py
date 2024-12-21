import discord
from datetime import datetime, timedelta


async def ttt_game_embed(player1, player2):
    countdown = await get_countdown(seconds=60)
    embed = discord.Embed(title='Tic Tac Toe',
                          description=f'- {player1} ❌ \n- {player2} ⭕',
                          colour=discord.Colour.from_rgb(79, 80, 87))
    embed.set_footer(text="By Arena Breakout")

    embed.add_field(name=f"Mark {countdown}", value='\u200b', inline=False)
    return embed


async def game_embed(embed, msg=None, time=False, result=False):
    embed.remove_field(0)
    # If time = True, it will reset time to 60 seconds
    if time:
        countdown = await get_countdown(seconds=60)
        embed.add_field(name=f"Mark {countdown}", value='\u200b', inline=False)

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


async def get_countdown(seconds=10):
    unix_time_now = datetime.now()
    unix_future_time = unix_time_now + timedelta(seconds=seconds)
    unix_countdown = unix_future_time.strftime('%s')
    countdown = f"<t:{unix_countdown}:R>"
    return countdown
