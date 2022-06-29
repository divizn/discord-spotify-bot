from pydoc import cli
import secrets
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from secrets import client_id, client_secret, bot_token
import discord
from discord.ext.commands import Bot

bot_token = secrets.bot_token
client_id = secrets.client_id
client_secret = secrets.client_secret #sets discord bot token, spotify app client id and client secrets 


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
bot = Bot(command_prefix = '!') #sets discord bot prefix to '!'
                             

@bot.event
#when bot starts (on_ready), presence of the bot is changed to "Use !cmds" and it shows when the bot is active in the terminal
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Use !cmds"))
    print(bot.user.name+" is active")

@bot.command()
#*args takes in the arguments passed to the bot (e.g. !search lil uzi will take lil and uzi) and then this method will return 5 songs from the arguments
async def song(ctx, *args):
    SEARCH_TERM = " ".join(args) #turns the args into a search term to be used 
    results = sp.search(q=SEARCH_TERM, type='track', limit=5) #gets top 5 tracks from search query
    urlsToSend = "First 5 results:"
    for item in results['tracks']['items']:
         urlsToSend += "\n"+item['external_urls']['spotify']
    if urlsToSend == "First 5 results:":
        await ctx.send(f"No results for {SEARCH_TERM}") #error handling for when there are no args
    else:
        await ctx.send(f"You searched for: {SEARCH_TERM}\n"+urlsToSend)
    return

@bot.command()
#this command shows an artists profile
async def artist(ctx, *args):
    SEARCH_TERM = " ".join(args)
    results = sp.search(q=SEARCH_TERM, type='artist', limit=5)
    if results['artists']['items'] == []:
        await ctx.send(f"No results for {SEARCH_TERM}")  #check if no artists
    json = results['artists']['items']
    artistLink = json[0]['external_urls']['spotify']
    artistImage = json[0]['images'][0]['url']
    followers = json[0]['followers']['total']
    genresArr = json[0]['genres']
    genres = ', '.join(map(str, genresArr))
    popularityIndex = str(json[0]['popularity'])
    artistName = json[0]['name']
    embed=discord.Embed(title=artistName, url=artistLink, color=0x00cc03)
    embed.set_thumbnail(url=artistImage)
    # embed.add_field(name=artistName, value=artistLink, inline=False)
    embed.add_field(name="Follower count:", value=followers, inline=False)
    embed.add_field(name="Genres:", value=genres, inline=True)
    embed.add_field(name="Popularity index (0-100):", value=popularityIndex, inline=False)
    await ctx.send(embed=embed)
    


@bot.command()
#this command shows the list of commands when !cmds is typed
async def cmds(ctx):
    await ctx.send("Use !song <search-tag> to get a song\nUse !artist <search-tag> to get an artist")
    return


bot.run(bot_token)
