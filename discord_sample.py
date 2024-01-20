import discord
import re
import os
from datetime import timedelta
from discord.abc import Messageable
from discord import TextChannel, Message, Thread
from dotenv import load_dotenv
from langchain.chains import ConversationChain, ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage, LLMResult, SystemMessage
from vectorstore import initialize_vectorstore

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
        
        
        thread: Messageable
        # if it isn't in a thread, create a thread from the message content.
        if message.channel.name == "chat-gpt":
            title = message.content
            thread: Thread = await message.create_thread(name=title[:100])
        else:
            thread = message.channel
            
        history = ChatMessageHistory()
        async for thread_message in thread.history(limit=100):
            content = re.sub("<@.*>", "", thread_message.content) or re.sub("<@.*>", "", thread_message.system_content)
            
            if thread_message.author == client.user:
                history.add_ai_message(content)
            else:
                history.add_user_message(content)
            
        content = re.sub("<@.*>", "", message.content)
        history.add_user_message(content)
        
        vector_store = initialize_vectorstore()
        
        llm = ChatOpenAI(
            model_name=os.environ["OPENAI_API_MODEL"],
            temperature=os.environ["OPENAI_API_TEMPERATURE"],
        )
        condense_question_llm = ChatOpenAI(
            model_name=os.environ["OPENAI_API_MODEL"],
            temperature=os.environ["OPENAI_API_TEMPERATURE"],
        )

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(),
            memory=ConversationBufferMemory(chat_memory=history, memory_key="chat_history", return_messages=True),
            condense_question_llm=condense_question_llm,
        )
        response = qa_chain.run(message.content)

        await thread.send(f"{message.author.mention}\n{response}")


if __name__ == "__main__":
    client.run(os.environ["DISCORD_TOKEN"])
