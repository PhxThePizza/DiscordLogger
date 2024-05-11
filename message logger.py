import discord
from discord.ext import commands
import os

class MessageLogger(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')
        
        # Create a folder for each server
        for guild in self.guilds:
            folder_name = f'message-log-{guild.name.lower().replace(" ", "-")}'
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                print(f'Created folder: {folder_name}')  # Add this debug statement

            # Create a .txt file for each channel in the server
            for channel in guild.text_channels:
                file_name = f'{channel.name.lower().replace(" ", "-")}.txt'
                file_path = os.path.join(folder_name, file_name)
                with open(file_path, 'w', encoding='utf-8') as file:
                    pass
                print(f'Created file: {file_path}')  # Add this debug statement

    async def on_message(self, message):
        if message.author == self.user:
            return

        timestamp = message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        guild_name = message.guild.name if message.guild else 'Direct Message'
        channel_name = message.channel.name if hasattr(message.channel, 'name') else 'Unknown'
        author_name = message.author.name
        content = message.content

        log_entry = f'[{timestamp}] [{guild_name}] [{channel_name}] {author_name}: {content}'
        print(log_entry)

        folder_name = f'message-log-{guild_name.lower().replace(" ", "-")}'
        file_name = f'{channel_name.lower().replace(" ", "-")}.txt'
        file_path = os.path.join(folder_name, file_name)
        try:
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(log_entry + '\n')
        except FileNotFoundError:
            print(f"Error: Folder or file doesn't exist: {file_path}")  # Add this debug statement

client = MessageLogger()
client.run(input("What is your discord token?: "))