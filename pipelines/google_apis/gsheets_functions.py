import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd

# Authentication Steps
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive',
          'https://mail.google.com/']
# This option is to authenticate using service_account.json (are there benefits to this?)
credentials = Credentials.from_service_account_file(
              '/Users/adamurquhart/coding/visual_studio/qardio/pipelines/google_apis/service_account.json',
              scopes=scopes)

gc = gspread.authorize(credentials)
gauth = GoogleAuth()
drive = GoogleDrive(gauth)


def gspread_write(df, wb, ws):
    # open a google sheet '1B0SFEV0K6TGodOIfCKqMRiPuiKgezA_-BvVk_AYhjVI'
    gs = gc.open_by_key(wb)
    # select a work sheet from its name 'python_data'
    ws = gs.worksheet(ws)

    # write to dataframe
    ws.clear()
    set_with_dataframe(worksheet=ws, dataframe=df, include_index=False,
                       include_column_header=True, resize=True)


def gspread_read(wb, ws):
    # open a google sheet
    gs = gc.open_by_key(wb)
    # select a work sheet from its name
    ws = gs.worksheet(ws)

    # Read to DataFrame
    return pd.DataFrame(ws.get_all_records())


if __name__ == '__main__':
    # df_22 = gspread_read('python_data')
    # df_22.to_csv('/Users/adamurquhart/Data/qardio_data.csv')
    df_22 = gspread_read(wb='1B0SFEV0K6TGodOIfCKqMRiPuiKgezA_-BvVk_AYhjVI', ws='Emailing Campaigns 2021')
    print(df_22.columns)
    df_22.drop(columns=['True Click Rate', 'Click per unique opens', '% Unsubs',
                        '% Unsubs Openers', 'Sessions', 'Sess per unique opens', 'ECR', 'Total Trans.',
                        'Revenue', 'AOV', 'QA Sold', 'QB Sold ', 'QC Sold  ', 'QA+QB Bundle',
                        'Triple Bundle', 'QA+QC bundle', 'QA Case', 'QA+SpO2', 'QTemp+SpO2',
                        'QC acces'])
