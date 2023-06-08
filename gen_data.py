import csv
import json

import requests

node = "https://osmosis.rest.stakin-nodes.com"

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

tx_resp = get_tx_by_hash("CF001F6398DB9B89FB107EE2D12627FDAA0773FE35DF3FB8D936D6780F07192E")

messages = tx_resp['tx']['body']['messages']
total = sum(int(msg['amount'][0]['amount']) for msg in messages)
data = []
for msg in messages:
     amount = int(msg['amount'][0]['amount'])
     tx = {'address': msg['to_address'], 'share': "{:.16f}".format(amount/total), 'amount': str(amount)}
     data.append(tx)

print(json.dumps(data, cls=CustomEncoder))

