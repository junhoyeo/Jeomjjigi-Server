import logging, json
import azure.functions as func
from hbcvt import h2b

def json_stringify(obj):
    return json.dumps(obj, ensure_ascii=False)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('query')
    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            query = req_body.get('query')

    if query:
        try:
            result = []
            for char in query:
                result.append([i[1][0] for i in h2b.letter(char)])
            return func.HttpResponse(
                json_stringify(
                    {
                        'success': True,
                        'query': query,
                        'result': result
                    }
                )
            )
        except:
            return func.HttpResponse(
                json_stringify(
                    {
                        'success': False,
                        'query': query,
                        'error': 'an error has occurred on the function'
                    }
                ),
                status_code=500
            )
    else:
        return func.HttpResponse(
             "'query' not found on the query string or in the request body",
             status_code=400
        )
