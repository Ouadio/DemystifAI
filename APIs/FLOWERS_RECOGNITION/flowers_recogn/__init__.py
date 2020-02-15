# -*- coding: utf-8 -*-


from keras.models import model_from_json
from scipy.io import loadmat
#Flask basics
from flask import Flask
#RestAPI
from flask_restful import Api

#utilities
import os
import pandas as pd

#App configuration
from config import DevConfig

#ORM & Migration
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

#Rest Authentication
from flask_jwt import JWT
from flowers_recogn.security import authenticate, identity

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#Flask App
app = Flask(__name__)
app.config.from_object(DevConfig)
app.config["SECRET_KEY"] = "winux"

#Data Base Configuration
db_dir = os.path.join(BASE_DIR, "database.sqlite")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_dir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Migration
Migrate(app, db)


#CPU config (GPU will run out of memory)
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

#Flask Api
api = Api(app)

#Models weights
MODELS_DIR = os.path.join(BASE_DIR, 'ML_Models')
PICTURES_DIR = os.path.join(BASE_DIR, 'static','imExamples')
MAPPINGS_DIR = os.path.join(BASE_DIR, 'static','imageMaps')


image_labels_path = os.path.join(MAPPINGS_DIR, 'imagelabels.mat')
names_path = os.path.join(MAPPINGS_DIR, 'flowers_names.csv')
maps_path = os.path.join(MAPPINGS_DIR, 'class_label_map.csv')

#Reading labels
image_labels = loadmat(image_labels_path)['labels'][0] - 1
#Reading names (a set of flowers label-name mapping)
image_names=pd.read_csv(names_path, sep=',', names=('labels','name'), header=0)
#reading the other index-index mapping caused by training gen
class_label_map = pd.read_csv(maps_path)

#Rest Authentication
jwt = JWT(app,authenticate, identity)

# load json and create model
json_file = open(os.path.join(MODELS_DIR, 'VGG_FNN_Arch.json'), 'r')
loaded_model_json = json_file.read()
json_file.close()
recognition_model = model_from_json(loaded_model_json)
# load weights into new model
recognition_model.load_weights(os.path.join(MODELS_DIR, "VGG_FNN_Tuned_Weights.h5"))
#COmpile the predict method for multi-threading
recognition_model._make_predict_function()





#EXPLANATION : 
    #"This is never mentioned in the Keras docs, but its necessary to make it work 
    #concurrently. In short, _make_predict_function is a function that compiles the 
    #predict function. In multi thread setting, you have to manually call this function 
    #to compile predict in advance, otherwise the predict function will not be compiled 
    #until you run it the first time, which will be problematic when many threading 
    #calling it at once. 
#####
#   REST APIs are naturally multi-thread, once they can execute multiple requests at 
#   the same time. 

