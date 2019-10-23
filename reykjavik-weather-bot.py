#!/usr/bin/env python

import requests
import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)

logging.basicConfig(filename = 'reykjavik_weather_bot.log',
                    filemode = 'a',
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

def vedur(update, context): # "/vedur" birtir einfaldar upplýsingar, "/vedur a" birtir allt
    apis = requests.get('https://apis.is/weather/observations/is?stations=1', timeout = 5).json()['results'][0]

    data = []

    name = '%s kl. %s \n\n\n' % (apis['name'], apis['time'].split(" ")[1][0:5])
    data.append(name)

    err = '\t\t' + apis['err']
    if not not apis['err']: data.append(err)
    w = '\t\tVeðurlýsing: ' + apis['W'] + ' \n\n'
    if not not apis['W']: data.append(w)
    t = '\t\tHitastig: ' + apis['T'] + '°C \n\n'
    if not not apis['T']: data.append(t)
    f = '\t\tVindhraði: ' +  apis['F'] + ' m/s \n\n'
    if not not apis['F']: data.append(f)
    fx = '\t\tMesti vindhraði: ' + apis['FX'] + ' m/s \n\n'
    if not not apis['FX']: data.append(fx)
    fg = '\t\tMesta vindhviða: ' + apis['FG'] + ' m/s \n\n'
    if not not apis['FG']: data.append(fg)
    d = '\t\tVindstefna: ' + apis['D'] + '\n\n'
    if not not apis['D']: data.append(d)
    r = '\t\tUppsöfnuð úrkoma: ' + apis['R'] + ' mm/klst \n\n'
    if not not apis['R']: data.append(r)
    v = '\t\tSkyggni: ' + apis['V'] + ' m \n\n'
    if not not apis['V']: data.append(m)
    n = '\t\tSkýjahula: ' + apis['N'] + ' % \n\n'
    if not not apis['N']: data.append(n)
    p = '\t\tLoftþrýstingur: ' + apis['P'] + ' hPa \n\n'
    if not not apis['P']: data.append(p)
    rh = '\t\tRakastig: ' + apis['RH'] + '% \n\n'
    if not not apis['RH']: data.append(rh)
    snc = '\t\tLýsing á snjó: ' + apis['SNC'] + ' \n\n'
    if not not apis['SNC']: data.append(snc)
    snd = '\t\tSnjódýpt: ' + apis['SND'] + ' \n\n'
    if not not apis['SND']: data.append(snd)
    sed = '\t\tSnjólag: ' + apis['SED'] + ' \n\n'
    if not not apis['SED']: data.append(sed)
    rte = '\t\tVegahiti: ' + apis['RTE'] + '°C \n\n'
    if not not apis['RTE']: data.append(rte)
    td = '\t\tDaggarmark: ' + apis['TD'] + '°C \n\n'
    if not not apis['TD']: data.append(td)

    user_says = " ".join(context.args)

    if user_says == 'a':
        update.message.reply_text(' '.join(data))
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
