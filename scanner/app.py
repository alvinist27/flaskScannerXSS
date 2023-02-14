import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from scanner.forms import ScanForm
from scanner.settings import SECRET_KEY_LENGTH, STATIC_PATH, TEMPLATE_PATH

app = Flask(__name__, template_folder=TEMPLATE_PATH, static_folder=STATIC_PATH)
SECRET_KEY = os.urandom(SECRET_KEY_LENGTH)
app.config['SECRET_KEY'] = SECRET_KEY
CSRFProtect(app)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/contact')
def contact_page():
    return render_template('contact.html')


@app.route('/project')
def project_page():
    return render_template('project.html')


@app.route('/service')
def service_page():
    return render_template('service.html')


@app.route('/team')
def team_page():
    return render_template('team.html')


@app.route('/testimonial')
def testimonial_page():
    return render_template('testimonial.html')


@app.errorhandler(404)
def not_found_page(error):
    return render_template('404.html'), 404


@app.route('/scan', methods=('GET', 'POST'))
def scan_page():
    scan_form = ScanForm()
    return render_template('scan.html', scan_form=scan_form)


if __name__ == '__main__':
    app.run(debug=True)
