import os
import discord

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'hello':
        print('got hello')
        await message.channel.send("Hi There...!")
        
        
client.run(token)