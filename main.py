import discord
from discord.ext import commands, tasks
from asyncio import sleep

bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name='/help'))

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: int):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.add_roles(muted_role)
    await ctx.send(f'{member.mention} has been muted for {duration} seconds.')
    await sleep(duration)
    await member.remove_roles(muted_role)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(muted_role)
    await ctx.send(f'{member.mention} has been unmuted.')

bot.run('YOUR_DISCORD_TOKEN')
