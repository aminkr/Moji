import requests


if __name__ == '__main__':
    url = 'http://127.0.0.1:5000/api/predict'
    files = {'file': open('report.xls', 'rb')}
    res = requests.post(url, files=files)
    print(res)