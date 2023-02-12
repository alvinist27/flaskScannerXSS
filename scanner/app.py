import os

from flask import Flask, render_template

from scanner.settings import SECRET_KEY_LENGTH, STATIC_PATH, TEMPLATE_PATH

app = Flask(__name__, template_folder=TEMPLATE_PATH, static_folder=STATIC_PATH)
SECRET_KEY = os.urandom(SECRET_KEY_LENGTH)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def main_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
