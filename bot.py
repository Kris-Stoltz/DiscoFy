import discord
from discord.ext import commands
from playlist import Playlist
import youtube_dl
import random

playlist = Playlist()


class Bot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.index = 0
        self.sources = []
        self.is_paused = False
        self.current_song = None

    def get_next(self):
        if self.index == len(self.sources):
            self.index = 0
        else:
            self.index += 1

    @commands.command(help='Connects the bot to your current voice channel.')
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send('You\'re not in a voice channel!')
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(help='Disconnects the bot from your current voice channel.')
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        self.sources = []

    @commands.command(help='Pauses any current music being played by the bot.')
    async def pause(self, ctx):
        vc = ctx.voice_client
        if vc.is_playing():
            vc.pause()
            self.is_paused = True
            await ctx.send('Discofy is paused ⏸️')

    @commands.command(help='Resumes any current music being played by the bot.')
    async def resume(self, ctx):
        vc = ctx.voice_client
        if not vc.is_playing():
            vc.resume()
            self.is_paused = False
            await ctx.send('Discofy is playing ▶️')

    @commands.command(help='Skips the current song being played by the bot.')
    async def skip(self, ctx):
        vc = ctx.voice_client
        vc.stop()
        await self.play(ctx)

    @commands.command(help='Shuffles the current playlist.')
    async def shuffle(self, ctx):
        self.current_song = self.sources[self.index-1]["title"]
        random.shuffle(self.sources)
        await ctx.send('Shuffling playlist 🔀')

    @commands.command(help='Returns the song name of the song currently being played.')
    async def song(self, ctx):
        if self.current_song is None:
            await ctx.send(f'Currently playing: **{self.sources[self.index -1 ]["title"]}**')
        else:
            await ctx.send(f'Currently playing: **{self.current_song}**')
            self.current_song = None

    @commands.command(help='Plays the current playlist(requires you to add a playlist, try ">help add").')
    async def play(self, ctx):
        vc = ctx.voice_client

        def play_song(error=None):
            if not self.is_paused:
                if not vc.is_playing():
                    vc.play(self.sources[self.index]['data'], after=play_song)
                    self.get_next()
        play_song()

    @commands.command(help='Add a spotify playlist, by typing >add and copying a spotify playlist link.')
    async def add(self, ctx, url):
        playlist.get_playlist(url)
        ffmpeg_opt = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}
        ydl_opt = {'format': 'bestaudio'}

        vc = ctx.voice_client
        self.index = 0
        self.sources = []

        for song in playlist.songs:
            with youtube_dl.YoutubeDL(ydl_opt) as ydl:
                info = ydl.extract_info(f'ytsearch:{song}', download=False)['entries'][0]
                url_2 = info['formats'][0]['url']
                source = {"data": await discord.FFmpegOpusAudio.from_probe(url_2, **ffmpeg_opt),
                          'title': info['title']}
                self.sources.append(source)
                if not vc.is_playing():
                    await self.play(ctx)


def setup(client):
    client.add_cog(Bot(client))

