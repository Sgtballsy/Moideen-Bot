import discord
from discord.ext import commands
from discord import app_commands

class UtilityCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kanakku", description="Get poetic stats about the server.")
    async def server_info(self, interaction: discord.Interaction):
        """Shows information about the server."""
        server = interaction.guild
        member_count = server.member_count
        
        embed = discord.Embed(
            title=f"{server.name} - Oru Kurippu", 
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=server.icon.url if server.icon else None)
        embed.add_field(
            name="Sakhakkal (Comrades)", 
            value=f"Ee koottaymayil **{member_count}** poraalikal undu.",
            inline=False
        )
        embed.set_footer(text="Nammal onnaayi oru puthiya naale theerkkum! (Together we will forge a new tomorrow!)")
        
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot): 
    await bot.add_cog(UtilityCog(bot))