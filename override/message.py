from discord import Intents, Client, File
from dotenv import load_dotenv
import os

intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents = intents)

load_dotenv()
TOKEN = str(os.getenv('DISCORD_TOKEN'))

ch_id = 1272961650009575536
msg : str = ""

@client.event
async def on_ready()->None:
    channel = client.get_channel(ch_id)

    #await channel.send(msg)
    await channel.send(file = File("hereturned.jpg"))
    await client.close()

def main()->None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()


