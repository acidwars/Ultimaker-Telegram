#!/usr/bin/env python3
from ultimaker import Ultimaker3
from telegram.ext import Updater, CommandHandler
from os import environ
import telegram
import logging
from urllib.request import urlretrieve

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
        %(message)s', level=logging.INFO)
api = Ultimaker3("192.168.1.119", "application")
api.loadAuth("/home/henrik/bin/ultimaker/auth.data")

def downloadSnapshot():
    url = "http://192.168.1.119:8080/?action=snapshot"
    urlretrieve(url, "/tmp/snapshot.jpg")


def checkJobState():
    job = api.get("/api/v1/print_job").json()
    materials = api.get("/api/v1/materials").json()
    stream = api.get("/api/v1/camera/feed").json()
    downloadSnapshot()
    return job, stream


def status(bot, update):
    chat_id = update.message.chat_id
    job, stream = checkJobState()
    job_name = job['name']
    job_progress = round(job['progress'], 2) * 100
    job_progress = str(job_progress)+"%"
    job_started = job['datetime_started']
    reply = "JOB: " + str(job_name) + "\nPROGRESS: " + \
            str(job_progress) + "\n" + "STARTED: " + str(job_started)+ \
            "\nFEED: " + stream
    logging.info(job_name)
    logging.info(job_progress)
    update.message.reply_text(reply)
    logging.info(job_started)
    bot.send_photo(chat_id="-1001196544036", photo=open("/tmp/snapshot.jpg",\
            'rb'))

bot = telegram.Bot(environ["ULTIMAKER_BOT_TOKEN"])
updater = Updater(environ["ULTIMAKER_BOT_TOKEN"])
updater.dispatcher.add_handler(CommandHandler('status', status))
updater.start_polling()
updater.idle()
