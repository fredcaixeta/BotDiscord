from discord.ext import commands
import discord

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Link para o Caminho das Armas.")
    async def armas(self, ctx):
        embed = discord.Embed(title="Caminho das Armas ⚔️", description="https://homebrewery.naturalcrit.com/share/JJz9jnEpNBXX", color=discord.Color.yellow())
        await ctx.send(embed=embed)

    @commands.command(help="Link para o Caminho do Subterfúgio.")
    async def subterfugio(self, ctx):
        embed = discord.Embed(title="Caminho do Subterfúgio 🗡️", description="https://homebrewery.naturalcrit.com/share/a6LemoDGJRJe", color=discord.Color.yellow())
        await ctx.send(embed=embed)

    @commands.command(help="Link para o Caminho da Sabedoria.")
    async def sabedoria(self, ctx):
        embed = discord.Embed(title="Caminho da Sabedoria 🧙‍♂️", description="https://homebrewery.naturalcrit.com/share/afJ-Pm3kb31W", color=discord.Color.yellow())
        await ctx.send(embed=embed)

    @commands.command()
    async def comandos(self, ctx):
        embed = discord.Embed(title="Meus Comandos", description="Aqui está a lista de todos os comandos disponíveis:", color=discord.Color.yellow())
        for command in self.bot.commands:
            embed.add_field(name=f'!{command.name}', value=command.help or "Sem descrição", inline=False)
        await ctx.send(embed=embed)
        
    @commands.command(help="Cargos")
    async def roles(self, ctx):
        embed = discord.Embed(title="Escolha seu Caminho!", description="Não se preocupe, o caminho que escolher não precisa ter a ver com o seu personagem criado, ele pode ser apenas um motivo para novos jogadores o consultarem se tiverem com dúvidas sobre o Caminho", color=discord.Color.yellow())
        embed.add_field(name="Caminho das Armas", value="⚔️", inline=True)
        embed.add_field(name="Caminho da Sabedoria", value="🧙‍♂️", inline=True)
        embed.add_field(name="Caminho do Subterfúgio", value="🗡️", inline=True)
        
        message = await ctx.send(embed=embed)
        emojis = ["⚔️", "🧙‍♂️", "🗡️"]
        for emoji in emojis:
            await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        guild = reaction.message.guild
        role_name = None

        if reaction.emoji == "⚔️":
            role_name = "Caminho das Armas"
        elif reaction.emoji == "🧙‍♂️":
            role_name = "Caminho da Sabedoria"
        elif reaction.emoji == "🗡️":
            role_name = "Caminho do Subterfúgio"

        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await user.add_roles(role)
                await user.send(f"Você agora pertence ao {role_name}!")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return

        guild = reaction.message.guild
        role_name = None

        if reaction.emoji == "⚔️":
            role_name = "Caminho das Armas"
        elif reaction.emoji == "🧙‍♂️":
            role_name = "Caminho da Sabedoria"
        elif reaction.emoji == "🗡️":
            role_name = "Caminho do Subterfúgio"

        if role_name:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await user.remove_roles(role)
                await user.send(f"Você não pertence mais ao {role_name}!")

async def setup(bot):
    await bot.add_cog(Commands(bot))