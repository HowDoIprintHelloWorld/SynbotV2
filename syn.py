import os
import discord
from discord.utils import get

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

async def dmUser(user, message):
  dmChan = user.dm_channel
  if dmChan == None:
    dmChan = await user.create_dm()
  await dmChan.send(message)
  

# To do: Make it log to a certain channel
def log(message):
  with open("data/log.txt", "a", encoding="latin-1") as log:
   log.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]"+message)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


async def getCommand(message):
  commands = {"verify":verify, "check-chall":checkChallenge, "time-out":timeOut}
  if len(message.content) > 1:
    command = message.content[1:].split()[0]
    if command in commands.keys():
      await commands[command](message)


@client.event
async def on_message(message):
  if message.author == client.user:
      return

  if message.content.startswith('!'):
      await getCommand(message)

@client.event
async def on_member_join(member):
  log(f"New member '{str(member.name)}' joined")

@client.event
async def on_member_remove(member):
  log(f"New member '{str(member.name)}' left")

@client.event
async def on_member_update(before, after):
  print("Member updated")
  log(f"Member '{str(before)}' changed to '{str(after)}'")


@client.event
async def on_reaction_add(reaction, user):
  pass

tok = os.environ['key']
client.run(tok)
