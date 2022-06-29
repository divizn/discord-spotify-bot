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
spotifyLogo = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/512px-Spotify_icon.svg.png"


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
    if results['tracks']['items'] == []:
        embed=discord.Embed(color=0x00cc03)
        embed.set_thumbnail(url=spotifyLogo)
        embed.add_field(name="No results found", value=f"No results found for '{SEARCH_TERM}', please try again and make sure the song name is valid", inline=False)
        await ctx.send(embed=embed)
    #get song name
    songName = results['tracks']['items'][0]['name']
    #gets song image
    imageURL = results['tracks']['items'][0]['album']['images'][0]['url']
    #get artist(s) names
    artistNamesArr = []
    #get song URL
    songURL = results['tracks']['items'][0]['external_urls']['spotify']
    #get popularity index 
    popularityIndex = results['tracks']['items'][0]['popularity']
    #check if song is explicit (true if yes)
    isExplicit = results['tracks']['items'][0]['explicit'] 
    #gets artist(s) names
    for artists in results['tracks']['items'][0]['artists']:
        artistNamesArr.append(artists['name'])
    artistNames = ', '.join(map(str, artistNamesArr))
    embed=discord.Embed(title=songName, url=songURL, color=0x00cc03)
    embed.set_thumbnail(url=imageURL)
    embed.add_field(name="Song name", value=songName, inline=True)
    embed.add_field(name="Artist(s)", value=artistNames, inline=False)
    if isExplicit:
        embed.add_field(name="Explicit?", value="Explicit", inline=False)
    else:
        embed.add_field(name="Explicit?", value="Not Explicit", inline=False)
    embed.add_field(name="Popularity index (0-100):", value=popularityIndex, inline=False)
    await ctx.send(embed=embed)
    return



@bot.command()
#this command shows an artists profile
async def artist(ctx, *args):
    SEARCH_TERM = " ".join(args)
    results = sp.search(q=SEARCH_TERM, type='artist', limit=5)
    if results['artists']['items'] == []:
        embed=discord.Embed(color=0x00cc03)
        embed.set_thumbnail(url=spotifyLogo)
        embed.add_field(name="No results found", value=f"No results found for '{SEARCH_TERM}', please try again and make sure the artist name is valid", inline=False)
        await ctx.send(embed=embed)
    json = results['artists']['items']
    #get artist details
    artistLink = json[0]['external_urls']['spotify']
    artistImage = json[0]['images'][0]['url']
    followers = json[0]['followers']['total']
    genresArr = json[0]['genres']
    if genresArr == []:
        genres = "(No genres specified)"
    else:
        genres = ', '.join(map(str, genresArr))
    popularityIndex = str(json[0]['popularity'])
    artistName = json[0]['name']
    #put details in discord embed
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
    embed=discord.Embed(title="Commands", color=0x00cc03)
    embed.set_thumbnail(url=spotifyLogo)
    embed.add_field(name="Search for a song", value="!song [song name]", inline=False)
    embed.add_field(name="Search for an artist", value="!artist [artist name]", inline=False)
    await ctx.send(embed=embed)


bot.run(bot_token)
