import os
from dotenv import load_dotenv
from discord.ext import commands
import asyncio

from utils import get_search_results, get_recent_queries

load_dotenv('.env')

# Bot Instantiated
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Bot is ready.')


@bot.event
async def on_message(message):
    """
    On 'hi' message, replies 'Hey! {username}'
    """
    if message.author == bot.user:
        return
    if message.content.lower() == "hi":
        await message.channel.send(f'Hey! {message.author.name}')
    await bot.process_commands(message)


async def db_query(author, string, recent=False):
    '''
    common function to make db queries for both google search and recent queries cases
    whole function is wrapped by decorator 'sync_to_async' to provide asynchronous support to DB query synchronous methods
    '''
    # from searchbot.search.views import get_search_results, get_recent_queries
    loop = asyncio.get_event_loop()
    if not recent:
        # Google Seach case
        result = await loop.run_in_executor(None, get_search_results, author, string)
    else:
        # recent queries case
        result = get_recent_queries(author, string)
    return """{}""".format("\n".join(result))


# !google command
@bot.command()
async def google(ctx, *, keyword=''):
    if not keyword:
        string_urls = 'Please provide search keyword and try again.'
    else:
        string_urls = await db_query(ctx.author.name, keyword)
    await ctx.send(string_urls)


# !recent command
@bot.command()
async def recent(ctx, *, string=''):
    query_strings = await db_query(ctx.author.name, string, True)
    await ctx.send(query_strings)


# main function to run the bot
def main():
    bot.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    main()
