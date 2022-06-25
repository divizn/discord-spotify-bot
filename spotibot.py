import secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from secrets import client_id, client_secret, bot_token
import discord
from discord.ext.commands import Bot

bot_token = secrets.bot_token
client_id = secrets.client_id
client_secret = secrets.client_secret #sets spotify app client id and client secrets


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
bot = Bot(command_prefix = '!') #sets discord bot prefix to '!'
                             

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Use !cmds"))
    print(bot.user.name+" is active")

@bot.command()
async def search(ctx, *args):
    SEARCH_TERM = " ".join(args)
    results = sp.search(q=SEARCH_TERM, type='track', limit=5) #gets top 5 tracks from search query
    urlToSend = "First 5 results:"
    for item in results['tracks']['items']:
         urlToSend += "\n"+item['external_urls']['spotify']
    if urlToSend == "First 5 results:":
        await ctx.send("No results")
    else:
        await ctx.send(f"You searched for: {SEARCH_TERM}\n"+urlToSend)
    return

@bot.command()
async def cmds(ctx):
    await ctx.send("Use !search [SEARCH_TERM] to get a song")
    return

bot.run(bot_token)