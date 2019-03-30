from flask import request
from flask_restful import Api, Resource
from hbcvt import h2b
import pprint

from app.views import api_blueprint, BaseResource
from app.models import Device, device_exist

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

@api.resource('/convert/text') # /api/service/text
class ServiceConvertText(Resource):
    def post(self):
        # receive (from app): (query, device_id)
        # service: 
            # check for strange chars in text
            # if not strange:
                # save text in Device object(device_id)
                # send request with page 1 to device
                # respond to app: success
            # else respond to app: fail
        query = request.json.get('query')
        device_id = request.json.get('device_id')
        if query and device_id:
            # todo: check strange text
            try: 
                text = convert(query) # convert to braille data
                
                # save to device
                if device_exist(device_id):
                    device = Device.query.filter_by(name=device_id).first()
                    device.update(text)
                else:
                    device = Device(
                        name=device_id,
                        text=text
                    )
                    device.save()
                
                # todo: send request to device with device_id
                # request to device: device.page()

                return {
                    'success': True
                }
            except:
                return {
                    'success': False,
                    'error': 'an error has occurred'
                }, 500
        else:
            return {
                'success': False,
                'error': "'query' or 'device_id' not found"
            }, 500

# paging resource
# todo: SDK 이용해 IoT 디바이스로 데이터 전송

@api.resource('/page/prev') # /api/service/page/prev
class ServicePagePrev(Resource):
    def post(self):
        # receive (from device): device_id
        device_id = request.json.get('device_id')
        if device_exist(device_id):
            device = Device.query.filter_by(name=device_id).first()
            if device.prev_page(): # 페이지 잘 돌아감
                # device.page()를 전송
                return {
                    'success': True,
                    'result': device.page()
                }
            else:
                return {
                    'success': False,
                    'error': 'index error'
                }
        else:
            return {
                'success': False,
                'error': 'no such device'
            }

@api.resource('/page/next') # /api/service/page/next
class ServicePageNext(Resource):
    def post(self):
        # receive (from device): device_id
        device_id = request.json.get('device_id')
        if device_exist(device_id):
            device = Device.query.filter_by(name=device_id).first()
            if device.next_page(): # 페이지 잘 넘어감
                # device.page()를 전송
                return {
                    'success': True,
                    'result': device.page()
                }
            else:
                return {
                    'success': False,
                    'error': 'index error'
                }
        else:
            return {
                'success': False,
                'error': 'no such device'
            }
