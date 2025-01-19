import functools

import discord

# ////////////////////////////////////////////////////////////////////////////////////

# ADDONS

import addons.commands.commands as com
FREAKIFY = functools.partial(com.rename, message=None, text="𝓯𝓻𝓮𝓪𝓴𝔂", type=com.RenameType.PREPEND, success="You have been 𝓯𝓻𝓮𝓪𝓴𝓲𝓯𝓲𝓮𝓭, enjoy", failure="I am afraid you are too freaky already" )
WHO = functools.partial(com.random_user, message = None)

import addons.fun.games as games
RUSSIAN_ROULETTE = functools.partial(games.roulette, x=1, y=6, points=20, message=None)
SHOTGUN_ROULETTE = functools.partial(games.roulette, x=1, y=2, points=50, message=None)
GRENADE_ROULETTE = functools.partial(games.roulette, x=1, y=1, points=0, message=None)
NERF_ROULETTE = functools.partial(games.roulette, x=1, y=100, points=1, message=None)
UNOKER = functools.partial(games.unoker, message=None)

import addons.fun.rps as rps
ROCK_PAPER_SCISSORS = functools.partial(rps.rock_paper_scissors, message=None)

import addons.fun.misc as misc
USER_TIMEOUT = functools.partial(misc.user_timeout, message=None, client=None)
NERD = functools.partial(misc.nerd, message=None)
THE_CHEESE_TOUCH = functools.partial(misc.cheese_touch, message=None)
MARRY_ME = functools.partial(misc.marry, message=None)
PEBBLE = functools.partial(misc.pebble, message=None)

# ////////////////////////////////////////////////////////////////////////////////////


# TRIGGER WORDS
triggers = [
    "bot",
    "help",
]

# RESPONSES
responses = {

    # ACTIONS

    ("timeout", "mute") : USER_TIMEOUT,
    "who": WHO,

    ("russian roulette", "revolver") : RUSSIAN_ROULETTE,
    "shotgun" : SHOTGUN_ROULETTE,
    "grenade" : GRENADE_ROULETTE,
    "nerf" : NERF_ROULETTE,

    ('rock', 'paper', 'scissors', 'lizard', 'spock',
     'mouse', 'worm', 'batman', 'snake', 'gun', 'knife',
     'toyota corolla', 'sock', 'human', 'banana', 'airplane',
     'bug', 'computer', 'fork', 'the mediterranean sea', 'shoe',
     'cheeseburger') : ROCK_PAPER_SCISSORS,

    "freak": FREAKIFY,
    "nerd": NERD,
    "touch" : THE_CHEESE_TOUCH,
    "marry me" : MARRY_ME,
    ("pebble", "gift") : PEBBLE,
    ("unoker", "poker") : UNOKER,

    # /////////////////////////////////////////////////////////

    # RESPONSES

    ("hello", "hi", "hey"): "HELLO",
    ("thank you", "thanks", "ty"): ("You are welcome", "You owe me now"),
    "er ": "I barely  know 'er",
    "duck" : discord.File("files/img/example.webp"),


    ("help", "commands") : """
    # COMMANDS:
    **Who** : Pick random user
    **Mute** : timeout random user and self
    **Mute(@)** : timeout @user and self
    
    # GAMES:
    **Roulette(russian, shotgun, grenade, nerf)** : x in y chance to be kicked from server for points
    **Rock, Paper, Scissors, etc** : Self explanatory
    **Unoker(RANK + SUIT)** : Poker with 1 card
    
    # OTHER:
    **Freak** : Freakify self
    **Freak(@)** : Freakify @user
    **Nerd**: NeRD SeLf
    **Nerd(reply)** : NeRD MeSSaGe
    **Touch(@)** : Give somene the cheese touch 
    **Marry me** : Become married (timeout immunity)
    **Pebble** : Check pebble collection
    **Pebble(@)** : Gift someone a pebble for points
    """,


    # /////////////////////////////////////////////////////////

    # DEFAULT

    "" : (
        "Did somebody say my name?",
        "Hello there!",
        "hey"
    )
}
