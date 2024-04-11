from models import init_db, authenticate_user
from flask import Flask, flash, redirect, render_template, request, session



app = Flask(__name__)
app.secret_key = 'IDHASIHDAIDHASKPCLS'  


init_db()

@app.route('/')
def home():

    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if password != 'admin' and password != '1':
            password = hash(password)

        
        result, msg, email, password, user_name = authenticate_user(email, password)
        if not result:
            flash(msg, category='error')
            return render_template('login.html')

        else:
            session['user_email'] = email # Set the user_id in the session
            session['user_password'] = password # Set the user_password in the session
            session['user_name'] = user_name # Set the user_name in the session
            return redirect('/')
    else:
        return render_template('login.html')


@app.route('/eventos')
def about():
    return render_template('eventos.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)