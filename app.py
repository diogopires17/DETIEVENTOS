import sqlite3
from models import *
from flask import Flask, flash, redirect, render_template, request, session



app = Flask(__name__)
app.secret_key = 'IDHASIHDAIDHASKPCLS'  


init_db()

@app.route('/')
def home():
    if 'user_email' not in session:
        return redirect('/login')
    events = get_events()
    print (events)

    return render_template('index.html', events=events)


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

@app.route('/criar')
def criar():
    #  se o user nao for o admin
    if session['user_email'] != "admin@gmail.com":
        flash("Não tem permissões para aceder aqui", category='error')
        return redirect('/')
    
    return render_template('novo_evento.html')
@app.route('/eventos')
def about():
    return render_template('eventos.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('q', '')  
    events = search_events(search_term)
    return render_template('index.html', events=events)


#                              FUNÇÕES AUXILIARES 

# funcao para a pesquisa 
def search_events(search_term):
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM events WHERE name LIKE ? OR description LIKE ? OR mes LIKE? OR dia LIKE ?", ('%'+search_term+'%', '%'+search_term+'%' ,'%'+search_term+'%', '%'+search_term+'%'))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)
        return None
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    home()