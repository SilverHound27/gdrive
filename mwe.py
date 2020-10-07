#!/usr/bin/env python3

from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from telegram import ParseMode
from telegram.ext.dispatcher import run_async
from pydrive.auth import GoogleAuth
from upload import upload
import os
gauth = GoogleAuth()

bot_token = '1157928826:AAGE1lSPh6ZNzHCu5ogjKwouBrDbgXqejfI'
updater = Updater(token=bot_token,  workers = 8 , use_context=True)
dp = updater.dispatcher                                                          
print('Bot started \n')

###############################################################################

@run_async
def auth(update, context):
    FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'
    drive: GoogleDrive
    http = None
    initial_folder = None
    ID = update.message.from_user.id
    ID = str(ID)
    try:
        gauth.LoadCredentialsFile(ID)
    except Exception as e:
        print("Cred file missing :", e)

    if gauth.credentials is None:
        authurl = gauth.GetAuthUrl()
        AUTH_URL = '<a href ="{}">Vist This Url</a> \n Generate And Copy Your Google Drive Token And Send It To Me'
        AUTH = AUTH_URL.format(authurl)
        context.bot.send_message(
            chat_id=update.message.chat_id, text=AUTH, parse_mode=ParseMode.HTML)

    elif gauth.access_token_expired:
        # Refresh Token if expired
        gauth.Refresh()
    else:
        # auth with  saved creds
        gauth.Authorize()
        context.bot.send_message(
            chat_id=update.message.chat_id, text= "Already AUTH")


# It will handle Sent Token By Users
@run_async
def token(update, context):
    msg = update.message.text
    ID = update.message.from_user.id
    ID = str(ID)
    token = msg.split()[-1]
    if len(token) == 57 and token[1] == "/" :
        print(token)
        try:
            gauth.Auth(token)
            gauth.SaveCredentialsFile(ID)
            context.bot.send_message(
                chat_id=update.message.chat_id, text="AUTH Success")
        except Exception as e:
            print("Auth Error :", e)
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text="AUTH Failed")
   
@run_async
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text='HELLO WORLD')

@run_async
def alive(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm alive :)")

@run_async
def doc_handle(update, context):
    doc = update.message.document
    new_filename = ".".join(doc.file_name.split())

    sent_message = context.bot.send_message(chat_id=update.message.chat_id,
                     text='trying to download file:\n\t{}'.format(new_filename))
    
    file = context.bot.getFile(doc.file_id)
    file.download(doc.file_name)
    os.rename(doc.file_name, new_filename)
    SIZE = round((os.path.getsize(new_filename))/1048576)

    sent_message.edit_text('Trying to upload file: \n\t{}'.format(new_filename))
    
    try:
        dl_url = upload(new_filename, update, context, 'HERMES_UPLOAD')
    except Exception as e:
        print("error Code : UPX11", e)
        sent_message.edit_text("Uploading fail :{}".format(e))
    else:
        sent_message.edit_text("File uploaded successfully\n Filename: {}\n URL: {}".format(new_filename, dl_url))
    try:
        os.remove(new_filename)
    except Exception as e:
        print(e)

########################################################################
start_handler = CommandHandler('start', start)
dp.add_handler(start_handler)

help_handler = CommandHandler('alive', alive)
dp.add_handler(help_handler)

receive_doc = MessageHandler(Filters.document, doc_handle)
dp.add_handler(receive_doc)

auth_handler = CommandHandler('auth', auth)
dp.add_handler(auth_handler)

token_handler = MessageHandler(Filters.text, token)
dp.add_handler(token_handler)

updater.start_polling()
updater.idle()
