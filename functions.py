from typing import Literal
import discord, asyncio, numpy as np, json, datetime as dt, random, requests, re
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from discord.ext import commands
import setup


def get_json_file(guild_id : int, file: str) -> dict:
    """data/{guild_id}/{file}.json"""
    if file in setup.POSSIBLE_FILES_TYPES:
        with open(f"data/{guild_id}/{file}.json", "r", encoding='utf-8') as f:
            file_content : dict = json.loads(f.read())
        return file_content
    else:
        print("ERROR: Problem with the type of file")


def get_translation(language : Literal['esp', 'fra', 'usa'], command : Literal['help']) -> dict :
    with open(f"translations/{language}.json", "r", encoding='utf-8') as f:
        return json.loads(f.read())[command]


def dump_json_file(guild_id: int, file: str, dump_content: dict):
    """data/{guild_id}/{file}.json"""
    if file in setup.POSSIBLE_FILES_TYPES:
        with open(f"data/{guild_id}/{file}.json", "w+", encoding='utf-8') as f:
            json.dump(obj = dump_content, fp = f, indent = 4)
    else:
        print("ERROR: Problem with the type of file")


def crop_image_circle(img_path : str) : 
    img = Image.open(img_path).convert('RGB')
    height,width = img.size
    lum_img = Image.new('L', [height,width] , 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0,0), (height-1,width-1)], 0, 360, fill = 255, outline = None)
    img_arr = np.asarray(img)
    lum_img_arr = np.asarray(lum_img)
    final_img_arr = np.dstack((img_arr,lum_img_arr))
    res : Image = Image.fromarray(final_img_arr)
    return res


def log_error(error, guild : discord.Guild = None):
    if guild == None:
        log = f"[{dt.datetime.now()}] -- {error}\n"
    else:
        log = f"[{dt.datetime.now()}] - [{guild.name}] - [{guild.id}] -- {error}\n"
    with open("bot.log", "a+") as file:
        file.write(log)
    print(f"\x1b[31m{log}\x1b[0m")