import requests 

r = requests.post('http://ubuntu.hanukoon.com:8080/api/service/convert/text', json={
    'device_id': 'odinevk',
    'query': '서울하드웨어해커톤'
})

print(r.status_code)
print(r.text)
