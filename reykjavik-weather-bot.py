#!/usr/bin/env python

import requests
import logging
from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler)

logging.basicConfig(filename = 'reykjavik_weather_bot.log', filemode = 'a', format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

keyboard = [['/vedur']]

def start(update, context):
    user = update.message.from_user
    update.message.reply_text(
        'Reykjavík Weather Bot sendir nýjustu veðurathuganir í Reykjavík frá Veðurstofu Íslands.\n\nSendu /vedur eða smelltu á hnappinn til að birta veðurathuganir.',
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, ))

def vedur(update, context):
    user = update.message.from_user
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
    if not not apis['V']: data.append(v)
    n = '\t\tSkýjahula: ' + apis['N'] + '% \n\n'
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

    update.message.reply_text(' '.join(data), reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, ))
    logger.info("%s bad um /vedur", user.username)

def main():
    updater = Updater("API_KEY", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("vedur", vedur))
    updater.start_polling()
    updater.idle()

main()
