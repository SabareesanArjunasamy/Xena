import asyncio
import math
import os
import discord
import requests
import json
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()

token = os.getenv('TOKEN')


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


allowedChannels = ['general']

prefix = '!'

intents.guild_messages = True
intents.reactions = True

@client.event
async def on_ready():
    print('Logged in as',client.user.name)
    

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if 'happy birthday' in message.content.lower():
        msg = (message.content.lower().split())
        person = ''
        for i in msg:
            if '<' in i:
                person = i
        await message.channel.send('Happy Birthday! ' + person+' By Sab 🎈🎉')
    print('message - content', message.content)
    

    print(f"{message.author.name} said: {message.content}")

    args = message.content[len(prefix):].strip().split()
    command = args.pop(0).lower()

    if command == 'poll':
        # Get the poll question and timer duration from the message
        question = ' '.join(args[:-1])
        duration_minutes = int(args[-1]) if args and args[-1].isdigit() else 1

        # Calculate the poll duration in seconds
        duration_seconds = duration_minutes * 60

        # Send the poll message
        poll_message_text = f'**Poll:** {question}\n**Duration:** {duration_minutes} minute{"s" if duration_minutes > 1 else ""}'
        poll_message = await message.channel.send(poll_message_text)
        await poll_message.add_reaction('👍')
        await poll_message.add_reaction('👎')

        # Set up the poll timer
        async def poll_timer(poll_message):
            for remaining_seconds in range(duration_seconds, 0, -1):
                minutes, seconds = divmod(remaining_seconds, 60)
                timer_text = f'{minutes:02d}:{seconds:02d}'
                poll_message_text_with_timer = f'{poll_message_text}\n**Time Remaining:** {timer_text}'
                await poll_message.edit(content=poll_message_text_with_timer)
                await asyncio.sleep(1)

            await poll_message.remove_reaction('👍', client.user)
            await poll_message.remove_reaction('👎', client.user)

            # Get the poll results
            poll_message = await message.channel.fetch_message(poll_message.id)
            results = poll_message.reactions

            # Format the poll results
            total_votes = sum(reaction.count - 1 for reaction in results)  # Subtract 1 to exclude the bot's own reaction
            result_text = f'**Poll Results:**\n{poll_message_text}\n'
            for reaction in results:
                users = []
                async for user in reaction.users():
                    if not user.bot:
                        users.append(user)
                count = len(users)
                if total_votes == 0:
                    percentage = 0
                else:
                    percentage = math.ceil(count / total_votes * 100)
                result_text += f'{reaction.emoji}: {count} ({percentage}%)\n'

            # Display the poll results
            await message.channel.send(result_text)

        # Start the poll timer
        asyncio.ensure_future(poll_timer(poll_message))

    elif command == 'test':
        await message.channel.send('This is a test command!')


@client.event
async def on_reaction_add(reaction, user):
    channel = discord.utils.get(user.guild.channels, name='general')
    if user.id != client.user.id and reaction.message.channel == channel:
        cache_msg = discord.utils.get(client.cached_messages, id=reaction.message.id)

        # Check every reaction in the cache_msg
        for r in cache_msg.reactions:
            async for u in r.users():
                if u.id == user.id and not u.bot and str(r) != str(reaction.emoji):
                    await reaction.remove(user)



    



# Connect the bot to Discord using the bot token
client.run(token)
