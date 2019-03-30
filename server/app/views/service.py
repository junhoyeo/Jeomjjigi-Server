from flask import request
from flask_restful import Api, Resource
from hbcvt import h2b
import re
import json
import pprint

# ***** failed *****
# import iothub_service_client
# from iothub_service_client import IoTHubMessaging, IoTHubMessage, IoTHubError

# def open_complete_callback(context):
#     print('open_complete_callback called with context: {0}'.format(context))

# def send_complete_callback(context, messaging_result):
#     context = 0
#     print('send_complete_callback called with context : {0}'.format(context))
#     print('messagingResult : {0}'.format(messaging_result))

from app.views import api_blueprint, BaseResource
from app.models import Device, device_exist
from app.utils.connection import send_to_device
from app.utils.ocr import ocr_image

api = Api(api_blueprint, prefix='/service')

PAGE_LIMIT = 5 # limit of braille chars per page

# def filter_query(query):
#     return re.sub(u'[^((?=\u3131-\ucb4c)(?=A-Za-z)(?=(\,|\.|\-|\?|\_|\!)+)]', '', query)

def filter_query(query):
    reg = re.compile('[^-가-힣a-bA-Z0-9,._ ?!]')
    return reg.sub('', query)

def convert(query):
    '''전달된 텍스트 query를 점자로 변환하며 10개 이하의 문자가 한 페이지에 들어가게 나누고, 
        각 페이지(list)로 이루어진 리스트 result를 반환합니다'''
    query = filter_query(query)
    result = []
    braille_count = 0 # number of braille chars in current page
    page = []
    for char in query:
        brailles = [i[1][0][:3] + list(reversed(i[1][0][3:])) for i in h2b.letter(char)]
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

                send_to_device(device_id, device.page())
                # ***** failed *****
                # msg = json.dumps(device.page())
                # try:
                #     iothub_messaging = IoTHubMessaging(connection_string)
                #     iothub_messaging.open(open_complete_callback, 0)
                #     message = IoTHubMessage(bytearray(msg, 'utf8'))
                #     iothub_messaging.send_async(device_id, message, send_complete_callback, 1)

                # except IoTHubError as iothub_error:
                #     print("Unexpected error {0}" % iothub_error)

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
            }, 400

@api.resource('/convert/image') # /api/service/convert/image
class ServiceConvertImage(Resource):
    def post(self):
        image = request.json.get('image')
        device_id = request.json.get('device_id')
        if image and device_id:
            try: 
                query = ocr_image(device_id, image)
                if not query:
                    return { 'success': False, 'error': 'no text found' }
                text = convert(query)
                if device_exist(device_id):
                    device = Device.query.filter_by(name=device_id).first()
                    device.update(text)
                else:
                    device = Device(
                        name=device_id,
                        text=text
                    )
                    device.save()
                send_to_device(device_id, device.page())
                return { 'success': True }
            except:
                return { 'success': False, 'error': 'an error has occurred' }, 500
        else:
            return { 'success': False, 'error': "'query' or 'device_id' not found" }, 400

# paging resources

@api.resource('/page/prev/<string:device_id>') # /api/service/page/prev
class ServicePagePrev(Resource):
    def get(self, device_id):
        # receive (from device): device_id
        if device_exist(device_id):
            device = Device.query.filter_by(name=device_id).first()
            if device.prev_page(): # 페이지 잘 돌아감

                send_to_device(device_id, device.page()) # device.page()를 전송
                
                return device.page()
            else:
                return {
                    'success': False,
                    'error': 'index error'
                }, 400
        else:
            return {
                'success': False,
                'error': 'no such device'
            }, 400

@api.resource('/page/next/<string:device_id>') # /api/service/page/next
class ServicePageNext(Resource):
    def get(self, device_id):
        # receive (from device): device_id
        if device_exist(device_id):
            device = Device.query.filter_by(name=device_id).first()
            if device.next_page(): # 페이지 잘 넘어감

                send_to_device(device_id, device.page()) # device.page()를 전송

                return device.page()
            else:
                return {
                    'success': False,
                    'error': 'index error'
                }, 400
        else:
            return {
                'success': False,
                'error': 'no such device'
            }, 400
