import secrets
import spotipy
import random
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
    results = sp.search(q=SEARCH_TERM, type='track', limit=20) #gets top 20 tracks from search query
    trackNo = random.randint(0,19)
    urlToSend = results['tracks']['items'][trackNo]['external_urls']['spotify']
    await ctx.send(f"You searched: {SEARCH_TERM}\nURL: {urlToSend}")
    return

@bot.command()
async def cmds(ctx):
    await ctx.send("Use !search [SEARCH_TERM] to get a song")
    return




bot.run(bot_token)
