import csv
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from skimage.transform import resize
from skimage.io import imread
import pandas as pd
import numpy as np

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
test_bp = Blueprint('test', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict(filepath, model):
    flat_img_arr = []
    img_array = imread(filepath)
    img_resized = resize(img_array,(150,150,3))
    flat_img_arr.append(img_resized.flatten())
    flat_img = np.array(flat_img_arr)
    df = pd.DataFrame(flat_img)
    return model.predict(df)

@test_bp.route('/test', methods=['GET','POST'])
def index():
    """
    index 함수에서는 '/' 엔드포인트로 접속했을 때 'index.html' 파일을
    렌더링 해줍니다.

    'index.html' 파일에서 'users.csv' 파일에 저장된 유저 목록을 보여줄 수 있도록
    유저들을 html 파일에 넘길 수 있어야 합니다.

    요구사항:
      - HTTP Method: `GET`
      - Endpoint: `/`

    상황별 요구사항:
      - `GET` 요청이 들어오면 `templates/index.html` 파일을 렌더해야 합니다.

    """
    if request.method == 'POST':
        error = ''
        if 'file' not in request.files:
            error = '파일이 없어요!'
            return render_template('test.html', error=error),200
        file = request.files['file']
        
        if file.filename == '':
            error = '사진을 넣어주세요!'
            return render_template('test.html', error=error),200
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            #result = predict(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), current_app.config['MODEL'])
            result = predict(file, current_app.config['MODEL'])
            print(result)
            if result[0]:
                return render_template('test.html', result=result),200
            else:
                return redirect(request.url)
        else:
            error = '잘못된 형식의 파일이에요!'
            return render_template('test.html', error=error),200
            
            
    return render_template('test.html'), 200
