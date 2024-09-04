import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import os
from dotenv import load_dotenv
import requests
import json

import openai

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API da OpenAI do arquivo .env
openai.api_key = os.getenv('OPENAI_API_KEY')


try:
    ANNOUNCE_CHANNEL_ID = int(os.getenv('ANNOUNCE_CHANNEL_ID'))
    BACKGROUNDS_CHANNEL_ID = int(os.getenv('BACKGROUNDS_CHANNEL_ID'))
    BUILDS_CHANNEL_ID = int(os.getenv('BUILDS_CHANNEL_ID'))
    MAIN_GUILD_ID = int(os.getenv('MAIN_GUILD_ID'))
    
except TypeError:
    raise ValueError("One or more environment variables are missing or not set correctly.")

class ConfirmButton(View):
    def __init__(self, user, embed, target_channel, moderation_channel, bot, title_type, files):
        super().__init__(timeout=60) 
        self.user = user
        self.embed = embed
        self.target_channel = target_channel
        self.moderation_channel = moderation_channel
        self.bot = bot
        self.title_type = title_type
        self.files = files

    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("Você não pode confirmar isso.", ephemeral=True)
            return

        await interaction.response.send_message("A sua publicação foi confirmada e publicada!", ephemeral=True)
        await self.target_channel.send(embed=self.embed)
        
        if self.files:
            await self.target_channel.send(files=[await file.to_file() for file in self.files])

        await self.moderation_channel.send(f"{self.user.display_name} ({self.user.id}) postou um {self.title_type}.")
        
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("Você não pode cancelar essa mensagem.", ephemeral=True)
            return
        
        await interaction.response.send_message("Sua publicação foi cancelada.", ephemeral=True)
        self.stop()

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(self.announce, guild=discord.Object(id=MAIN_GUILD_ID))
        self.bot.tree.add_command(self.testeai, guild=discord.Object(id=MAIN_GUILD_ID))
        #self.bot.tree.add_command(self.build, guild=discord.Object(id=MAIN_GUILD_ID))

    def get_openai_completion(self, system_message, questions):
    # Lista para armazenar as mensagens formatadas
        formatted_questions = [
            {
                "role": "system",
                "content": system_message
            }
        ]

        # Verifica e formata as perguntas
        for question in questions:
            if not isinstance(question, dict) or ('assistant' not in question and 'user' not in question):
                return {"error": "Each question must be a dict containing the keys 'assistant' or 'user'"}
            
            if 'assistant' in question:
                formatted_questions.append({
                    "role": "assistant",
                    "content": question['assistant']
                })
            
            if 'user' in question:
                formatted_questions.append({
                    "role": "user",
                    "content": question['user']
                })

        # Configuração da API
        api_url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"  # Use a chave da API do ambiente
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": formatted_questions
        }

        # Envio da requisição para a API
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))

        # Verifica se a resposta é válida
        if response.status_code == 200:
            response_data = response.json()
            return response_data["choices"][0]["message"]["content"]
        else:
            return {"error": response.status_code, "message": response.text}
        
    @app_commands.command(name="anuncio", description="Envia um anúncio RP no #anuncios-roleplay")
    async def announce(self, interaction: discord.Interaction):
        await interaction.response.send_message("Olhe seu privado para continuarmos o anuncio.", ephemeral=True)
        await self.send_dm(interaction.user, ANNOUNCE_CHANNEL_ID, "anúncio", "o anúncio", "anúncio", "seu anúncio")

    @app_commands.command(name="testeai", description="Testando o OpenAI para o Epic!")
    async def testeai(self, interaction: discord.Interaction):
        await interaction.response.send_message("Olhe seu privado para continuarmos...", ephemeral=True)
        await self.send_dm(interaction.user, BACKGROUNDS_CHANNEL_ID, "testeai", "a história do seu personagem", "personagem", "seu background")

    async def send_dm(self, user: discord.User, channel_id: int, title_type: str, description_prompt: str, title_prompt: str, success_message: str):
        def check(m):
            return m.author == user and isinstance(m.channel, discord.DMChannel)
        
        try:
            restart = True
            while restart == True:
                dm_channel = await user.create_dm()
                #var systemMessage := "Você é um banqueiro medieval de RPG. Responda como tal. O aventureiro que fala com você é um " + sourceRaca + "com descrição" + sourceDescription + ". Máximo de 50 caracteres.";
                await dm_channel.send(f"Fale ao ChatGPT o contexto do personagem (NPC) - Exemplo: Você é um banqueiro medieval de RPG. Responda como tal. O aventureiro que fala com você é um drow com descrição <está sangrando muito>. Máximo de 50 caracteres.")
                context = await self.bot.wait_for('message', check=check)
                context = context.content
                
                await dm_channel.send(f"Agora a interação com o Player - Exemplo: Olá banqueiro, traga meu cofre! - ou - Parado aí! Largue a arma!")
                message_player = await self.bot.wait_for('message', check=check)
                
                message_player = [{"user": message_player.content}]
                resposta_ai = self.get_openai_completion(context, message_player)
                
                #resposta_ai = "teste"
                await dm_channel.send(f"OpenAI: {resposta_ai} \n *** \n AI BOT: Deseja começar de novo? Yes / No")
                restart_confirm = await self.bot.wait_for('message', check=check)
                
                if restart_confirm == "No":
                    restart = False
                    
                
            file_urls = []
            file_attachments = []
            
            """
            if files_to_include.content.lower() != 'nenhum':
                if files_to_include.attachments:
                    file_attachments = files_to_include.attachments
                else:
                    file_urls = files_to_include.content.split()
            
            
            
            if file_urls:
                for url in file_urls:
                    embed.add_field(name="File URL", value=url, inline=False)
            
            view = ConfirmButton(user, embed, self.bot.get_channel(channel_id), self.bot.get_channel(MODERATION_CHANNEL_ID), self.bot, title_type, file_attachments)
            #await dm_channel.send("Aqui está uma prévia da sua publicação:", embed=embed, view=view)
            
            if file_attachments:
                await dm_channel.send("Esses são os arquivos que você anexou:", files=[await file.to_file() for file in file_attachments])
            """
        except Exception as e:
            await dm_channel.send(f"Ocorreu um erro: {e}")

async def setup(bot):
    await bot.add_cog(SlashCommands(bot))