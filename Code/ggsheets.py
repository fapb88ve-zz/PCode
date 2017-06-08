import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd
import datetime
import time


def customers():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_id.json', scope)
    gs = gspread.authorize(creds)
    sheet = gs.open('Registro de Clientes').sheet1
    c_list = sheet.get_all_records()
    return pd.DataFrame(c_list)


def reg_files():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_id.json', scope)
    gs = gspread.authorize(creds)
    s_name = 'Registro de Archivos {}'.format(datetime.datetime.today().date())
    sh = gs.create(s_name)


print('Hasta que hora desea mantener el programa funcionando? (Favor utilizar format de hora de 24 horas, i.e.: 17:40')
response = input()
hour = response.split(':')[0]
minutes = response.split(':')[1]
print(hour, minutes)
