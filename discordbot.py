import discord
from discord.ext import commands

from main import translate  # Import the translate function from main.py

# Set up the bot with the necessary intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# Command: /translate
@bot.command()
async def translate(ctx):
    # Check if the command is used in the #manipur channel
    if ctx.channel.name != 'manipur':
        # Send an ephemeral message if the command is not used in the #manipur channel
        await ctx.reply("This command can only be used in the #manipur channel.", ephemeral=True)
        return

        # Check if the user replied to a message
        if not ctx.message.reference:
        await ctx.reply("Please reply to a message to use this command.", ephemeral=True)
        return

        # Get the replied message
        try:
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except discord.NotFound:
        await ctx.reply("Could not fetch the replied message. It may have been deleted.", ephemeral=True)
        return

        # Get the text of the replied message
        text_to_translate = replied_message.content

        # Check if the replied message has content to translate
        if not text_to_translate.strip():
        await ctx.reply("The replied message has no text to translate.", ephemeral=True)
        return

        # Call the translate function from main.py
        try:
        translated_text = translate(text_to_translate)
        except Exception as e:
        await ctx.reply(f"An error occurred during translation: {str(e)}", ephemeral=True)
        return

        # Send the translated text as an ephemeral message to the command user
        await ctx.reply(f"Translated text: {translated_text}", ephemeral=True)
    await ctx.author.send(f"Translated text: {translated_text}")

# Run the bot
bot.run('YOUR_DISCORD_BOT_TOKEN')