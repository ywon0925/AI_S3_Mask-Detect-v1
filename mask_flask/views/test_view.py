import csv
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
import numpy as np
from pymongo import MongoClient
import datetime
from PIL import Image
import io
import cv2


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
test_bp = Blueprint('test', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def convert_to_jpg(file):
    fname = file.filename
    i = pyheif.read(file)
    # Convert to other file format like jpeg
    s = io.BytesIO()
    pi = Image.frombytes(mode=i.mode, size=i.size, data=i.data)
    pi.save(s, format="jpeg")
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], fname.replace('heic','jpg'))
    pi.save(path)
    
    return path
def predict(file, model):
    X_test = []
    img_array = cv2.imread(file)[...,::-1]
    img_resized = cv2.resize(img_array,(224,224))
    X_test.append(img_resized)
    X_test = np.array(X_test)/255
    X_test.reshape(-1, 224, 224, 1)
    return model.predict(X_test)

def usage_count_to_mongo(predict):
    HOST = 'cluster0.n76ap.mongodb.net'
    USER = 'admin'
    PASSWORD = ''
    DATABASE_NAME = 'myFirstDatabase'
    COLLECTION_NAME = 'usage'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]

    feedback={}
        
    feedback['predict'] = int(predict)
    feedback['use_date'] = str(datetime.datetime.utcnow().date())
    feedback['use_time'] = datetime.datetime.utcnow()
    
    db[COLLECTION_NAME].insert_one(feedback)
    print('record model usage on mongoDB successfully')
@test_bp.route('/test', methods=['GET','POST'])
def index():
    result = None
    if request.method == 'POST':
        error = ''
        # check if file exist
        if 'file' not in request.files:
            error = '파일이 없어요!'
            return render_template('test.html', error=error),200
        file = request.files['file']
        print(type(file))

        if file.filename == '':
            error = '사진을 넣어주세요!'
            return render_template('test.html', error=error),200
        
        # if file is allowed type (ex jpg, png ...)
        # predict with image 
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            result = predict(file_path, current_app.config['MODEL'])
            if result[0][1] > 0.5:
                result = 1
            else:
                result = 0
            usage_count_to_mongo(result)
                
            os.remove(file_path)
            return render_template('test.html', result=result),200
        else:
            error = '잘못된 형식의 파일이에요!'
            return render_template('test.html', error=error),200
            
            
    return render_template('test.html', result=result), 200
