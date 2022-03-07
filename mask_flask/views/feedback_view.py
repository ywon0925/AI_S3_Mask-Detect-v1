from flask import Blueprint, render_template, request
import datetime
from pymongo import MongoClient

def feedback_to_mongo(target, predict):
    HOST = 'cluster0.n76ap.mongodb.net'
    USER = 'admin'
    PASSWORD = ''
    DATABASE_NAME = 'myFirstDatabase'
    COLLECTION_NAME = 'feedback'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]

    feedback={}
    if target == 'yes':
        mg_target = 1
    else:
        mg_target = 0

    if predict == 'yes':
        mg_predict = mg_target
        mg_success = 1
    else:
        mg_success = 0
        if mg_target == 1:
            mg_predict = 0
        else:
            mg_predict = 1
        
    feedback['target'] = mg_target
    feedback['predict'] = mg_predict
    feedback['success'] = mg_success
    feedback['use_date'] = str(datetime.datetime.utcnow().date())
    feedback['use_time'] = datetime.datetime.utcnow()
    
    db[COLLECTION_NAME].insert_one(feedback)
    print('feedback added to mongoDB successfully')


feedback_bp = Blueprint('feedback_bp', __name__)

@feedback_bp.route('/feedback', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        error = ''
        if 'target' not in request.form or 'predict' not in request.form:
            error = '폼을 작성해주세요!'
            return render_template('feedback.html', error = error), 200
        target = request.form['target']
        predict = request.form['predict']
        
        feedback_to_mongo(target, predict)
        thankmsg ="Thank you for your Feedback!"
        
        return render_template('feedback.html', thankmsg=thankmsg), 200
        
    return render_template('feedback.html'), 200
