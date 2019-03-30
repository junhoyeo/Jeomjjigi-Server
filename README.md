# Seoul HW Hackathon 2019

# 📌 API Server Docs
- `nohup python -u serve.py &`

<!-- - `azure-iothub-service-client` 패키지 사이즈 때문에 lock이 오래 걸리므로 `pipenv install --skip-lock`를 권장함 -->
<!-- - MacOS에서 `brew install boost-python3` 해야 하더라 -->

## ./server/secret.json
```json
{
    "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxx-x-xxxxxxxxx",
    "connection": "HostName=xxxxx.azure-devices.net;SharedAccessKeyName=xxxxx;SharedAccessKey=xxxxx"
}
```

`./server/`에 위와 같이 Google Cloud Vision API가 사용 설정된 api_key와 Azure IoT hub에 대한 connection string을 포함하는 `secret.json`을 생성해 둔다.

## 1. 애플리케이션 → 서버 📱

앱이 전달: (텍스트 또는 이미지 → 텍스트, 디바이스 id) → 서버가 디바이스 id에 맞는 오브젝트에 텍스트 저장 → 앱에 성공여부 전송, IoT 디바이스로 페이징된 점자 데이터의 1페이지 전송

## [POST] /api/service/convert/text

안드로이드 애플리케이션(클라이언트)로부터 **텍스트**와 연결할 **디바이스 id**를 입력받아 해당 디바이스 오브젝트에 점자 정보를 저장하고 디바이스로 데이터를 전송한다.

### request

```json
{
    "device_id": "odinevk",
    "query": "서울하드웨어해커톤"
}
```

`device_id`: string → 디바이스 키 값

`query`: string → 변환할 텍스트

### response

```json
{
    "success": true
}
```

`success`: bool → 성공 시 참, 실패 또는 에러 시 거짓

(success=false 시 에러 유형(메세지)에 대한 `error` 필드가 추가됨)

### to IoT device

```json
[
    [0, 0, 0, 0, 0, 1], 
    [0, 1, 1, 1, 0, 0], 
    [1, 1, 0, 1, 1, 0], 
    [1, 0, 1, 1, 0, 0], 
    [0, 1, 0, 0, 0, 0], 
    [0, 1, 0, 1, 1, 0], 
    [1, 1, 0, 0, 0, 1], 
    [0, 1, 0, 1, 0, 0], 
    [0, 1, 0, 1, 0, 1]
]
```

위와 같은 데이터가 IoT 디바이스로 전송된다(렌더링할 점자의 첫 페이지).

### todo

- 전달받은 text를 살펴서 점자로 표현이 어려운 데이터를 필터링하거나 에러 출력

## [POST] /api/service/convert/image

안드로이드 애플리케이션(클라이언트)로부터 **base64 인코딩된 이미지 텍스트**와, 연결할 **디바이스 id**를 입력받아 해당 디바이스 오브젝트에 점자 정보를 저장하고 디바이스로 데이터를 전송한다.

### request
```json
{
    "device_id": "odinevk",
    "image": "BASE64_ENCODED_DATA"
}
```

`device_id`: string → 디바이스 키 값

`image`: string → base64 인코딩된 이미지 텍스트

### response
```json
{
    "success": true
}
```

`success`: bool → 성공 시 참, 실패 또는 에러 시 거짓

(success=false 시 에러 유형(메세지)에 대한 `error` 필드가 추가됨)

## 2. IoT 디바이스 → 서버 💡

## [GET] /api/service/page/prev/{device_id:string}

## [GET] /api/service/page/next/{device_id:string}

디바이스에서 `device_id`를 페이지 넘김에 따라 전송하면 서버는 해당 디바이스가 읽어야 할 페이지 데이터를 전송한다(안드는 몰라도 됨).

### response

```json
[
    [0, 0, 0, 0, 0, 1], 
    [0, 1, 1, 1, 0, 0], 
    [1, 1, 0, 1, 1, 0], 
    [1, 0, 1, 1, 0, 0], 
    [0, 1, 0, 0, 0, 0], 
    [0, 1, 0, 1, 1, 0], 
    [1, 1, 0, 0, 0, 1], 
    [0, 1, 0, 1, 0, 0], 
    [0, 1, 0, 1, 0, 1]
]
```

```json
{
    "success": false,
    "error": "index error"
}
```

```json
{
    "success": false,
    "error": "no such device"
}
```

`index error`일 때는 그냥 클라이언트 단에서 에러로 처리한다.
