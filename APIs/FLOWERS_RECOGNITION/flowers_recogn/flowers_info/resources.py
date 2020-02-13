# -*- coding: utf-8 -*-

from flask_restful import Resource
from flask import request

from flowers_recogn.models import Flower


import numpy as np
import os
import io
from flask_jwt import jwt_required

class flower_list(Resource):
    
    def get(self):
        all_flowers = Flower.query.all()
        flowers_list = []
        for fl in all_flowers:
            flowers_list.append(fl.name)
        return({'names':flowers_list})
    