import requests
from redis import Redis
import json


cache = Redis(host='localhost', port=6379, db=7)


def main():
    filename = 'iinbin.txt'
    with open(filename, 'r') as f:
        iins = f.read()
        iins = iins.split('\n')
    count = 0
    result = []
    for iin in iins:
        
        count += 1

        print(count)

        identifier = iin.strip()
        
        print(identifier)

        url = "https://stat.gov.kz/api/juridical/counter/api/?bin={}&lang=ru".format(identifier)
        
        key = f'iin_{identifier}'

        try:
            resp = requests.get(url)
        except requests.exceptions.SSLError:
            resp = requests.get(url)
        
        if resp.status_code == 200:
            data = {}
            resp = resp.json()
            print(resp)
            key = f'wrong_{identifier}'
            if resp['success'] is True:
                data['identifier'] = identifier
                data['name'] = resp['obj']['name']
                data['status'] = 'YES'
                result.append(data) 
            else:
                data['identifier'] = identifier
                data['name'] = None
                data['status'] = 'NO'
                result.append(data)
    
    with open('iins.json', 'w') as f:
        json.dump(result, f)
        f.close()



def get_json():
    
    for obj in cache.keys(pattern='iin_*'):
        print(obj)


if __name__ == '__main__':
    main()
    # get_json()

