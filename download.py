import requests
import json
from datetime import date, timedelta
import time
import os

BEARER = 'Bearer '
URL = "https://api-school.kinderlime.com/api/web/parent/photos/?page=1&filters[photo][datetime_from]={} 00:00&filters[photo][datetime_to]={} 23:59"
START_DATE = date(2021, 6, 28)
END_DATE = date(2022, 9, 26)

def getMeta(datetime_from, datetime_to):
    payload={}
    headers = {
    'Authorization': BEARER
    }

    req_url = URL.format(datetime_from, datetime_to)
    response = requests.request("GET", req_url, headers=headers, data=payload)

    return json.loads(response.text)

def saveMedia(dt, metadata):
    if len(metadata['photos']) != 0:
        isExist = os.path.exists(dt)
        if not isExist:
            os.makedirs(dt)
            print('Created Directory:', dt)
        for photo in metadata['photos']:
            print(dt, photo['id'])
            response = requests.request("GET", photo['main_url'])
            if response.headers.get('Content-Type') == 'image/jpeg':
                with open(dt + '/' + photo['id'] + '.jpg', 'wb') as f:
                    f.write(response.content)
            else:
                print(photo)
                exit()
            

def main():
    from_dt = START_DATE
    to_dt = START_DATE + timedelta(days=1)
    while from_dt != END_DATE:
        print(from_dt.strftime('%Y-%m-%d'), to_dt.strftime('%Y-%m-%d'))
        dailyMeta = getMeta(from_dt, to_dt)
        saveMedia(from_dt.strftime('%Y-%m-%d'), dailyMeta)
        from_dt = from_dt + timedelta(days=1)
        to_dt = to_dt + timedelta(days=1)
        time.sleep(3)
    
main()