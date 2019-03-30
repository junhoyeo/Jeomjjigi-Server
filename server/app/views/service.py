from flask import request
from flask_restful import Api, Resource
from hbcvt import h2b
import pprint

from app.views import api_blueprint, BaseResource

api = Api(api_blueprint, prefix='/service')

PAGE_LIMIT = 10 # limit of braille chars per page

def convert(query):
    '''전달된 텍스트 query를 점자로 변환하며 10개 이하의 문자가 한 페이지에 들어가게 나누고, 
        각 페이지(list)로 이루어진 리스트 result를 반환합니다'''
    result = []
    braille_count = 0 # number of braille chars in current page
    page = []
    for char in query:
        brailles = [i[1][0] for i in h2b.letter(char)] 
            # braille chars made with current letter(char)
        # print(char, brailles) # for debugging
        if braille_count + len(brailles) > 10: # next page
            result.append(page)
            page = brailles
            braille_count = len(brailles)
        else: # add in current page
            braille_count += len(brailles)
            page += brailles
    if page:
        result.append(page)
    # for page in result:
    #     pprint.pprint(page) # for debugging
    #     print(len(page))
    pprint.pprint(result)
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
