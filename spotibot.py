
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

artist_name = ""
songs = []
amount_of_songs = 0

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
bot = Bot(command_prefix = '!') #sets discord bot prefix to '!'
                             

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Use !song"))
    print(bot.user.name)
    print("bot active")

@bot.command()
async def song(ctx, arg):
    artist_name = arg
    results = sp.search(q=artist_name, type='track', limit=20) #gets artists top 20 tracks
    for track in results['tracks']['items']:
        songs.append(track['name'])
    songToSend = random.choice(songs)
    await ctx.send(songToSend)
    songs.clear()
    return
          


bot.run(bot_token)
