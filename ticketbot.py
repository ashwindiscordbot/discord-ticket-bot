# ticketbot.py
import discord
from discord.ext import commands
import os

# Read token from environment variable (Replit secret)
TOKEN = os.environ['TOKEN']

# Enable all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Store ticket channels in memory
ticket_channels = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('Bot is online and ready!')

# Command to create a ticket
@bot.command()
async def ticket(ctx, *, reason=None):
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True)
    }
    channel_name = f"ticket-{ctx.author.name}"
    ticket_channel = await guild.create_text_channel(channel_name, overwrites=overwrites, reason=reason)
    ticket_channels[ctx.author.id] = ticket_channel.id
    await ticket_channel.send(f"{ctx.author.mention}, your ticket has been created! Reason: {reason if reason else 'No reason provided'}")
    await ctx.send(f"{ctx.author.mention}, your ticket channel is {ticket_channel.mention}")

# Command to close a ticket
@bot.command()
async def close(ctx):
    if ctx.channel.id in ticket_channels.values():
        await ctx.send("Closing this ticket in 5 seconds...")
        await discord.utils.sleep_until(discord.utils.utcnow() + discord.timedelta(seconds=5))
        await ctx.channel.delete()
    else:
        await ctx.send("This command can only be used inside a ticket channel.")

bot.run(TOKEN)
