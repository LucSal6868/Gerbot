import discord
import random
import re
import datetime
import sys

import data.json_manager as json_manager
from addons.fun import games
from addons.fun import leaderboard

# ////////////////////////////////////////////////////////////////////////////////////

# MARRY ME

spouse_role : str

async def marry(message : discord.Message):

    role = discord.utils.get(message.guild.roles, name=spouse_role)
    if role is None:
        role = await message.guild.create_role(name=spouse_role, color=discord.Color.from_rgb(255,182,193), hoist=True)

    if role in message.author.roles:
        await message.reply("Give someone else a chance")
        return

    try:
        for m in role.members:
            await m.remove_roles(role)

        await message.author.add_roles(role)

        await message.reply(f"<@{message.author.id}> and I are now happily married!")

    except:
        await message.reply(f"Nah")

# ////////////////////////////////////////////////////////////////////////////////////

# TIMEOUT

timeout_exceptions = []
timeout_ignore_spouse : bool
timeout_exception_message : str

timeout_random_range = (1, 3)
timeout_targeted_range = (5, 8)
timeout_self_target_time : int
timeout_multiplier : int

async def user_timeout(message : discord.Message, client : discord.Client):

    match = re.search(r'<@(\d+)>', message.content.lower())

    if not match: # RANDOM MUTE

        all_users = message.channel.guild.members
        random_user = random.choice(all_users)
        random_num: int = random.randint(timeout_random_range[0], timeout_random_range[1])
        random_num_multiplied = random_num * timeout_multiplier

        # TIMEOUT RANDOM USER
        try:
            await random_user.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=random_num), reason="bad luck")
            await message.channel.send(f"Random user <@{random_user.id}> has been muted for {random_num} minutes.")
        except:
            await message.channel.send(f"<@{random_user.id}>, CANNOT BE MUTED")
            print("Cannot mute target")
            sys.stdout.flush()

        # TIMEOUT AUTHOR
        try:
            await message.author.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=random_num_multiplied), reason=f"YOU DID THIS TO YOURSELF")
            await message.channel.send(f"In exchange <@{message.author.id}> has been muted for {random_num_multiplied} minutes")
        except:
            print("Cannot mute author")
            sys.stdout.flush()

    else: # TARGETED MUTE

        target_user = await message.channel.guild.fetch_member(match.group(1))
        random_num: int = random.randint(timeout_targeted_range[0], timeout_targeted_range[1])
        random_num_multiplied: int = random_num * timeout_multiplier

        if timeout_ignore_spouse:
            married_role = discord.utils.get(message.guild.roles, name=spouse_role)
            if married_role in target_user.roles:
                await message.reply("I WOULD NEVER DO THAT TO MY SPOUSE")
                return


        # TARGET IS SUICIDAL
        if target_user.id == message.author.id:
            try:
                await message.channel.send(f"Dude are u ok???\n<@{message.author.id}> has been muted for {timeout_self_target_time} minutes" )
                await message.author.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=timeout_self_target_time), reason=f"Self harm")
            except:
                print("Cannot mute author")
                sys.stdout.flush()

        # TARGET IS EXCEPTION OR BOT
        elif target_user.id  in timeout_exceptions and client.user.id  in timeout_exceptions:
            try:
                await message.author.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=random_num_multiplied), reason=f"YOU DID THIS TO YOURSELF")
                await message.channel.send(f"NICE TRY STUPID\n<@{message.author.id}> has been muted for {random_num_multiplied} minutes")
            except:
                print("Cannot mute author")
                sys.stdout.flush()

        # NORMAL TARGETED TIMEOUT
        else:

            # TIMEOUT TARGET
            try:
                await target_user.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=random_num), reason=f"<@{message.author.id}>")
                await message.channel.send(
                    f"<@{target_user.id}> has been muted for {random_num} minutes")
            except:
                await message.channel.send(f"<@{target_user.id}>, CANNOT BE MUTED")
                print("Cannot mute target")
                sys.stdout.flush()

            #TIMEOUT AUTHOR
            try:
                await message.author.timeout(discord.utils.utcnow() + datetime.timedelta(minutes=random_num_multiplied), reason=f"YOU DID THIS TO YOURSELF")
                await message.channel.send(
                    f"In exchange <@{message.author.id}> has been muted for {random_num_multiplied} minutes")
            except:
                print("Cannot mute author")
                sys.stdout.flush()


# ////////////////////////////////////////////////////////////////////////////////////

# NERD
async def nerd(message : discord.Message):
    text: str
    if message.reference:
        reference = await message.channel.fetch_message(message.reference.message_id)
        text = ''.join(random.choice([c.lower(), c.upper()]) for c in reference.content)
    else:
        text: str = ''.join(random.choice([c.lower(), c.upper()]) for c in message.content)

    await message.channel.send("\"" + text + "\" - :nerd:")

# ////////////////////////////////////////////////////////////////////////////////////

# CHEESE TOUCH

cheese_touch_role : str

async def cheese_touch(message : discord.Message):
    target : discord.Member = None
    match = re.search(r'<@(\d+)>', message.content.lower())
    if match:
        target = await message.channel.guild.fetch_member(match.group(1))

    # NO TARGET FOUND
    if not target:
        await message.channel.send("@someone to target them with the cheese touch")
        return

    if target.bot:
        await message.reply("I'm afraid I can't do that, Dave")
        return

    if target.id == message.author.id:
        await message.reply("????????? is this how you get you sick kicks?????")
        return


    # CREATE ROLE IF IT DOES NOT EXIST
    role = discord.utils.get(message.guild.roles,name=cheese_touch_role)
    if role is None:
        role = await message.guild.create_role(name=cheese_touch_role, color=discord.Color.gold(), hoist=True)

    # IF ROLE EMPTY, OR USER HAS ROLE, TOUCH CHEESE
    if role in message.author.roles or len(role.members) <= 0:

        # add role to touched
        try:
            await target.add_roles(role)
            await message.channel.send(f"<@{target.id}> NOW HAS THE CHEESE TOUCH. EVERYONE SOCIALLY ISOLATE THEM")

            try:
                await message.author.remove_roles(role)
            except:
                await message.reply(f"If you are reading this message, you still have the touch for some reason")
        except:
            await message.reply(f"IDK why but they are immune to the cheese touch")

    # IF USER DOES NOT HAVE ROLE FAIL
    else:
        await message.reply(f"you do not have the cheese touch my friend")


# ////////////////////////////////////////////////////////////////////////////////////

# PEBBLE

pebble_key : str
pebble_key_count_key : str
pebbles_have_cost : bool
pebble_cost : int

pebble_types = {
    'Common': ["blue_circle", "red_circle", "yellow_circle", "green_circle", "purple_circle"],
    'Rare': ["large_blue_diamond", "small_blue_diamond", "large_orange_diamond", "small_red_triangle_down", "small_red_triangle"],
    'Square': ["blue_square", "red_square", "yellow_square", "green_square", "purple_square"],
    'Heart': ["blue_heart", "red_heart", "yellow_heart", "green_heart", "purple_heart"],
    'Ball': ["yarn", "softball", "yo_yo", "tennis", "crystal_ball"],
    'Fruit': ["blueberries", "lemon", "apple", "kiwi", "grapes"],
    'Animal': ["jellyfish", "hatched_chick", "crab", "snake", "bug"],
    'Legendary': ["gem", "coin", "dollar"],
    'WHITE': ["white_circle", "white_large_square", "white_heart", "egg", "mouse2"],
    'BLACK': ["black_circle", "black_large_square", "black_heart", "8ball", "black_cat"]
}
pebble_weights= {
    'Common': 100,
    'Rare': 25,
    'Square': 10,
    'Heart': 10,
    'Ball': 10,
    'Fruit': 10,
    'Animal': 10,
    'Legendary': 5,
    'WHITE': 2,
    'BLACK': 1,
}
total_weight = sum(pebble_weights.values())

def get_pebble() -> str:
    chosen_category = random.choices(
        population=list(pebble_weights.keys()),
        weights=list(pebble_weights.values()),
        k=1)[0]
    #result : str = random.choice(pebble_types[chosen_category])
    result : str = pebble_types[chosen_category][random.randint(0, len(pebble_types[chosen_category]) - 1)]
    return result

async def pebble(message : discord.Message):
    target : discord.Member = None

    match = re.search(r'<@(\d+)>', message.content.lower())
    if match:
        target = await message.channel.guild.fetch_member(match.group(1))

    # NO TARGET FOUND
    if not target:
        data: dict = json_manager.get_json_var(message.channel.guild.id, pebble_key) or {}
        user_pebbles : dict = data.get(str(message.author.id), {})
        text = f"\n\nCOLLECTION:\n\n"

        for key in pebble_types.keys():
            if key == pebble_key_count_key:
                continue

            if set(pebble_types[key]) & set(user_pebbles):
                text += f"**{key.upper()}** : \n"
            else:
                text += f"UNDISCOVERED : \n"

            # LIST PEBBLES
            for pebb in pebble_types[key]:
                peb_count = user_pebbles.get(pebb, 0)
                if peb_count != 0:
                    text += f"| :{pebb}: = {peb_count} "
                else:
                    text += f"| :grey_question: "
            text += "\n"


        text += "\n@someone to gift them a pebble!\n"

        await message.channel.send(text)
        return

    # TARGET IS SELF
    if target.id == message.author.id:
        await message.reply("This is sad to watch")
        return

    # CHARGE FOR PEBBLE
    if pebbles_have_cost:
        data: dict = json_manager.get_json_var(message.channel.guild.id, games.points_key) or {}
        user_points = data.get(str(message.author.id), 0) - pebble_cost

        if user_points < 0:
            try:
                await message.reply(f"YOU ARE TOO POOR.\n\nTHE PRICE OF A PEBBLE IS {pebble_cost} POINTS")
            except:
                pass
            return

        data[str(message.author.id)] = user_points
        json_manager.set_json_var(message.channel.guild.id, games.points_key, data)

    # ADD PEBBLE TO SAVE FILE
    new_pebble : str = get_pebble()

    data: dict = json_manager.get_json_var(message.channel.guild.id, pebble_key) or {}
    target_pebbles = data.get(str(target.id), {})
    target_pebbles[new_pebble] =  target_pebbles.get(new_pebble, 0) + 1
    target_pebbles[pebble_key_count_key] =  target_pebbles.get(pebble_key_count_key, 0) + 1
    data[str(target.id)] = target_pebbles
    json_manager.set_json_var(message.channel.guild.id, pebble_key, data)

    try:
        await message.channel.send(f"<@{message.author.id}> gifted <@{target.id}> a pebble for {pebble_cost} points!\
                                   \n\n:{new_pebble}: added to <@{target.id}>'s collection!")
        await leaderboard.update_leaderboard(message)

    except:
        pass

# ////////////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////////////////////////