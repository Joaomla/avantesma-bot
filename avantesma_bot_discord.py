import discord
import random
import asyncio
from datetime import datetime
import wikipedia
import requests

from tokens import Tokens

greetings = ['Hi!', 'Hello!', 'Hello there!']

class MyClient(discord.Client):

    async def hello(self, message):
        if message.content.startswith('!hi') or message.content.startswith('!hello'):
            hello_id = random.randint(0, len(greetings))

            if hello_id == len(greetings):
                now = datetime.now()
                current_hour = int(now.strftime('%H'))
                if 6 < current_hour < 12:
                    await message.channel.send('Good Morning!')
                elif 12 <= current_hour < 18:
                    await message.channel.send('Good Afternoon!')
                else:
                    await message.channel.send('Good Evening!')
                return

            await message.channel.send(greetings[hello_id])

    async def guess_game(self, message):
        if message.content.startswith('!guess'):
            await message.channel.send('Guess a number between 1 and 10.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send('Sorry, you took too long. The number was {}.'.format(answer))

            if int(guess.content) == answer:
                await message.channel.send('You are right!')
            else:
                await message.channel.send('Wrong. It was actually {}.'.format(answer))

    async def rock_paper_scissors_game(self, message):
        if message.content.startswith('!rps'):
            await message.channel.send('Rock, Paper, Scissors. Shoot!')

            rps = ['rock', 'paper', 'scissors']

            def is_correct(m):
                return m.author == message.author and m.content.lower() in rps

            bot_choice = random.randint(0,len(rps)-1)

            try:
                user_choice = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send('Sorry, you took too long! I got tired.')

            user_choice = rps.index(user_choice.content.lower())

            if user_choice == bot_choice:
                await  message.channel.send("It's a tie!")
            elif user_choice == (bot_choice + 1) % 3:
                await message.channel.send("Congrats! I chose {}, so you win.".format(rps[bot_choice].capitalize()))
            else:
                await message.channel.send("I win! I chose {}.".format(rps[bot_choice].capitalize()))
    
    async def wiki(self, message):
        if message.content.startswith('!wiki'):
            search = message.content.replace("!wiki", "")
            if search == '':
                return
            try:
                results = wikipedia.summary(search, sentences=3)
            except wikipedia.DisambiguationError as e:
                s = random.choice(e.options)
                results = wikipedia.summary(s, sentences=3)
                return await message.channel.send("According to Wikipedia: \n" + results)
            return await message.channel.send("According to Wikipedia: \n" + results)
    

    async def on_ready(self):
        print('Logged in as {0.user}'.format(client))

    async def on_message(self, message):
        # the robot shouldn't reply to itself
        if message.author.id == self.user.id:
            return

        await self.hello(message)
        await self.guess_game(message)
        await self.rock_paper_scissors_game(message)
        await self.wiki(message)


if __name__ == "__main__":
    client = MyClient()
    client.run(Tokens.discord_token)
