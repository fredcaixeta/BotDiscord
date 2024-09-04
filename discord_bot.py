import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter o token do bot e o ID do canal de teste das variáveis de ambiente
BOT_TOKEN = os.getenv('BOT_TOKEN')
TEST_CHANNEL_ID = int(os.getenv('TEST_CHANNEL_ID'))
MAIN_GUILD_ID = int(os.getenv('MAIN_GUILD_ID'))  # Certifique-se de que o ID da guilda esteja no .env

print(TEST_CHANNEL_ID)

# Configurar intents (permitir que o bot leia mensagens de texto)
intents = discord.Intents.default()
intents.message_content = True

# Criar uma instância do bot com o prefixo de comando "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# Evento que é chamado quando o bot se conecta com sucesso ao servidor
@bot.event
async def on_ready():
    print(f'Logado como {bot.user}')  # Confirmação no console
    channel = bot.get_channel(TEST_CHANNEL_ID)
    if channel is not None:
        await channel.send("AI Bot is online!")  # Enviar mensagem ao canal especificado
    else:
        print("Canal não encontrado. Verifique o ID do canal.")
    
    # Sincronizar comandos globais e de guilda (por exemplo, comandos slash)
    guild = discord.Object(id=MAIN_GUILD_ID)
    try:
        await bot.tree.sync(guild=guild)
        print(f"Comandos sincronizados com a guilda {MAIN_GUILD_ID}.")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

# Carregar todos os cogs da pasta 'cogs'
async def load_extensions():
    try:
        await bot.load_extension('cogs.slash_commands')
        print(f"Cog cogs.slashcommands carregado com sucesso.")
    except Exception as e:
        print(f"Falha ao carregar cog cogs.slashcommands: {e}")

# Inicializa a execução do bot e carrega os cogs
async def main():
    async with bot:
        await load_extensions()
        await bot.start(BOT_TOKEN)

# Executa o bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())