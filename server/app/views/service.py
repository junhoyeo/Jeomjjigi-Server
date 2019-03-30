from flask import request
from flask_restful import Api, Resource
from hbcvt import h2b

from app.views import api_blueprint, BaseResource

api = Api(api_blueprint, prefix='/service')

def convert(query):
    result = []
    for char in query:
        result.append([i[1][0] for i in h2b.letter(char)])
    return result

@api.resource('/') # /api/service/
class ServiceTest(Resource):
    def get(self):
        return {
            'success': True
        }

@api.resource('/convert') # /api/auth/service
class ServiceConvert(BaseResource):
    def get(self):
        query = request.args.get('query')
        if query:
            try: 
                result = convert(query)
                return self.safe_json({
                    'success': True,
                    'query': query,
                    'result': result
                })
            except:
                return self.safe_json({
                    'success': False,
                    'query': query,
                    'error': 'an error has occurred'
                }, status_code=500)
        else:
            return {
                'success': False,
                'error': "'query' not found"
            }, 500

    def post(self):
        query = request.json.get('query')
        if query:
            try: 
                result = convert(query)
                return self.safe_json({
                    'success': True,
                    'query': query,
                    'result': result
                })
            except:
                return self.safe_json({
                    'success': False,
                    'query': query,
                    'error': 'an error has occurred'
                }, status_code=500)
        else:
            return {
                'success': False,
                'error': "'query' not found"
            }, 500
