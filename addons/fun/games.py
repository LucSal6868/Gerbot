import discord
import random

from addons.fun import leaderboard
import data.json_manager as json_manager
from PIL import Image


# ////////////////////////////////////////////////////////////////////////////////////

deaths_key = "deaths"
points_key = "points"

def add_points(message: discord.Message, points: int):
    data: dict = json_manager.get_json_var(message.channel.guild.id, points_key) or {}
    data[str(message.author.id)] = data.get(str(message.author.id), 0) + points
    json_manager.set_json_var(message.channel.guild.id, points_key, data)

def reset_points(message: discord.Message):
    data: dict = json_manager.get_json_var(message.channel.guild.id, points_key) or {}
    data[str(message.author.id)] = 0
    json_manager.set_json_var(message.channel.guild.id, points_key, data)

def add_deaths(message: discord.Message, points: int):
    data: dict = json_manager.get_json_var(message.channel.guild.id, deaths_key) or {}
    data[str(message.author.id)] = data.get(str(message.author.id), 0) + points
    json_manager.set_json_var(message.channel.guild.id, deaths_key, data)

# ////////////////////////////////////////////////////////////////////////////////////

# RUSSIAN ROULETTE

roulette_count_points : bool = True
roulette_count_deaths: bool = True
roulette_kick : bool = True
roulette_rejoin : bool = True

async def roulette(x : int, y : int, points : int,  message : discord.Message):
    survived : bool = random.randint(1, y) > x
    text : str = f"{x} in {y} odds..\n"

    if survived:
        text += "# *click*.\n\n"

        # RANDOM VICTORY MESSAGE
        text += random.choice((
            "You live to fight another day.",
            "You survived",
            "You may not be so lucky next time",
            "You win.",
            "You did not die.",
            "You lived, surprisingly",
        )) + "\n"

        if roulette_count_points:
            text += f"{points} points earned"
            #UPDATE POINTS
            add_points(message, points)


    else:
        text += "# *BANG!*\n\n"

        # RANDOM DEATH MESSAGE
        text += f"<@{message.author.id}> " + random.choice((
            "died.",
            "bit the bullet.",
            "pushed their luck",
            "lost",
            "yee'd their last haw",
            "is no longer with us",
        )) + "\n"

        if roulette_count_points: #UPDATE POINTS
            text += f"Points reset to 0"
            reset_points(message)

        if roulette_count_deaths: #UPDATE DEATHS
            add_deaths(message, 1)

        # KICK AND SEND REJOIN MESSAGE
        if roulette_kick:

            #REJOIN
            if roulette_rejoin:
                invite_link = await message.channel.create_invite()
                await message.author.send(f"You died, rejoin:\n{invite_link}")

            #KICK
            try:
                await message.author.kick()
            except:
                text += f"\n*(Cant kick <@{message.author.id}>)*"

    await message.reply(text)

    # UPDATE LEADERBOARD
    if roulette_count_deaths or roulette_count_points:
        await leaderboard.update_leaderboard(message)

# ////////////////////////////////////////////////////////////////////////////////////

# UNOKER
class Card:
    def __init__(self, rank, suit):
        self.rank : str = rank
        self.suit : str = suit
suits = ['heart', 'diamond', 'spade', 'club']
ranks = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
deck = []

cards_drawn : int = 4
card_images_folder : str = "files/img/cards"
cards_points_enabled : bool = True

poker_hand_points = {
    'none' : -10,
    'Pair' : 0,
    'Two Pair' : 50,
    'Three of a Kind' : 50,
    'Straight' : 100,
    'Flush' : 100,
    'Full House' : 200,
    'Four of a Kind' : 250,
    'Straight Flush': 500,
    'Royal Flush' : 5000
}


def evaluate_hand(ranks_dict, suits_dict, play):
    is_flush = any(count == 5 for count in suits_dict.values())
    rank_indices = [ranks.index(card.rank) for card in play]
    rank_indices.sort()
    is_straight = all(rank_indices[i] + 1 == rank_indices[i + 1] for i in range(len(rank_indices) - 1))

    if is_flush and is_straight:
        if {'ten', 'jack', 'queen', 'king', 'ace'}.issubset([card.rank for card in play]):
            return 'Royal Flush'
        return 'Straight Flush'

    if 4 in ranks_dict.values():
        return 'Four of a Kind'
    if 3 in ranks_dict.values() and 2 in ranks_dict.values():
        return 'Full House'
    if is_flush:
        return 'Flush'
    if is_straight:
        return 'Straight'
    if 3 in ranks_dict.values():
        return 'Three of a Kind'
    if list(ranks_dict.values()).count(2) == 2:
        return 'Two Pair'
    if 2 in ranks_dict.values():
        return 'Pair'

    return 'none'

async def unoker(message : discord.Message):
    if len(deck) < cards_drawn:
        deck.clear()
        new_deck = [Card(rank, suit) for rank in ranks for suit in suits]
        deck.extend(new_deck)

    player_suit = next((item for item in suits if item in message.content.lower()), None)
    player_rank = next((item for item in ranks if item in message.content.lower()), None)

    if not player_rank or not player_suit:
        await message.reply("Pick a rank and suit to play!\n(Ace of hearts, ten of spades, etc)")
        return

    hand : list = random.sample(deck, cards_drawn)
    for card in hand:
        deck.remove(card)

    play : list = hand + [Card(player_rank, player_suit)]

    # POKER HANDS
    suits_dict = {suit: 0 for suit in suits}
    ranks_dict = {rank: 0 for rank in ranks}
    for card in play:
        suits_dict[card.suit] += 1
        ranks_dict[card.rank] += 1

    hand_type = evaluate_hand(ranks_dict, suits_dict, play)
    hand_points = poker_hand_points[hand_type]

    text : str = "PLAYING UNOKER:\n"
    text += f"# {hand_type}\n"
    text += f"You earned : {hand_points} Points"

    # SORT
    suit_order = {'heart': 1, 'diamond': 2, 'spade': 3, 'club': 4}  # Define suit order
    rank_order = {rank: index for index, rank in enumerate(ranks)}  # Define rank order
    hand = sorted(hand, key=lambda c: (suit_order[card.suit], rank_order[card.rank]))

    # CREATE HAND IMAGE
    card_files = []
    for card in hand:
        card_files.append(card_images_folder + '/'+ card.suit + "_" + card.rank + ".png")
    card_files.append(card_images_folder + "/plus.png")
    card_files.append(card_images_folder + '/' + player_suit + "_" + player_rank + ".png")

    width, height = Image.open(card_images_folder + '/empty.png').size
    cards_img = [Image.open(card_file).resize((width, height)) for card_file in card_files]
    combined_image = Image.new('RGBA', (width * (cards_drawn + 2), height))
    for i, card_img in enumerate(cards_img):
        combined_image.paste(card_img, (i * width, 0))

    combined_image.save(card_images_folder + '/a.png')
    add_points(message, hand_points)
    try:
        await leaderboard.update_leaderboard(message)
        await message.reply(text, file=discord.File(card_images_folder + '/a.png'))
    except:
        pass



# ////////////////////////////////////////////////////////////////////////////////////

# SHOP

# SHIP

# FISH

# ////////////////////////////////////////////////////////////////////////////////////