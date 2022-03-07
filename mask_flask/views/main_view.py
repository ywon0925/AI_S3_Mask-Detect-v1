from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html'), 200


@main_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html'), 200