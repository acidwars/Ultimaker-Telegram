#!/usr/bin/env python3
from ultimaker import Ultimaker3
from telegram import Bot
from os import environ
import time
import logging

__base_dir = "/var/log/ultimaker/"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
        %(message)s', level=logging.INFO, filename=__base_dir+"jobwatcher.log" )
api = Ultimaker3(environ['ULTIMAKER_IP'], "test")
api.loadAuth("/home/henrik/bin/ultimaker/auth.data")
bot = Bot(token=environ['ULTIMAKER_TOKEN'])
chat_id = environ['ULTIMAKER_CHATID']


def __get_job_state():
    job = api.get("/api/v1/print_job").json()
    if job.response != 200:
        logging.info("No jobs found!")
        return False
    if job.respone == 200:
        logging.info("Found " + job['name'])
        return True


while True
    if __get_job_state:
        job = api.get("/api/v1/print_job").json()
        job_progress = round(job['progress'], 2)
        job_name = job['name']
        if job_progress == 1.0:
            logging.info("Job finished!")
            msg = "Job " + job_name + " finished!"
            bot.send_message(chat_id=chat_id, text=msg)
            break
        else:
            time.sleep(20)
    if not __get_job_state:
        logging.warning("Did not found a job!")
        time.sleep(60)
