import discord, requests
from datetime import datetime as dt
from discord.ext import commands
import config

discord_bot = commands.Bot(command_prefix = config.PREFIX, intents = discord.Intents.default())
discord_bot.remove_command('help')


def log_error(error):
    print(f"\x1b[31m[{dt.now()}] -- {error}\n\x1b[0m")


@discord_bot.tree.error
async def on_command_error(inte: discord.Interaction, error):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await inte.response.send_message("Oh non, malheureux ! Tu n'as pas les permissions pour faire cette action ! Il faut être administrateur.")
    else:
        log_error(error)

@discord_bot.event
async def on_command_error(ctx : commands.Context, error):
    print("on_command_error")
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(f"Je ne connais pas cette commande. Si tu as un trou de mémoire, la commande `/help` est là pour toi !")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.reply("Je n'ai pas les permissions nécessaire à la réalisation de cette commande. Merci de verifier que j'ai bien les permissions administrateur.")
    else:
        log_error(error)


# bot.event
if True:
    @discord_bot.event
    async def on_ready():
        await discord_bot.tree.sync()
        await discord_bot.change_presence(status=discord.Status.online, activity=discord.Game(f""))
        print(f"\x1b[32m{dt.now()} -- Bot EscapIST OK !\x1b[0m")



@discord_bot.tree.command(name="informations", description="Découvre de nombreuses IST !")
@discord.app_commands.describe(ist = "Le nom de l'IST pour laquelle tu veux en apprendre plus.")
@discord.app_commands.choices( ist = [
    discord.app_commands.Choice(name = "Chlamydiae", value = "0"),
    discord.app_commands.Choice(name = "Hépatite B", value = "1"),
    discord.app_commands.Choice(name = "Syphilis", value = "2"),
    discord.app_commands.Choice(name = "VIH / Sida", value = "3"),
])
async def informations(inte : discord.Interaction, ist : discord.app_commands.Choice[str]):
    ist_data = requests.get(url="http://194.9.172.252:10000/api/ist").json()[int(ist.value)]
    embed = discord.Embed(title = ist_data['name'], description=ist_data['description'])

    # j'ai honte c'est degeulasse comme code mais bon pas grave
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


@discord_bot.tree.command(name="add_question", description="Ajouter une question dans le quizz.")
@discord.app_commands.describe(question = "La question à ajouter")
@discord.app_commands.checks.has_permissions(administrator=True)
async def add_question(inte : discord.Interaction, question : str, question_name : str, bonnereponse : str, reponse2 : str, reponse3 : str):
    url = "http://194.9.172.252:10000/api/questions"
    post_data = {
        "question" : {
            "name": question_name,
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
    req = requests.post(url, json = post_data)
    if req.status_code != 200 or req != 201:
        await inte.response.send_message("Ce nom de question est déjà utilisé !")
    else:
        await inte.response.send_message("La question a été ajoutée avec succès !")
@add_question.error
async def on_command_error(inte: discord.Interaction, error):
    if isinstance(error, discord.app_commands.MissingPermissions):
        await inte.response.send_message("Oh non, malheureux ! Tu n'as pas les permissions pour faire cette action ! Il faut être administrateur.")

discord_bot.run(config.TOKEN)
