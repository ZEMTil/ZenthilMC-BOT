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
    if not muted_role:
        muted_role = await ctx.guild.create_role(name='Muted')
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)

    if muted_role in member.roles:
        await ctx.send(f'{member.mention} is already muted.')
        return

    await member.add_roles(muted_role, reason=f'Muted for {duration} seconds.')
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
