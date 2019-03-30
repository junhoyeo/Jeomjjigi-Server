import requests, json
api_key = json.load(open('./secret.json'))['api_key']
request_url = f'https://vision.googleapis.com/v1/images:annotate?key={api_key}'

def ocr_image(device_id, base64_image):
    res = requests.post(request_url, headers={
        'Content-Type': 'application/json; charset=utf-8'
    }, json={
        'requests': [{
            'image': {
                'content': base64_image
            },
            'features': [{ 
                'type': 'TEXT_DETECTION'
            }]
        }]
    })
    try:
        return res.json()['responses'][0]['fullTextAnnotation']['text'].replace('\n', ' ')
    except KeyError:
        return False
