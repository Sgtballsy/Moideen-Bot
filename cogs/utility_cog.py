import discord
from discord.ext import commands
from discord import app_commands

class UtilityCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="kannaku", description="Get Poetic Stats about The Server")
    async def server_info(self, intercation: discord.Interaction):
        server = interaction.guild
        member_count = server.member_count
        
        embed = discord.Embed(
            title=f"S{server.name} - Oru Kurippu (A Note)",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=server.icon.url if server.icon else None)
        embed.add_field(
            name="Sakhakale (Comrades)",
            value=f"Ee koottaymaye oru saakshi: {member_count} sakhakal (This collective has {member_count} comrades)",
            inline=False
        )
        embed.set_footer(text="Nammal onnaayi oru puthiya naale theerkkum (Together we shall shape a new tomorrow)")
        
        await interaction.response.send_message(embed=embed)
    
    
    async def setup(bot: commands.Bot):
        await bot.add_cog(UtilityCog(bot))