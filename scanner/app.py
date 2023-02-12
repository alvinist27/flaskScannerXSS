import os

from flask import Flask, render_template

from scanner.settings import SECRET_KEY_LENGTH, STATIC_PATH, TEMPLATE_PATH

app = Flask(__name__, template_folder=TEMPLATE_PATH, static_folder=STATIC_PATH)
SECRET_KEY = os.urandom(SECRET_KEY_LENGTH)
app.config['SECRET_KEY'] = SECRET_KEY


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


if __name__ == '__main__':
    app.run()
