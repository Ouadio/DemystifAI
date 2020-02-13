
#Flask basics
from flask import ( render_template, Blueprint, redirect, url_for)
import requests  
from web_apps.Flowers_Recognition.forms import uploadRecogIm
from werkzeug.utils import secure_filename
import os
from web_apps import app
from flask_login import login_required

flowers_blueprints = Blueprint('Flowers', __name__, template_folder='templates/Flowers_Recognition', static_folder='static/Flowers_Recognition', static_url_path='static')


@flowers_blueprints.route('/display', methods = ['GET'])
def display():    
    return(render_template("display.html"))


@flowers_blueprints.route('/recognition', methods = ['GET','POST'])
@login_required
def recognition():
    form = uploadRecogIm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        full_filename = os.path.join(app.config['BASE_DIR'], app.config['UPLOAD_FOLDER'],filename)
        form.file.data.save(full_filename )
        url = 'http://localhost:5000/predict'
        file = {'image': open(full_filename,'rb')}
        response = requests.post(url, files=file)
        jsonFile = response.json()
        #titles_dict = list(jsonFile.keys())
        user_image = '/'+os.path.join( app.config['UPLOAD_FOLDER'],filename)
        
        result  = []
        best_pred = jsonFile.get('Best prediction',None)
        
        base_google_url = "https://www.google.com/search?q="
        fl_name = best_pred.get('name')
        fl_google = base_google_url + str.replace(fl_name, ' ', '+') + '+flower'
        best_pred['link'] = fl_google
        
        result.append(best_pred)
        if jsonFile.get('Second best prediction',None) is not None:
            second_best_pred = jsonFile.get('Second best prediction',None)
            fl_name = second_best_pred.get('name')
            fl_google = base_google_url + str.replace(fl_name, ' ', '+') + '+flower'
            second_best_pred['link'] = fl_google
            result.append(second_best_pred)
        
        
        return render_template("display.html", user_image = user_image, result = result)
        
    return render_template('upload.html', form=form, user_image=None)



@flowers_blueprints.route('/flowerslist', methods = ['GET'])
@login_required
def displayFlowersList():
    url = 'http://localhost:5000/flower_list'
    response = requests.get(url)
    jsonFile = response.json()
    flowersList = jsonFile["names"]
    base_google_url = "https://www.google.com/search?q="
    flowers_data = []
    for fl in flowersList:
        fl_google = base_google_url + str.replace(fl, ' ', '+') + '+flower'
        fl_dict = {'name':fl ,'link':fl_google}
        flowers_data.append(fl_dict)
    
    return(render_template("flowers_list.html", flowers_data = flowers_data))