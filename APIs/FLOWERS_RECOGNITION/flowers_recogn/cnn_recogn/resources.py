from flask_restful import Resource
from flask import request
from PIL import Image

from flowers_recogn import recognition_model
from flowers_recogn.utils.im_process import prepImg, predictSpecie
import numpy as np
import os
import io
from flask_jwt import jwt_required

class recognition(Resource):
    
    #@jwt_required()
    def post(self):
        imgRaw = request.files.get("image")
        if imgRaw:
            #Image retrieving
            img = request.files["image"].read()
            img = Image.open(io.BytesIO(img))
            #Image Preprocessing
            img = prepImg(img, maxRatio=1.3)
            #Specie Prediction
            predictions = predictSpecie(img, model=recognition_model)
            return(predictions)
            
        else:
            return({'Best prediction':None, 'Second best prediction':None}, 401)
        
