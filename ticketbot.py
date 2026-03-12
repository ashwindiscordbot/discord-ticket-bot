# ticketbot.py
import discord
from discord.ext import commands
from datetime import timedelta
import os

# Get your token from Replit Secrets
TOKEN = os.environ['TOKEN']

# Enable all intents (make sure Privileged Intents are ON in Developer Portal)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# When bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('Bot is online and ready!')

# Command to create a ticket
@bot.command()
async def ticket(ctx):
    """Create a private ticket channel."""
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True)
    }
    ticket_channel = await guild.create_text_channel(
        name=f'ticket-{ctx.author.name}', overwrites=overwrites
    )
    await ticket_channel.send(f"Hello {ctx.author.mention}, support will be with you soon!")
    await ctx.send(f"Ticket created: {ticket_channel.mention}", delete_after=5)

# Command to close a ticket
@bot.command()
async def close(ctx):
    """Close the ticket channel."""
    if ctx.channel.name.startswith("ticket-"):
        await ctx.send("Closing this ticket in 5 seconds...")
        await asyncio.sleep(5)  # Wait 5 seconds before deletion
        await ctx.channel.delete()
    else:
        await ctx.send("This command can only be used in ticket channels.", delete_after=5)

# Run the bot
bot.run(TOKEN)
