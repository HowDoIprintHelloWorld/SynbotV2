import os
import discord
import time
from discord.utils import get
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

skid_role_id  = 1104393023149834323   #CHANGE THIS!!!!!!!!!!!!!!!!!!
mod_role_id   = 1104374965136011314   #CHANGE THIS!!!!!!!!!!!!!!!!!!
log_channel_id= 1104418931063664730   #CHANGE THIS!!!!!!!!!!!!!!!!!!

try:
  muted = open("muted_users", "r").read().strip().split("\n")
except:
  open("muted_users", "w").write("")
  muted = []

try:
  reps = open("reps", "r").read().strip().split("\n")
except:
  open("reps", "w").write("")
  reps = []

last_rep = []

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

async def help_page(message):
        help_page_text = """
```
_    _ ______ _      _____
| |  | |  ____| |    |  __ \\
| |__| | |__  | |    | |__) |
|  __  |  __| | |    |  ___/
| |  | | |____| |____| |
|_|  |_|______|______|_|

+rep: reply to a message with this command and the user will get +1 reputation.

-rep: Reply to a message with this command and the user will get -1 reputation.

!rep *<user id>: If no user id is provided it displays your own reputation and if one is provided, it displays the users reputation.

!help: Displays this.

!faq: Displays frequently asked questions in here server.
```
      """.strip()
        await message.channel.send(help_page_text)

@bot.event
async def on_message(message):
        ctx = await bot.get_context(message)
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
        "kys",
        "services"
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

        if message.content == "!help":
            await help_page(message)

        elif message.content == "!faq":
            await faq(message)

        elif message.content == "!rep":
            try:
              index_loc = reps.index(str(message.author.id))
              await message.channel.send("The user:" + str(message.author) + " has " + reps[index_loc+1] + " reputation.")
            except:
              await message.channel.send("Username doesn't exist or doesn't have rep yet.")

        elif message.content.startswith("!rep"):
              try:
                index_loc = reps.index(message.content.split("!rep")[1].strip())
                to_rep = int(message.content.split("!rep")[1].strip())
                name = await bot.fetch_user(to_rep)
                await message.channel.send("The user:" + str(name) + " has " + reps[index_loc+1] + " reputation.")
              except:
                await message.channel.send("Username doesn't exist or doesn't have rep yet.")

        elif message.content.startswith("!addrep"):
            to_rep = int(message.content.split("!addrep")[1].strip())
            try:
              index_loc = reps.index(str(message.author.id))
              if int(reps[index_loc+1]) < 5:
                await message.channel.send("You have to have 5 or more rep to give rep.")
                return
            except:
                await message.channel.send("You have to have 5 or more rep to give rep.")
                return

            try:
              index_loc = last_rep.index(message.author.id)
              if time.time() - last_rep[index_loc+1] < 300:
                await message.channel.send("Hold your horses! Only (-/+)1 rep per 5 minutes.")
                return
            except:
              last_rep.append(message.author.id)
              last_rep.append(0)

            if message.author.id == to_rep or to_rep == bot.user.id:
                return
            try:
              user = await bot.fetch_user(to_rep)
              index_loc = reps.index(str(to_rep))
              reps[index_loc+1] = str(int(reps[index_loc+1])+1)
              index_loc = last_rep.index(message.author.id)
              last_rep[index_loc+1] = time.time()
              channel = bot.get_channel(log_channel_id)
              await channel.send("The user " + str(message.author) + " +rep user: " + str(user))
            except Exception as e:
              print(e)
              try:
                name = await bot.fetch_user(to_rep)
                print("Name:" + str(name))
                reps.append(str(to_rep))
                reps.append(str(1))
              except:
                await message.channel.send("The user:" + str(to_rep) + " doesn't exist.")

        elif message.content == "+rep":
            try:
              index_loc = reps.index(str(message.author.id))
              if int(reps[index_loc+1]) < 5:
                await message.channel.send("You have to have 5 or more rep to give rep.")
                return
            except:
                await message.channel.send("You have to have 5 or more rep to give rep.")
                return

            try:
              index_loc = last_rep.index(message.author.id)
              if time.time() - last_rep[index_loc+1] < 300:
                await message.channel.send("Hold your horses! Only (-/+)1 rep per 5 minutes.")
                return
            except:
              last_rep.append(message.author.id)
              last_rep.append(0)

            reply_to = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            if message.author.id == reply_to.author.id or reply_to.author.id == bot.user.id:
                return
            try:
              index_loc = reps.index(str(reply_to.author.id))
              reps[index_loc+1] = str(int(reps[index_loc+1])+1)
              index_loc = last_rep.index(message.author.id)
              last_rep[index_loc+1] = time.time()
              channel = bot.get_channel(log_channel_id)
              await channel.send("The user " + str(message.author) + " +rep user: " + str(reply_to.author) + " reply to message:\n" + str(reply_to.content))
            except:
              reps.append(str(reply_to.author.id))
              reps.append(str(1))

        elif message.content == "-rep":
            try:
              index_loc = reps.index(str(message.author.id))
              if int(reps[index_loc+1]) < 5:
                await message.channels.end("You have to have 5 or more to take rep.")
                return
            except:
                await message.channels.end("You have to have 5 or more to take rep.")
                return

            try:
              index_loc = last_rep.index(message.author.id)
              if time.time() - last_rep[index_loc+1] < 300:
                await message.channel.send("Hold your horses! Only (-/+)1 rep per 5 minutes.")
                return
            except:
              last_rep.append(message.author.id)
              last_rep.append(0)

            reply_to = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            if message.author.id == reply_to.author.id or reply_to.author.id == bot.user.id:
                return
            try:
              index_loc = reps.index(str(reply_to.author.id))
              reps[index_loc+1] = str(int(reps[index_loc+1])-1)
              index_loc = last_rep.index(message.author.id)
              last_rep[index_loc+1] = time.time()
              channel = bot.get_channel(log_channel_id)
              await channel.send("The user " + str(message.author) + " -rep user: " + str(reply_to.author) + " reply to message:\n" + str(reply_to.content))
            except:
              reps.append(str(reply_to.author.id))
              reps.append(str(-1))

        if mod_role_id in [role.id for role in message.author.roles]:
            if message.content.startswith("!modhelp"):
                mod_help_page = """
!unmute userid: Unmute muted user.
!mute userid: Mute a user
                """.strip()
                await message.channel.send(mod_help_page)
            elif message.content.startswith("!unmute"):
                muted.remove(''.join(message.content.split("!unmute")[1:]).strip())
                await message.channel.send("The user \"" + ''.join(message.content.split("!unmute")[1:]).strip() + "\" has been unmuted by the staff!")
            elif message.content.startswith("!mute"):
                muted.append(''.join(message.content.split("!mute")[1:]).strip())
                await message.channel.send("The user \"" + ''.join(message.content.split("!mute")[1:]).strip() + "\" has been muted by staff.")

        if muted != open("muted_users", "rb").read().strip().split(b"\n"):
            open("muted_users", "w").write('\n'.join(muted))
        print(reps)
        print(last_rep)
        if '\n'.join(reps) != open("reps", "r").read().strip().split("\n"):
            open("reps", "w").write('\n'.join(reps))

tok = os.environ['key']
bot.run(tok)
