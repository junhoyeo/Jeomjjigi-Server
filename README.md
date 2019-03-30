# Seoul HW Hackathon 2019

# 📌 API Server Docs

## 1. 애플리케이션 → 서버 📱

앱이 전달: (텍스트 또는 이미지 → 텍스트, 디바이스 id) → 서버가 디바이스 id에 맞는 오브젝트에 텍스트 저장 → 앱에 성공여부 전송, IoT 디바이스로 페이징된 점자 데이터의 1페이지 전송

## [POST] /api/service/convert/text

안드로이드 애플리케이션(클라이언트)로부터 **텍스트**와 연결할 **디바이스 id**를 입력받아 해당 디바이스 오브젝트에 점자 정보를 저장하고 디바이스로 데이터를 전송(구현 중)한다.

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

### todo

- azure-iot-sdk-python을 이용해서 디바이스로 정보 전송
- 전달받은 text를 살펴서 점자로 표현이 어려운 데이터를 필터링하거나 에러 출력

## 2. IoT 디바이스 → 서버 💡

## [POST] /api/service/page/prev

## [POST] /api/service/page/next

디바이스에서 `device_id`를 페이지 넘김에 따라 전송하면 서버는 해당 디바이스가 읽어야 할 페이지 데이터를 전송한다(안드는 몰라도 됨).

### request

```json
{
    "device_id": "odinevk"
}
```

### response

```json
{
    "success": true, 
    "result": [
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
}
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

아직 SDK로도 구현해야 한다.
