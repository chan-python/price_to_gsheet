import ast
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
price_conv = []

def get_price(param_coin):
    binance_url = 'https://api.binance.com'
    response = requests.get(binance_url)

    parameters = {'symbol': param_coin}
    res = requests.get(binance_url + '/api/v3/avgPrice', params=parameters)
    usd = ast.literal_eval(res.text)
    usdt_conv = float(usd["price"])
    return usdt_conv

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]
json_file_name = '--downloaded json file--.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/--securekey--/edit#gid=0'
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('liquidation')

price_list = ['BTCUSDT', 'ETHUSDT', 'XRPUSDT', 'LUNAUSDT']
price_excel_list = ['B2', 'B3', 'B4', 'B6']

for i in range(0, 3):
    price_conv.append(get_price(price_list[i]))

url = "https://sg-api.upbit.com"
querystring = {"market": "BTC-LUNA", "count": "1"}
response = requests.request("GET", url + '/v1/trades/ticks', params=querystring)
lunabtc = response.text.replace("[", "")
lunabtc = lunabtc.replace("]", "")
lunabtc = ast.literal_eval(lunabtc)
lunabtc_conv = float(lunabtc['trade_price'])
caculate_luna = 1 * lunabtc_conv * price_conv[0]
price_conv.append(caculate_luna)

for i in range(0, len(price_list)):
    coin_name = price_list[i].replace("USDT", "")
    print("1 "+ coin_name +" $" + '%.8f' % price_conv[i])
    worksheet.update_acell(price_excel_list[i], price_conv[i])
