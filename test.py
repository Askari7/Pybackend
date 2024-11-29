import datetime, time
import requests
import json

api = "http://182.180.188.205:9099/api/save-record/"
file = "D:/dawatislami/back/Pybackend/data.txt"

def send_data():
    while True:
        # try:
        with open(file) as f:
            val = f.readline().strip()
            # print(val)
        if len(val)>0:
            data = json.loads(val)
            x = requests.post(api,json=data,timeout=30)
            print(x)
            # if x.status_code == 201:
            #     with open(file,'r') as f:
            #         val = f.read().splitlines()
            #     writes = val[1:]
            #     with open(file,'w') as f:
            #         for data in writes:
            #             f.write(data+'\n')
            
        break
        # except Exception as e:
        #     print(e)
        #     time.sleep(1)
        #     break

send_data()
