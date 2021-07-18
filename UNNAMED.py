import bs4
from discord import embeds
from discord import client
from discord.client import Client
from discord.embeds import Embed#
from selenium import webdriver#
from selenium.webdriver.chrome.options import Options#
from discord.utils import get#
from discord import FFmpegPCMAudio, channel#
from discord.ext import commands # from discord.ext import tasks, commands
from discord.ext import tasks #
import discord #
import asyncio #
import time #
import nacl#
import sys
sys.path.append("C:\\Users\\leegu\\AppData\\Local\\Programs\\Python\\Python38\\Scripts")
from youtube_dl import YoutubeDL#
import random
import datetime #
import os
import re
from dotenv import load_dotenv#
import numpy
import json
import csv

from Class.COVID_FINDER.COVID_FINDER import COVID

bot = commands.Bot(command_prefix='!')
client = discord.Client()
BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN"

user = [] #유저 입력 노래
musictitle = [] #입력된 정보의 노래 제목
song_queue = [] #입력된 정보의 노래 링크
musicnow = [] #현재 출력되는 노래 배열

def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    chromedriver_dir = ".\\Driver\\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir, options = options)
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    
    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()
    
    return music, URL


def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx)) 

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
    else:
        if not vc.is_playing():
            client.loop.create_task(vc.disconnect())

@bot.event
async def on_ready():
    print("=============")
    print(" 실 행 완 료 ")
    print("=============")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("기침"))
    REFRESH_DATA.start(744199524138090501)



@bot.command(aliases = ["zfs", "ㅋㄹㄴ", "zhfhsk"])
async def 코로나(ctx, arg = None):
    RESULT_EMBED = COVID.COVID_CHECK(arg)
    await ctx.send(embed = RESULT_EMBED)



@tasks.loop(seconds = 1)
async def REFRESH_DATA(self):
    TIME_CHECK = COVID.TIME_CHECK()
    if TIME_CHECK == True:
        channel = bot.get_channel(self)
        NOTICE_MSG = await channel.send("현재 데이터를 갱신중입니다.")
        COVID.REFRESH_DATA(TIME_CHECK)
        await NOTICE_MSG.edit(content ="현재 데이터 갱신을 완료하였습니다.")


@bot.command()
async def 테스트(ctx):
    TEXT = "```diff\n- 확진자\n```"
    TEST_EMBED = discord.Embed(title = f"{TEXT}", description = f"{TEXT}")
    await ctx.send(embed = TEST_EMBED)


@bot.command()
async def 추가(ctx,*,msg):
    user.append(msg)
    result, URLTEST = title(msg)
    song_queue.append(URLTEST)
    await ctx.send(result + " 를 재생목록에 추가했담")

@bot.command(aliases = ['del'])
async def 삭제(ctx,*,number):
    try:
        ex =len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number) - 1]
        del musicnow[int(number)-1+ex]

        await ctx.send("대기열이 정상적으로 삭제됐담")
    except:
        if len(list) == 0:
            await ctx.send ("대기열에 노래가 없어 삭제할 수 없담")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록 개수를 벗어났담")
            else:
                await ctx.send("숫자를 입력하람")

@bot.command()
async def 목록(ctx):
    if len(musictitle) == 0:
        await ctx.send("노래가 등록되어 있지 않담")
    else:
        global Text
        Text =""
        for i in range(len(musictitle)):
            Text =Text + "\n" +str(i + 1) + "." + str(musictitle[i])
        await ctx.send(embed = discord.Embed(title ="노래목록",description = Text.strip(), color =0x00ffff))

@bot.command()
async def 초기화(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(embed = discord.Embed(title= "목록초기화", description = """목록이 정상적으로 초기화됬담""", color = 0x00ffff))
    except:
        await ctx.send("아직 아무노래도 등록하지 않았담.") 

@bot.command()
async def 살아나(ctx):
    global vc
    vc = await ctx.message.author.voice.channel.connect()
    await ctx.send("살았따!")

@bot.command()
async def 죽어(ctx):
    try:
        await vc.disconnect()
        await ctx.send("죽었따!")
    except:
        await ctx.send("집이 없어요")

@bot.command()
async def 따라하기(ctx, *, text):
    await ctx.send(embed = discord.Embed(title = '따라하기', description = text, color =0x00ff00))

@bot.command()
async def 링크(ctx, *, url):
    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}
    
    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info =ydl.extract_info(url, download=False)
        URL = info ['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL,**FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + url + "을(를) 재생하고 있담.", color = 0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있담")

@bot.command()
async def 주사위(ctx):
    await ctx.send(f'주사위를 굴린따!\n{random.randint(1,6)}이(가) 나왔따!.')

@bot.command(aliases = ['shfo', 'play', 'ㅔㅣ묘'])
async def 노래(ctx, *, msg):
    
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
                await ctx.send("채널에 당신이 없담")
                

    if not vc.is_playing():
        
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = ".\\Driver\\chromedriver_win32\\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()


        musicnow.insert(0, entireText)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생된담", description = "현재 " + musicnow[0] + "을(를) 재생하고 있담.", color = 0x00ff00))
        
        vc.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS),after =lambda e: play_next(ctx))
    else:   
        user.append(msg)
        result, URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send(embed = discord.Embed(title = "노래목록", description = result + " 를 재생목록에 추가했담",color = 0x00ffff))

@bot.command(aliases = ['멈춰','ㄴ새ㅔ','ajacnj'])
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title = "일시정지", description = musicnow[0] + "을(를) 일시정지 했담", color= 0x00ffff))
    else:
        await ctx.send("지금 노래가 재생되고 있지 않담.")

@bot.command(aliases=['재생','resume'])
async def 다시재생(ctx):
   if not vc.is_playing():
    try:
        vc.resume()
    except:
        await ctx.send("지금 노래가 재생되고 있지 않담.")

@bot.command(aliases=['스탑','tmxkq','skip'])
async def stop(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title = "노래 껏담",description = musicnow[0] + "을(를) 껏담", color = 0x00ffff))
    else:
       await ctx.send("지금 노래가 재생되고 있지 않담.")

@bot.command(aliases = ['now'])
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send("지금은 노래가 재생되고 있지 않담")
    else:
        await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재" + musicnow[0] + "을(를) 재생하고 있담", color = 0x00ffff))

@bot.command()
async def 멜론차트(ctx):
    if not vc.is_playing():
        
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = ".\\Driver\\chromedriver_win32\\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query=멜론차트")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + entireText + "을(를) 재생하고 있담.", color = 0x00ffff))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생되고 있어서 노래를 재생할 수 없담!")

@bot.command()
async def 도움말(ctx):
   await ctx.send(embed = discord.Embed(title='도움말',description="""\n도움말 ->돌정령의 모든 명령어를 볼 수 있담 \n 살아나 -> 돌정령이 자신이 속한 채널로 들어간담 \n 죽어 -> 돌정령이 자신이 속한 채널에서 쫒겨난담(주륵) \n 주사위 -> 1부터 6까지 숫자를 랜덤으로 뽑는담 \n 노래 -> 노래를 재생한담 (노래 대신 [shfo,play,ㅔㅣ묘] 로도 된담)\n이외에도 [목록,추가,삭제,초기화,지금노래,skip,다시재생,일시정지]가 있담 """,color = 0x00ffff))

bot.run(BOT_TOKEN)
