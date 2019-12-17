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

def smart(bot):
    global led1 
    global led2 
    global led3 
    global update_id
    back = 20
    
    # led status 
    if led1.closed:
        led1 = LED(12)

    if led2.closed:
        led2 = LED(21)

    if led3.closed:
        led3 = LED(16)

    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        action_list = [[ "روشن", "بازگشت"], [""]]
        sleep(1)
        update.message.reply_text("لطفا یکی از گزینه‌های زیر را انتخاب نمائید : ", reply_markup=telegram.ReplyKeyboardMarkup(action_list, one_time_keyboard=True))
        led1.off()
        led2.off()
        led3.off()
       
        if update.message:
            if update.message.text == "روشن" :
                while back:

                    lightLevel = readLight()
                    update.message.reply_text("شدت نور برابر است با : {}".format(lightLevel))
                    if 100<lightLevel<150:
                        led1.on()
                        led2.off()
                        led3.off()
                        update.message.reply_text("چراغ یک روشن")
                    elif 50<lightLevel<100:
                        led1.on()
                        led2.on()
                        led3.off()
                        update.message.reply_text("چراغ یک و دو روشن")
                    elif lightLevel<50:
                        led1.on()
                        led2.on()
                        led3.on()
                        update.message.reply_text("همه چراغ‌ها روشن شوند")
                    else:
                        led1.off()
                        led2.off()
                        led3.off()
                        update.message.reply_text("نیازی به چراغ روشن وجود ندارد.")

                    sleep(2.5)
                    back -=True
                    if not back:
                        update.message.reply_text("تست به پایان رسید!")
            elif update.message.text == "بازگشت":
                import run

                led1.close()
                led2.close()
                led3.close()

                run.main()
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
            smart(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            update_id += 1
 
if __name__ == '__main__':
    main()
