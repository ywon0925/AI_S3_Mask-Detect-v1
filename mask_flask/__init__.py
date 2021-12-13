from flask import Flask
import pickle
from tensorflow import keras
import os

path = os.path.join(os.getcwd(),'mask_flask/img_upload')
if not os.path.exists(path):
    os.makedirs(path)

UPLOAD_FOLDER = path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODEL'] = None
with open('mask_flask/tf_learning_model.pkl','rb') as pickle_file:
    app.config['MODEL'] = pickle.load(pickle_file)
    
from mask_flask.views.main_view import main_bp
from mask_flask.views.test_view import test_bp
from mask_flask.views.feedback_view import feedback_bp

app.register_blueprint(main_bp)
app.register_blueprint(test_bp)
app.register_blueprint(feedback_bp)


if __name__ == "__main__":
    app.run(debug=True)
