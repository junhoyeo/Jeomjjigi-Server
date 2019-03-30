from flask import Response
from flask_restful import Resource
import json

from app import app

class BaseResource(Resource):
    @classmethod
    def safe_json(cls, data, status_code=200, **kwargs):
        return Response(
            json.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )

@app.route('/')
def index():
    return 'App working'

from flask import Blueprint
api_blueprint = Blueprint('api', __name__) # api

import app.views.service
