import csv
import json

import requests

snapshot_file = "../stakedrop/snapshot-29-01-2023.csv"
node = "https://osmosis-mainnet-rpc.allthatnode.com:1317"

'''WIP why is it not working ?'''
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, float):
            return "{:.16f}".format(obj)
        elif isinstance(obj, int):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def get_tx_by_hash(hash: str):
   resp = requests.request(
       "GET", f"{node}/cosmos/tx/v1beta1/txs/{hash}"
   )
   return resp.json()

tx_resp = get_tx_by_hash("1A20E4A1F89D9DC6D8F5CAAAEA84AF5CE5E130493AFF789462AF5E8B13E00A78")

messages = tx_resp['tx']['body']['messages']
total = sum(int(msg['amount'][0]['amount']) for msg in messages)
data = []
for msg in messages:
     amount = int(msg['amount'][0]['amount'])
     tx = {'address': msg['to_address'], 'share': "{:.16f}".format(amount/total), 'amount': str(amount)}
     data.append(tx)

print(json.dumps(data, cls=CustomEncoder))

