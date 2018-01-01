#! /usr/bin/env python3
# coding=utf-8

import sys
import os
import logging
import json
import requests
import importlib
import time
from telegram.ext import Updater
from telegram.ext import CommandHandler, Filters, MessageHandler
from bs4 import BeautifulSoup
from tinydb import TinyDB, Query

Daemon = importlib.import_module('daemon')

CONFIG = {}
DB = ''

def read_config():
    """
        Read config from `config.json`
    """
    global CONFIG
    with open("config.json", "r") as file:
        CONFIG = json.load(file)

    logging.debug("CONFIG: %s" % CONFIG)


def msg_wrapper(func):
    def wrapper(*args, **kwargs):
        update = args[1]
        logging_msg = "Receiving message from %d. Context: %s" % \
            (update.message.from_user.id, update.message.text)
        logging.info(logging_msg)
        # Check authorization
        user_id = update.message.from_user.id
        if str(user_id) not in CONFIG['admin']:
            logging_msg = "Non-admin user."
            logging.info(logging_msg)
            return
        # Call handler
        sent_msg = func(*args, **kwargs)
        logging_msg = 'Sent message: %s' % sent_msg.text
        logging.info(logging_msg)

    return wrapper


@msg_wrapper
def start(bot, update):
    """
        Handle `/start` command
    """
    return bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def user_id(bot, update):
    '''
        Handle `/user-id` command
    '''
    return bot.send_message(chat_id=update.message.chat_id, text=update.message.from_user.id)


@msg_wrapper
def get_kancolle_twitter_avatar(bot, update):
    '''
        Get the avatar of official Twitter account for Kantai Collection
    '''
    html = requests.get('https://twitter.com/KanColle_STAFF')
    soup = BeautifulSoup(html.text, "html.parser")
    tag = soup.find_all("a", class_="ProfileAvatar-container")
    return bot.send_message(chat_id=update.message.chat_id, \
                text=str(tag[0]['data-resolved-url-large']))


@msg_wrapper
def db_status(bot, update):
    '''
        Handle `/db-status` command
    '''
    db_name = "db-default.json"
    if 'db_name' in CONFIG:
        db_name = CONFIG['db_name']
    response_msg = 'Database name: %s\nDatabase file size: %s\nLast modified time: %s'\
         % (db_name, os.path.getsize(db_name), time.strftime("%d %b %Y %H:%M:%S", time.localtime(os.path.getmtime(db_name))))
    return bot.send_message(chat_id=update.message.chat_id, \
                text=response_msg)


def main():
    """
        Main function
    """
    read_config()
    db_name = "db-default.json"
    if 'db_name' in CONFIG:
        db_name = CONFIG['db_name']
    DB = TinyDB(db_name)

    updater = Updater(CONFIG['bot_token'])

    # Handle `/start`
    start_handler = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_handler)

    # Handle `/user-id`
    updater.dispatcher.add_handler(CommandHandler('user_id', user_id))
    # Handle `/kancolle-avatar`
    updater.dispatcher.add_handler(CommandHandler('kancolle_avatar', get_kancolle_twitter_avatar))
    # Handle `/db-satatus`
    updater.dispatcher.add_handler(CommandHandler('db_status', db_status))

    updater.start_polling()

class BotDaemon(Daemon.Daemon):
    def run(self):
        main()


usage = 'main.py {start|status|restart|stop}'
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(usage)
        exit(0)
    
    debug = False
    if len(sys.argv) == 3 and sys.argv[2] == '-d':
        debug = True
    
    # set logging
    if debug:
        logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(name)s][%(pathname)s:%(lineno)s][%(levelname)s][%(message)s]')
        # Daemon
        daemon = BotDaemon('/tmp/tg_bot_0x590F_test.pid', stderr='bot-err.log')
        logging.info('Debug mode.')
    else:
        logging.basicConfig(level=logging.ERROR,
                    format='[%(asctime)s][%(name)s][%(pathname)s:%(lineno)s][%(levelname)s][%(message)s]')
        # Daemon
        daemon = BotDaemon('/tmp/tg_bot_0x590F_test.pid', stderr='bot-err.log')

    operation = sys.argv[1]
    if operation == "status":
        print("Viewing daemon status")
        pid = daemon.get_pid()

        if not pid:
            print("Daemon isn't running ;)")
        else:
            print("Daemon is running [PID=%d]" % pid)
    elif operation == "start":
        print('Starting bot...')
        daemon.start()
        pid = daemon.get_pid()

        if not pid:
            print("Unable run daemon")
        else:
            print("Daemon is running [PID=%d]" % pid)
    elif operation == 'stop':
        print("Stoping daemon")
        daemon.stop()
    elif operation == 'restart':
        print("Restarting daemon")
        daemon.restart()
    else:
        print(usage)
