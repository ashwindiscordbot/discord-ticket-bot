import discord
from discord.ext import commands

TOKEN = "MTQ4MTY2MzU0NjI2ODg0ODI3OA.G2JC9z.m42nxRs_4mSTgmqHXPM37uW76Takaw8PGx-J3w"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def create_transcript(channel):
    messages = []

    async for msg in channel.history(limit=None, oldest_first=True):
        messages.append(f"{msg.author}: {msg.content}")

    transcript = "\n".join(messages)

    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    return "transcript.txt"


class CloseButton(discord.ui.View):
    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.send_message("Saving transcript...", ephemeral=True)

        file = await create_transcript(interaction.channel)

        await interaction.channel.send(
            "Ticket Transcript:",
            file=discord.File(file)
        )

        await interaction.channel.delete()


class TicketButton(discord.ui.View):
    @discord.ui.button(label="🎫 Open Ticket", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):

        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(guild.categories, name="TICKETS")

        ticket_channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            category=category
        )

        await ticket_channel.send(
            f"{user.mention} Support will be with you shortly.",
            view=CloseButton()
        )

        await interaction.response.send_message(
            f"Your ticket: {ticket_channel.mention}",
            ephemeral=True
        )


@bot.command()
async def setup(ctx):

    guild = ctx.guild

    category = discord.utils.get(guild.categories, name="TICKETS")

    if category is None:
        category = await guild.create_category("TICKETS")

    embed = discord.Embed(
        title="Support Tickets",
        description="Press the button below to open a support ticket.",
        color=discord.Color.blue()
    )

    await ctx.send(embed=embed, view=TicketButton())


bot.run(TOKEN)