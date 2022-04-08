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
        action_list_manual = ["hii"] ["hey"]
        update.message.reply_text("لطفا یکی از گزینه‌های زیر را انتخاب نمائید : ", reply_markup=telegram.ReplyKeyboardMarkup(action_list_manual, one_time_keyboard=True))

        if update.message:  
            if update.message.text == "turn on red":
                led1.on()
                bot.sendMessage(update.message.chat_id , "turned on red")
                sleep(1)

            elif update.message.text == "turn on blue":
                led2.on()
                update.message.reply_text("turned on blue")
                sleep(1)

            elif update.message.text == "turn on green":
                led3.on()
                update.message.reply_text("turned on green")
                sleep(1)

            elif update.message.text == "turn on all":
                led1.on()
                led2.on()
                led3.on()
                update.message.reply_text("turned on all")
                sleep(1)

            if update.message.text == "turn of red":
                led1.off()
                update.message.reply_text("turned of red")
                sleep(1)

            elif update.message.text == "turn of blue":
                led2.off()
                update.message.reply_text("turned of blue")
                sleep(1)

            elif update.message.text == "turn of green":
                led3.off()
                update.message.reply_text("turned of green")
                sleep(1)

            elif update.message.text == "turn all off":
                led1.off()
                led2.off()
                led3.off()
                update.message.reply_text("turned all leds off. thanks for saving energy")
                sleep(1)
            elif update.message.text == "start":
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
    bot = telegram.Bot('AAETnun0PVseADWv4Tb8uwQWHmjY4wPvWQ8')

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
