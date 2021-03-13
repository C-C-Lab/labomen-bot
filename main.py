import discord
import random

# 必要な設定を定義
ACCESS_TOKEN = 'ODIwMjcwNTYwOTUyMTg4OTQ4.YEyufQ.XtPyfFRuytMTU06fW85jnVbsCVE'
ready_message = "接続し、準備ができました"

client = discord.Client()

@client.event
async def on_ready():
    #Test Code
    print(ready_message)
    print(discord.__version__)

@client.event
async def on_message(message):
    if message.author.bot:
        return

client.run(ACCESS_TOKEN)
