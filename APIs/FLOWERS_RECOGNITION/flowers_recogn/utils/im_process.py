


from keras.preprocessing import image
from flowers_recogn import class_label_map, image_names
import numpy as np

#Function that maps the images labels (1-102) to the flowers names 
def getName(pred_index, image_names = image_names, class_indices = class_label_map):
    label = class_indices.iloc[pred_index].Label
    return(image_names.loc[label,'name'])

def prepImg(img, maxRatio=1.3):
    img_arr = image.img_to_array(img)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img_arr = image.img_to_array(img)
    
    w,h = img_arr.shape[1], img_arr.shape[0]
    ratio = w/h
    if ratio>maxRatio:
        d = int(np.round((w-1.1*h)/2))
        cropBox = (d, 0, w-d,h)
        img = img.crop(box = cropBox)
    if ratio<1/maxRatio:
        d = int(np.round((h-1.1*w)/2))
        cropBox = (0, d, w,h-d)
        img = img.crop(box = cropBox)
    
    img = img.resize((227, 227))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)/255
    
    return(img)
    

def predictSpecie(img, model):
    pred = model.predict_proba(img)
    predIndex = np.argmax(pred)
    proba = int(np.round(pred[0,predIndex],2)*100)
    
    if proba<50:
        argsorted = np.argsort(-pred)[0]
        
        #first best pred
        prob1 = pred[0,argsorted[0]] 
        prob1 = int(np.round(prob1,2)*100)
        resultName1 = getName(argsorted[0])
        result1 = {'name':resultName1,'probability':(str(prob1)+'%')}
        
        #second best pred
        prob2 = pred[0,argsorted[1]] 
        prob2 = int(np.round(prob2,2)*100)
        resultName2 = getName(argsorted[1])
        result2 = {'name':resultName2,'probability':(str(prob2)+'%')}
        
        return({'Best prediction':result1, 'Second best prediction':result2})
        
        
    proba = str(proba)+'%'
    resultName = getName(predIndex)
    result0 = {'name':resultName,'probability':proba}
    return({'Best prediction':result0, 'Second best prediction':None})