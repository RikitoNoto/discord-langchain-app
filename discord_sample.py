import discord
import re
import os
from discord import Message
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

load_dotenv()


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

        content = re.sub("<@.*>", "", message.content)
        llm = ChatOpenAI(
            model_name=os.environ["OPENAI_API_MODEL"],
            temperature=os.environ["OPENAI_API_TEMPERATURE"],
        )
        response = llm.predict(content)

        await message.channel.send(f"{message.author.mention}\n{response}")


if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])
