from email.mime import message
import discord
from discord.ext import commands, tasks
from discord import app_commands
import requests
import os
import re
import datetime
from datetime import time

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== EVENTO =====
@bot.event
async def on_ready():
    await bot.tree.sync()
    
    atividade = discord.CustomActivity(
        name="PriestHelper | /liturgia"
    )

    await bot.change_presence(
        status=discord.Status.online,
        activity=atividade
    )

    if not enviar_liturgia_automatica.is_running():
        enviar_liturgia_automatica.start()

    print(f"Estou ligado! 🤖 {bot.user}")


# ===== COR DA LITURGIA =====
def cor_embed(cor_liturgica: str) -> int:
    cores = {
        "Verde": 0x2ecc71,
        "Roxo": 0x8e44ad,
        "Vermelho": 0xe74c3c,
        "Branco": 0xecf0f1,
        "Rosa": 0xfd79a8,
        "Preto": 0x2d3436
    }
    return cores.get(cor_liturgica, 0x3498db)

# ===== DIVIDIR TEXTO GRANDE EM PARTES =====
def dividir_texto(texto: str, tamanho: int = 1024):
    return [texto[i:i+tamanho] for i in range(0, len(texto), tamanho)]

# ===== ADICIONAR LEITURAS AO EMBED (ROBUSTO) =====
def adicionar_leituras(embed, titulo, lista_leituras, emoji):
    for leitura in lista_leituras:
        partes = dividir_texto(leitura["texto"])

        # Garante que sempre exista pelo menos uma parte
        if not partes:
            partes = ["(Texto indisponível)"]

        # Primeiro campo COM título
        embed.add_field(
            name=f"{emoji} {titulo} ({leitura['referencia']})",
            value=partes[0],
            inline=False
        )

        # Campos seguintes SEM repetir título
        for parte in partes[1:]:
            embed.add_field(
                name="\u200b",
                value=parte,
                inline=False
            )

# ===== SLASH COMMAND =====
@bot.tree.command(name="liturgia", description="Mostra a liturgia completa do dia")
@app_commands.describe(data="Data no formato DD-MM-YYYY (opcional)")
async def liturgia(
    interaction: discord.Interaction,
    data: str | None = None
):
    # ===== VALIDAR DATA =====
    if data:
        if not re.fullmatch(r"\d{2}-\d{2}-\d{4}", data):
            await interaction.response.send_message(
                "⚠️ Formato inválido.\nUse **DD-MM-YYYY** (ex: 03-01-2026).",
                ephemeral=True
            )
            return
        url = f"https://liturgia.up.railway.app/v2/{data}"
    else:
        url = "https://liturgia.up.railway.app/v2/"

    # ===== CHAMADA DA API =====
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()

    except requests.RequestException:
        await interaction.response.send_message(
            "⚠️ Não consegui acessar a liturgia agora ou você pode ter digitado a data errada.",
            ephemeral=True
        )
        return

    # ===== DADOS PRINCIPAIS =====
    liturgia_nome = dados["liturgia"]
    cor = dados["cor"]
    leituras = dados["leituras"]
    data = dados.get("data", "Data não informada")

    # ===== EMBED =====
    embed = discord.Embed(
        title=f"📅 Liturgia de {data}",
        description=f"📖 **{liturgia_nome}**\n🎨 Cor litúrgica: **{cor}**",
        color=cor_embed(cor)
    )

    # ===== ORDEM LITÚRGICA REAL =====
    adicionar_leituras(
        embed,
        "Primeira Leitura",
        leituras.get("primeiraLeitura", []),
        "📖"
    )

    adicionar_leituras(
        embed,
        "Salmo",
        leituras.get("salmo", []),
        "🎵"
    )

    adicionar_leituras(
        embed,
        "Segunda Leitura",
        leituras.get("segundaLeitura", []),
        "📘"
    )

    adicionar_leituras(
        embed,
        "Evangelho",
        leituras.get("evangelho", []),
        "✝️"
    )

    embed.set_footer(text="Fonte: liturgia.up.railway.app")

    await interaction.response.send_message(embed=embed)

@tasks.loop(time=time(19, 0))
async def enviar_liturgia_automatica():
    canal = bot.get_channel(1448836352761135268)

    if not canal:
        return

    try:
        resposta = requests.get("https://liturgia.up.railway.app/v2/", timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
    except requests.RequestException:
        await canal.send("⚠️ Não consegui entregar a liturgia diária hoje.")
        return

    liturgia_nome = dados["liturgia"]
    cor = dados["cor"]
    leituras = dados["leituras"]
    data_api = dados.get("data", "Data não informada")

    embed = discord.Embed(
        title=f"📅 Liturgia Diária",
        description=f"📖 **{liturgia_nome}**\n🎨 Cor litúrgica: **{cor}**",
        color=cor_embed(cor)
    )

    adicionar_leituras(embed, "Primeira Leitura", leituras.get("primeiraLeitura", []), "📖")
    adicionar_leituras(embed, "Salmo", leituras.get("salmo", []), "🎵")
    adicionar_leituras(embed, "Segunda Leitura", leituras.get("segundaLeitura", []), "📘")
    adicionar_leituras(embed, "Evangelho", leituras.get("evangelho", []), "✝️")

    embed.set_footer(text="Fonte: liturgia.up.railway.app")

    await canal.send(embed=embed)

DEBATE_CHANNEL_ID = 1448832962111082649

PALAVRAS_PROIBIDAS = [
    "idiota",
    "burro",
    "imbecil"
]

DEBATE_CHANNEL_ID = 1448832962111082649

PALAVRAS_PROIBIDAS = [
    "idiota",
    "burro",
    "imbecil"
]

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if not message.guild:
        return

    # garante que é thread (fórum)
    if not message.channel.parent:
        return

    # verifica se a thread pertence ao fórum certo
    if message.channel.parent.id != DEBATE_CHANNEL_ID:
        return

    conteudo = message.content.lower()

    for palavra in PALAVRAS_PROIBIDAS:
        if palavra in conteudo:
            await message.delete()

            aviso = await message.channel.send(
                f"{message.author.mention}, cuidado com as palavras! 🚫"
            )
            await aviso.delete(delay=60)
            break

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
