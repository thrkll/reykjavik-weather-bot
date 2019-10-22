#!/usr/bin/env python

import requests
import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

logging.basicConfig(filename = 'iceland_weather_bot.log',
                    filemode = 'a',
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

def vedur(update, context): # "/vedur" birtir einfaldar upplýsingar, "/vedur a" birtir allt
    apis = requests.get('https://apis.is/weather/observations/is?stations=1', timeout = 5).json()['results'][0]
    name = '%s kl. %s \n\n\n' % (apis['name'], apis['time'].split(" ")[1][0:5])
    # time = apis['time'].split(" ")[1][0:5]
    f = '\t\tVindhraði: ' +  apis['F'] + ' m/s \n\n'
    fx = '\t\tMesti vindhraði: ' + apis['FX'] + ' m/s \n\n'
    fg = '\t\tMesta vindhviða: ' + apis['FG'] + ' m/s \n\n'
    d = '\t\tVindstefna: ' + apis['D'] + '\n\n'
    t = '\t\tHitastig: ' + apis['T'] + '°C \n\n'
    r = '\t\tUppsöfnuð úrkoma: ' + apis['R'] + ' mm/klst \n\n'
    v = '\t\tSkyggni: ' + apis['V'] + ' m \n\n'
    n = '\t\tSkýjahula: ' + apis['N'] + ' % \n\n'
    p = '\t\tLoftþrýstingur: ' + apis['P'] + ' hPa \n\n'
    rh = '\t\tRakastig: ' + apis['RH'] + '% \n\n'
    user_says = " ".join(context.args)
    if user_says == 'a':
        update.message.reply_text(name + f + fx + fg  + d + t + r + v + n + p + rh)
        logger.info("%s bað um /vedur a", user.first_name)
    else:
        update.message.reply_text(name + t + f + r)
        logger.info("%s bað um /vedur", user.first_name)
    return ConversationHandler.END

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater("API_KEY", use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
        CommandHandler('vedur', vedur),
        ],
        states={},
        fallbacks=[]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
