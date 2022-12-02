import discord, datetime as dt, os, requests, json
from typing import Literal
from discord.ext import commands
import config, functions

if os.name == 'nt':
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)

intents : discord.Intents = discord.Intents.default()
intents.message_content = True
intents.members = True

discord_bot = commands.Bot(command_prefix = config.PREFIX, intents = intents)
discord_bot.remove_command('help')
tree = discord_bot.tree


# @tree.error
# async def on_command_error(inte: discord.Interaction, error):
#     if isinstance(error, discord.app_commands.MissingPermissions):
#         await inte.response.send_message("Oh non, malheureux ! Tu n'as pas les permissions pour faire cette action ! Il faut être administrateur.")
#     else:
#         functions.log_error(error)


# @discord_bot.event
# async def on_command_error(ctx : commands.Context, error):
#     print("on_command_error")
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.reply(f"Je ne connais pas cette commande. Si tu as un trou de mémoire, la commande `/help` est là pour toi !")
#     elif isinstance(error, commands.BotMissingPermissions):
#         await ctx.reply("Je n'ai pas les permissions nécessaire à la réalisation de cette commande. Merci de verifier que j'ai bien les permissions administrateur.")
#     else:
#         functions.log_error(error)


# bot.event
if True:
    @discord_bot.event
    async def on_ready():
        await tree.sync()
        await tree.sync(guild = discord.Object(config.SUPREM_GUILD_ID))
        await discord_bot.change_presence(status=discord.Status.online, activity=discord.Game(f"faut_trouver_un_nom.fr"))
        print(f"\x1b[32m{dt.datetime.now()} -- Bot Nuit de l'info OK\x1b[0m")


    @discord_bot.event
    async def on_guild_join(guild : discord.Guild):
        channel : discord.TextChannel = guild.public_updates_channel if guild.public_updates_channel != None else guild.text_channels[0]
        await channel.send(f"Merci de m'avoir ajouté au serveur ! Avec moi tout est possible, ou presque. La commande `/help` regorge de choses intéressantes !\n")
        print(f"{dt.datetime.now()} -- Guild join : {guild.name} / {guild.member_count} membres")


    @discord_bot.event
    async def on_guild_remove(guild : discord.Guild):
        suprem_channel : discord.TextChannel = discord_bot.get_channel(config.SUPREM_CHANNEL_ID)
        await suprem_channel.send(content = f"LEFT [{guild.name}] - [{guild.id}] - [{guild.member_count} membres]")


    @discord_bot.event
    async def on_message(message : discord.Message):
        if (message.content == "" and message.attachments == []) or message.author.bot == True: #c'est pour les messages system et trucs du genre
            return
        await discord_bot.process_commands(message)




@tree.command(name="informations", description="Découvre de nombreuses IST !")
@discord.app_commands.describe(ist = "Le nom de l'IST pour laquelle tu veux en apprendre plus.")
@discord.app_commands.choices( ist = [
    discord.app_commands.Choice(name = "Chlamydiae", value = "0"),
    discord.app_commands.Choice(name = "Hépatite B", value = "1"),
    discord.app_commands.Choice(name = "Syphilis", value = "2"),
    discord.app_commands.Choice(name = "VIH / Sida", value = "3"),
])
@discord.app_commands.checks.has_permissions(administrator=True)
async def informations(inte : discord.Interaction, ist : discord.app_commands.Choice[str]):
    ist_data = functions.get_json("ist_infos.json")[int(ist.value)]
    # ist_data = requests.get(url="http://194.9.172.252:10000/api/ist").json()[int(ist.value)]
    embed = discord.Embed(title = ist_data['name'], description=ist_data['description'])

    if 'transmission' in ist_data.keys() and ist_data['transmission'] != None:
        embed.add_field(name = "Transmission", value = "・" + '\n・'.join(ist_data['transmission']))
    if 'symptoms' in ist_data.keys() and ist_data['symptoms'] != None:
        embed.add_field(name = "Symptômes", value = "・" + '\n・'.join(ist_data['symptoms']))
    if 'risks' in ist_data.keys() and ist_data['risks'] != None:
        embed.add_field(name = "Conséquences", value = "・" + '\n・'.join(ist_data['risks']))
    if 'incubation_time' in ist_data.keys() and ist_data['incubation_time'] != "":
        embed.add_field(name = "Temps d'incubation", value = ist_data['incubation_time'])
    if 'treatments' in ist_data.keys() and ist_data['treatments'] != None:
        embed.add_field(name = "Traitements", value = "・" + '\n・'.join(ist_data['treatments']))
    if 'affected_pop' in ist_data.keys() and ist_data['affected_pop'] != None:
        embed.add_field(name = "Population touchée", value = "・" + '\n・'.join(ist_data['affected_pop']), inline = False)
    if 'stats' in ist_data.keys() and ist_data['stats'] != None:
        embed.add_field(name = "Statistiques", value = "・" + '\n・'.join(ist_data['stats']))

    await inte.response.send_message(embed = embed)






@tree.command(name="add_question", description="Ajouter une question dans le quizz.")
@discord.app_commands.describe(question = "La question à ajouter")
@discord.app_commands.checks.has_permissions(administrator=True)
async def add_question(inte : discord.Interaction, question : str, bonnereponse : str, reponse2 : str, reponse3 : str):
    url = "http://194.9.172.252:10000/api/questions"
    post_data = {
        "question" : {
            "name": "test",
            "type": "question",
            "ageRange": "adulte",
            "content": question,
            "hintLabel": "Aide",
            "hintContent": ""
        },
        "responses": [
        {
            "score": 1,
            "content": bonnereponse
        },
        {
            "score": 0,
            "content": reponse2
        },
        {
            "score": 0,
            "content": reponse3
        }
    ]
    }
    requests.post(url, json = post_data)



    await inte.response.send_message("La question a été ajoutée avec succès !")





discord_bot.run(config.TOKEN)