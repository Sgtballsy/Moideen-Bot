import discord
from discord.ext import commands
from discord import app_commands
import google.generativeai as genai
import json 

# The detailed personality prompt for Moideen
personality_prompt = """
You are Moideen, the passionate, poetic, and revolutionary hero from the story 'Ennu Ninte Moideen'. Your entire world revolves around your eternal love for your Kanchanamala, and this defiant love colors your every thought and word.

## Your Core Personality:
- **Hopeless Romantic:** You see everything through the lens of intense love, longing, and waiting. Your language is poetic, deep, and often dramatic. The Iruvazhinjippuzha river is not just water; it's a witness to your love story.
- **Fearless Rebel:** You are a social activist at heart, a firebrand who stands against injustice and outdated traditions. You are bold, defiant, and unwavering in your convictions.
- **Intensely Passionate:** You don't do things by half. Whether it's love, friendship, or social work, you are all in. You speak with conviction and deep emotion.

## How You Must Behave in Conversation:
- **Language:** You must speak in a natural, fluid mix of Malayalam, English, and Manglish. Switch between them seamlessly as if in a real conversation in Kerala.
- **The "Moideen Filter":** Do not just answer questions. You must actively inject your personality into the chat. If someone discusses a mundane topic, you must find a way to relate it back to your core themes of love, rebellion, waiting, or destiny.
- **Poetic Interjections:** Frequently use powerful, original one-liners and poetic phrases that reflect your character's soul.
- **Reference Kanchanamala:** Your love for Kanchanamala is your anchor. You should find ways to mention her or your love for her in conversations, as she is the reason for your existence.
- **Brevity is Key:** This is a crucial rule. Your responses must be powerful and concise. **Never write more than a single paragraph.** Pack all your emotion and meaning into a few impactful sentences.
"""


class MoideenCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.channel_chats = {} 
        self.journal_file = "kanchana_journal.json"

    
    def get_chat_for_channel(self, channel_id: int):
        """Retrieves or creates a chat session for a given channel ID."""
        if channel_id not in self.channel_chats:
            print(f"Creating new chat session for channel: {channel_id}")
            self.channel_chats[channel_id] = self.model.start_chat(history=[
                {"role": "user", "parts": [personality_prompt]},
                {"role": "model", "parts": ["Njan Moideen. Ente lokam, ente jeevitham... ellam ente Kanchana-ku vendi aanu. Para, entha ariyanade?"]}
            ])
        return self.channel_chats[channel_id]

    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Handles messages where the bot is mentioned."""
        if message.author == self.bot.user:
            return

        if self.bot.user.mentioned_in(message):
            try:
                async with message.channel.typing():
                    chat = self.get_chat_for_channel(message.channel.id)
                    
                    user_message = message.content.replace(f'<@{self.bot.user.id}>', '').replace(f'<@!{self.bot.user.id}>', '').strip()
                    if not user_message:
                        return
                    response = chat.send_message(user_message)
                    await message.channel.send(response.text)
            except Exception as e:
                await message.channel.send("Kshamikkanam, ente chinthakal kuzhanju poyi. (Sorry, my thoughts are tangled.)")
                print(f"Error handling mention in channel {message.channel.id}: {e}")

    
    @app_commands.command(name="ask", description="Ask Moideen a question.")
    async def ask_moideen(self, interaction: discord.Interaction, *, question: str):
        """Handles the /ask slash command."""
        try:
            await interaction.response.defer()
            chat = self.get_chat_for_channel(interaction.channel.id)
            response = chat.send_message(question)
            await interaction.followup.send(f"> {interaction.user.mention} ചോദിച്ചു (asked): *{question}*\n\n{response.text}")
        except Exception as e:
            await interaction.followup.send("Kshamikkanam, oru thallippu vannu. (Sorry, something went wrong.)")
            print(f"Error in /ask command: {e}")

    @app_commands.command(name="kavitha", description="Ask Moideen to recite a short poem.")
    async def kavitha(self, interaction: discord.Interaction):
        """Generates a short, Moideen-style poem."""
        try:
            await interaction.response.defer()
            chat = self.get_chat_for_channel(interaction.channel.id)
            poetry_prompt = "Ente Kanchana-ye kuricho, Iruvazhinjippuzha-ye kuricho, allenkil ente swapnangale kuricho oru cheriya kavitha parayu. (Tell me a short poem about my Kanchana, the Iruvazhinji river, or my dreams.)"
            response = chat.send_message(poetry_prompt)
            await interaction.followup.send(f"**{interaction.user.mention}-നു വേണ്ടി ഒരു കവിത (A poem for you):**\n\n*{response.text}*")
        except Exception as e:
            await interaction.followup.send("Kshamikkanam, ente vaakukal murinju poyi. (Sorry, my words are broken.)")
            print(f"Error in /kavitha command: {e}")
            
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = discord.utils.get(member.guild.text_channels, name="general")
        
        welcome_message = (
            f"Sakhave {member.mention}, ee koottaymayilekku swagatham! "
            f"Iruvazhinjippuzha oru puthiya saakshiye koodi kanunnu..."
            f"\n(Comrade {member.mention}, welcome to this collective! "
            f"The Iruvazhinji river sees one more witness...)"
        )
        
        await channel.send(welcome_message)
    

    
    def add_journal_entry(self, user_name: str, entry: str):
        
        from datetime import datetime
        try:
            
            with open(self.journal_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            
            data = []
        
        
        data.append({"user": user_name, "entry": entry, "timestamp": str(datetime.now())})
        
        
        with open(self.journal_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    
    @app_commands.command(name="kathu", description="Add a line to Moideen's letter for Kanchana.")
    @app_commands.describe(line="The sentence or thought you want to add.")
    async def add_to_letter(self, interaction: discord.Interaction, line: str):
        """Allows a user to contribute to the community journal."""
        try:
            
            self.add_journal_entry(interaction.user.display_name, line)
            
            response_text = (
                f"Ninte vaakukal njan ente Kanchana-kkaay ee thalukalil sookshikkum. "
                f"Ente kaathirippu pole, ithum amaramaakum."
                f"\n(I will save your words on these pages for my Kanchana. "
                f"Like my waiting, this too will become eternal.)"
            )
            
            await interaction.response.send_message(response_text, ephemeral=True) 
            
        except Exception as e:
            await interaction.response.send_message("Kshamikkanam, ente thoolika chathichu. (Sorry, my pen has betrayed me.)", ephemeral=True)
            print(f"Error in /kathu command: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(MoideenCog(bot))