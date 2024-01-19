import discord
import re
import os
from datetime import timedelta
from discord.abc import Messageable
from discord import TextChannel, Message, Thread
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import MomentoChatMessageHistory
from langchain.schema import HumanMessage, LLMResult, SystemMessage

load_dotenv()


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: Message):
    if message.channel.name == "chat-gpt" or message.channel.parent.name == "chat-gpt":
        if message.author == client.user:
            return
        
        channel: Messageable
        if message.channel.name == "chat-gpt":
            thread: Thread = await message.create_thread(name=message.content)
            channel = thread
        else:
            channel = message.channel

        content = re.sub("<@.*>", "", message.content)
        llm = ChatOpenAI(
            model_name=os.environ["OPENAI_API_MODEL"],
            temperature=os.environ["OPENAI_API_TEMPERATURE"],
        )
        response = llm.predict(content)

        await channel.send(f"{message.author.mention}\n{response}")


if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])
