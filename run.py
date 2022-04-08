#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep

def control(bot):
    global update_id
    
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        action_list = [[ "hey raspy"], ["hey"]]
        sleep(1)
        update.message.reply_text("hii, how can i help you", reply_markup=telegram.ReplyKeyboardMarkup(action_list, one_time_keyboard=True))
        
        if update.message:
            if update.message.text == "کنترل هوشمند" :
                import smart
                smart.main()
                sleep(1)

            elif update.message.text == "turn on led":
                import manual 
                manual.main()
                sleep(1)

            elif update.message.text == "خاتمه":
                import sys
                #sys.exit(0)
                print("bye")

        else:
            time.sleep(2)

def main():
    global update_id
    bot = telegram.Bot('AAETnun0PVseADWv4Tb8uwQWHmjY4wPvWQ8')

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            control(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1
 
if __name__ == '__main__':
    main()
