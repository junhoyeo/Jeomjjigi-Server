import requests 

r = requests.post('http://localhost:8080/api/service/convert', json={
    'query': '서울하드웨어해커톤'
})

print(r.status_code)
print(r.text)
