import re, os, asyncio, html, logging
from telethon import TelegramClient, events, Button, functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import pack_bot_file_id as lolpic


logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

try:
  BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
  APP_ID = int(os.environ.get("APP_ID", 6))
  API_HASH = os.environ.get("API_HASH", None)
  OWNER_ID = int(os.environ.get("OWNER_ID", None))
  CHANNEL = os.environ.get("CHANNEL")
  
  alain = TelegramClient('alain', APP_ID, API_HASH).start(bot_token=BOT_TOKEN)

  
  print('Processing....')
except Exception as e:
  print(f"ERROR\n{str(e)}")

async def check(ch, event, xD):
    try:
            sed = await xD(functions.channels.GetParticipantRequest(channel=ch, user_id=event.sender_id))
            if sed.participant:
                return True
    except telethon.errors.rpcerrorlist.UserNotParticipantError:
        return False
      
@alain.on(events.NewMessage(pattern="[/!?=$-~.|}](start|START|Start)$"))
async def startkaru(event):
  but = [[Button.inline('Groups.', data="link")]]
  if event.is_private:
    return await event.reply(f'**Hey** **[{event.sender.first_name}](tg://user?id={event.sender.id})!**\n**Nice to see you here..!\nSorry but i only works in osmani network..:)\n\nWill see you there!😉**', buttons=but)
  chat = [-1001363684870]
  if event.chat_id in chat:
    sedkk = [[Button.inline('Groups.', data="del")]]
    await event.reply(f"**Hey** **[{event.sender.first_name}](tg://user?id={event.sender.id})!**\n**I'm Osmani assistant who works for osmani network...!**", buttons=sedkk)
  else:
    await alain.delete_dialog(event.chat_id)
  
@alain.on(events.callbackquery.CallbackQuery(data="link"))
async def links(event):
  tf = [[Button.url('✘ Support ✘', 't.me/osmanigroupbot'), Button.url('✘ Owner ✘', 't.me/ribajosmani')]]
  tf += [[Button.url('✘ Updates ✘', 't.me/teamosmani'), Button.inline('Back', data='pback')]]
  await event.edit('**Here are all the links of osmani network...!**', buttons=tf)
  
@alain.on(events.callbackquery.CallbackQuery(data="del"))
async def links(event):
  tf = [[Button.url('✘ Support ✘', 't.me/osmanigroupbot'), Button.url('✘ Owner ✘', 't.me/ribajosmani')]]
  tf += [[Button.url('✘ Updates ✘', 't.me/teamosmani'), Button.inline('Close', data='delll')]]
  await event.edit('**Here are all the links of osmani network...!**', buttons=tf)
  
  
@alain.on(events.callbackquery.CallbackQuery(data="delll"))
async def links(event):
  await event.delete()
  
@alain.on(events.callbackquery.CallbackQuery(data="pback"))
async def pbak(event):
  but = [[Button.inline('Groups.', data="link")]]
  await event.edit(f'**Hey** **[{event.sender.first_name}](tg://user?id={event.sender.id})!**\n**Nice to see you here..!\nSorry but i only works in osmani network..:)\n\nWill see you there!😉**', buttons=but)

  
from telethon import events
import re, os
import asyncio
import traceback
import io
import os
import sys
import time
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *
from telethon.errors import *

bot = alain
#

async def aexec(code, event):
    exec(
        f'async def __aexec(event): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](event)

@bot.on(events.NewMessage(pattern="/eval"))
async def _(event):
    if event.sender.id == OWNER_ID:
        pass
    else:
        return
    cmd = event.text.split(" ", maxsplit=1)[1]
    cmd = event.text.split(" ", maxsplit=1)[1] 
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Sᴜᴄᴄᴇss"
    final_output = "**Eᴠᴀʟ:**\n`{}`\n\n**Oᴜᴛᴘᴜᴛ:**\n`{}`".format(cmd,evaluation)
    MAX_MESSAGE_SIZE_LIMIT = 4095
    if len(final_output) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await bot.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id,
            )

    else:
        await event.reply(final_output)




from os import remove, execle, path, environ
import asyncio
import sys
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
import heroku3
tbot = bot


UPSTREAM_REPO_URL = "https://github.com/Ribaj"
HEROKU_APP_NAME = None
HEROKU_API_KEY = None

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"•[{c.committed_datetime.strftime(d_form)}]: {c.summary} by <{c.author}>\n"
        )
    return ch_log


async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@bot.on(events.NewMessage(pattern="^/update(?: |$)(.*)"))
async def upstream(ups):
    if event.sender.id == OWNER_ID:
        pass
    else:
        return await event.reply("**• Go away nibba •**")
    
    check = ups.message.sender_id
    
    lol = await ups.reply("`Checking for updates, please wait....`")
    conf = ups.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    

    try:
        txt = "`Oops.. Updater cannot continue "
        repo = Repo()
    except NoSuchPathError as error:
        await lol.edit(f"{txt}\n`directory {error} is not found`")
        repo.__del__()
        return
    except GitCommandError as error:
        await lol.edit(f"{txt}\n`Early failure! {error}`")
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            pass
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != "master":
        await lol.edit(
            f"**[UPDATER]:**` Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "please checkout to any official branch`"
        )
        repo.__del__()
        return

    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")

    if not changelog and not force_update:
        await lol.edit("\n`Your bot is`  **up-to-date**  \n")
        repo.__del__()
        return

    if conf != "now" and not force_update:
        changelog_str = (
            f"**New update available available 🇸🇴\n\n{ac_br}\n\nChangelog:**\n`{changelog}`"
        )
        if len(changelog_str) > 4096:
            await lol.edit("`Changelog is too big, view the file to see it.`")
            file = open("output.txt", "w+")
            file.write(changelog_str)
            file.close()
            await tbot.send_file(
                ups.chat_id,
                "output.txt",
                reply_to=ups.id,
            )
            remove("output.txt")
        else:
            await lol.edit(changelog_str)
        await ups.respond("**Do `/update now` **to update your bot 🇸🇴**")
        return

    if force_update:
        await lol.edit("`Force-Syncing to latest master bot code, please wait...`")
    else:
        await lol.edit("`Still Running ....`")

    if HEROKU_API_KEY is not None:
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APP_NAME:
            await lol.edit(
                "`Please set up the HEROKU_APP_NAME variable to be able to update your bot.`"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await lol.edit(
                f"{txt}\n`Invalid Heroku credentials for updating bot dyno.`"
            )
            repo.__del__()
            return
        await lol.edit(
            "`[Updater]\
                        Your bot is being deployed, please wait for it to complete.\nIt may take upto 5 minutes `"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except GitCommandError as error:
            await lol.edit(f"{txt}\n`Here is the error log:\n{error}`")
            repo.__del__()
            return
        await lol.edit("Successfully Updated!\n" "Restarting.......")
    else:
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        reqs_upgrade = await updateme_requirements()
        await lol.edit("`Successfully Updated!\n" "restarting......`")
        args = [sys.executable, "-m", "Evie"]
        execle(sys.executable, *args, environ)
        return


      
      


  
  
print('xD')
alain.run_until_disconnected()

