import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import pandas as pd


def clients():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_id.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Registro de Clientes').sheet1
    c_list = sheet.get_all_records()
    return pd.DataFrame(c_list)
