from models import init_db
from flask import Flask, render_template

app = Flask(__name__)


init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/eventos')
def about():
    return render_template('eventos.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

if __name__ == '__main__':
    app.run(debug=True)