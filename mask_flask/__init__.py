from flask import Flask
import pickle
import sklearn

UPLOAD_FOLDER = 'mask_flask/img_upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODEL'] = None
with open('mask_flask/model.pkl','rb') as pickle_file:
    app.config['MODEL'] = pickle.load(pickle_file)
    
from mask_flask.views.main_view import main_bp
from mask_flask.views.test_view import test_bp

app.register_blueprint(main_bp)
app.register_blueprint(test_bp)

if __name__ == "__main__":
    app.run(debug=True)
