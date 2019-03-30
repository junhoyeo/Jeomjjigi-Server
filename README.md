# Seoul HW Hackathon 2019

# 📌 API Server Docs

## [GET] /api/service/convert?query={query:string}

response는 아래 POST 방식과 동일합니다.

## [POST] /api/service/convert

### request

```json
{
    "query": "서울하드웨어해커톤"
}
```

`query`: string

### response
한 페이지당 최대 10개의 점자 문자를 표시할 수 있으므로, 각 한글 문자에 맞게 최대한 데이터를 정리하여 전송합니다.
