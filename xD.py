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
    return await event.reply(f'**Hey** **[{event.sender.first_name}](tg://user?id={event.sender.id})!**\n**Nice to see you here..!\nSorry but i only works in zeda network..:)\n\nWill see you there!😉**', buttons=but)
  chat = [-1001363684870]
  if event.chat_id in chat:
    sedkk = [[Button.inline('Groups.', data="del")]]
    await event.reply(f"**Hey** **[{event.sender.first_name}](tg://user?id={event.sender.id})!**\n**I'm Zeda assistant who works for zeda network...!**", buttons=sedkk)
  else:
    await alain.delete_dialog(event.chat_id)
  
@alain.on(events.callbackquery.CallbackQuery(data="link"))
async def links(event):
  tf = [[Button.url('✘ Support ✘', 't.me/ZedaSupport'), Button.url('✘ Spam ✘', 't.me/ZedaSpam')]]
  tf += [[Button.url('✘ Updates ✘', 't.me/ZedaUpdates'), Button.inline('Back', data='pback')]]
  await event.edit('**Here are all the links of zeda network...!**', buttons=tf)
  
@alain.on(events.callbackquery.CallbackQuery(data="del"))
async def links(event):
  tf = [[Button.url('✘ Support ✘', 't.me/ZedaSupport'), Button.url('✘ Spam ✘', 't.me/ZedaSpam')]]
  tf += [[Button.url('✘ Updates ✘', 't.me/ZedaUpdates'), Button.inline('Close', data='delll')]]
  await event.edit('**Here are all the links of zeda network...!**', buttons=tf)
  
  
@alain.on(events.callbackquery.CallbackQuery(data="delll"))
async def links(event):
  await event.delete()
  
@alain.on(events.callbackquery.CallbackQuery(data="pback"))
async def pbak(event):
  but = [[Button.inline('Groups.', data="link")]]
  await event.edit(f'**Hey** **[{event.sender.first_name}](tg://user?id={event.sender.id})!**\n**Nice to see you here..!\nSorry but i only works in zeda network..:)\n\nWill see you there!😉**', buttons=but)

  
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

  
  
print('xD')
alain.run_until_disconnected()

