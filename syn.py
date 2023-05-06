import os
import discord
from discord.utils import get
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

skid_role_id  = 0   #CHANGE THIS!!!!!!!!!!!!!!!!!!
mod_role_id   = 0   #CHANGE THIS!!!!!!!!!!!!!!!!!!
log_channel_id= 0   #CHANGE THIS!!!!!!!!!!!!!!!!!!

try:
  muted = open("muted_users", "r").read().strip().split("\n")
except:
  open("muted_users", "w").write("")
  muted = []

async def faq(message):
        faq_section = """
```
______      ____
|  ____/\   / __ \\
| |__ /  \ | |  | |
|  __/ /\ \| |  | |
| | / ____ \ |__| |
|_|/_/    \_\___\_\\

"Will you hack person X?": NO, we will not hack anybody because:
   1.We're not getting involved with your personal life.
   2.It's illegal.

"Can you hack account X for me?": NO, we will not hack any account because:
   1.It's impossible without an exploit for the actual website that would probably be worth millions or phishing the person.
   2.It's illegal.
   3.It's against the websites TOS.

"How to hack?": There's no "the way" to learn hacking, it's something everybody needs to find themselves. We can teach about a specific subject thought.

"Is X a scam?": How would we know?! Google the brand/company/website and use your common sense.
```
      """.strip()
        await message.channel.send(faq_section)

@bot.event
async def on_message(message):
        words = [
        "dox",
        "dos",
        "deanonymize",
        "swat",
        "spam",
        "bomb",
        "nigger",
        "retard",
        "tranny",
        "click this",
        "carding",
        "free crypto",
        "free money",
        "kill you",
        "kys"
        ]
        if str(message.author.id) in muted:
          await message.delete()
          return

        if skid_role_id in [role.id for role in message.author.roles]:
          for word in words:
              if word in message.content.lower():
                  await message.delete()
                  await message.channel.send("The user \"" + str(message.author) + "\" has been muted for potentially being a skid, and is waiting for staff approval.")
                  muted.append(str(message.author.id))
                  channel = bot.get_channel(log_channel_id)
                  await channel.send("The user " + str(message.author.id) + " sent message which was flagged:\n " + message.content)

        if message.content == "!faq":
            await faq(message)

        if mod_role_id in [role.id for role in message.author.roles]:
            if message.content.startswith("!modhelp"):
                help_page = """
!unmute userid: Unmute muted user.
!mute userid: Mute a user
                """.strip()
                await message.channel.send(help_page)
            elif message.content.startswith("!unmute"):
                muted.remove(''.join(message.content.split("!unmute")[1:]).strip())
                await message.channel.send("The user \"" + ''.join(message.content.split("!unmute")[1:]).strip() + "\" has been unmuted by the staff!")
            elif message.content.startswith("!mute"):
                muted.append(''.join(message.content.split("!mute")[1:]).strip())
                await message.channel.send("The user \"" + ''.join(message.content.split("!mute")[1:]).strip() + "\" has been muted by staff.")

        if muted != open("muted_users", "rb").read().strip().split(b"\n"):
            open("muted_users", "w").write('\n'.join(muted))

tok = os.environ['key']
print(tok)
bot.run(tok)
