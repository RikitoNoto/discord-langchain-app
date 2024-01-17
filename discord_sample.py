import discord
from discord import Message, TextChannel

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: Message):
    if message.channel.name == "chat-gpt":
        if message.author == client.user:
            return
        await message.channel.send("Hello!")
        if message.content.startswith("$hello"):
            await message.channel.send("Hello!")


client.run("")
