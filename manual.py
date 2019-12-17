#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from telegram import ReplyKeyboardMarkup
from gpiozero import LED
import RPi.GPIO as GPIO
from sensor import *
from telegram.ext import Updater, MessageHandler, Filters
import sys 

#setup the light sensor 
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

update_id = None
led1 = LED(12)
led2 = LED(21)
led3 = LED(16)

def manual(bot):
    global led1
    global led2 
    global led3 
    global update_id

    # led status 
    if led1.closed:
        led1 = LED(12)

    if led2.closed:
        led2 = LED(21)

    if led3.closed:
        led3 = LED(16)

    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        action_list_manual = [["یک روشن", "دو روشن" , "سه روشن"  , "همه روشن"] , ["یک خاموش","دو خاموش","سه خاموش","همه خاموش"], ["بازگشت"],[] ]
        update.message.reply_text("لطفا یکی از گزینه‌های زیر را انتخاب نمائید : ", reply_markup=telegram.ReplyKeyboardMarkup(action_list_manual, one_time_keyboard=True))

        if update.message:  
            if update.message.text == "یک روشن":
                led1.on()
                bot.sendMessage(update.message.chat_id , "لامپ شماره یک روشن شد.")
                sleep(1)

            elif update.message.text == "دو روشن":
                led2.on()
                update.message.reply_text("لامپ شماره دو روشن شد.")
                sleep(1)

            elif update.message.text == "سه روشن":
                led3.on()
                update.message.reply_text("لامپ شماره سه روشن شد.")
                sleep(1)

            elif update.message.text == "همه روشن":
                led1.on()
                led2.on()
                led3.on()
                update.message.reply_text("همه ی لامپ ها روشن شدند .")
                sleep(1)

            if update.message.text == "یک خاموش":
                led1.off()
                update.message.reply_text("لامپ شماره یک خاموش شد.")
                sleep(1)

            elif update.message.text == "دو خاموش":
                led2.off()
                update.message.reply_text("لامپ شماره دو خاموش شد.")
                sleep(1)

            elif update.message.text == "سه خاموش":
                led3.off()
                update.message.reply_text("لامپ شماره سه خاموش شد.")
                sleep(1)

            elif update.message.text == "همه خاموش":
                led1.off()
                led2.off()
                led3.off()
                update.message.reply_text("همه ی لامپ ها خاموش شدند .")
                sleep(1)
            elif update.message.text == "بازگشت":
                import run

                led1.close()
                led2.close()
                led3.close()

                sleep(1)
                run.main()
                sleep(1)
        else :
            sleep(1)


def main():
    global update_id
    bot = telegram.Bot('Telegram Token')

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            manual(bot)
            #smart(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1
 
if __name__ == '__main__':
    main()
