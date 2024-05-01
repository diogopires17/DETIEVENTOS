from datetime import datetime
import sqlite3
from models import *
from flask import Flask, flash, redirect, render_template, request, session, url_for



app = Flask(__name__)
app.secret_key = 'IDHASIHDAIDHASKPCLS'  


init_db()


@app.template_filter('formatdate')
def format_date(value, format='%d-%B'):
    if value is None:
        return ""
    month_names = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
        'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
        'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
        'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
    }
    formatted_date = value.strftime(format)
    for eng, pt in month_names.items():
        formatted_date = formatted_date.replace(eng, pt)
    return formatted_date


@app.route('/')
def home():
    print(session)
    if 'user_email' not in session:
        return redirect(url_for('login'))  # Redirect to the login page if user is not logged in
    
    events = get_events()
    
    # Convert the date strings to datetime objects
    converted_events = []
    for event in events:
        converted_event = list(event)
        converted_event[5] = datetime.strptime(event[5], '%Y-%m-%d').date()
        converted_events.append(tuple(converted_event))
    converted_events.sort(key=lambda x: x[5])
    
    is_admin = 'user_email' in session and session.get('user_email') == "admin@gmail.com"
    name  = session.get('user_name')
    if name is  not None:
        user = True
    return render_template('index.html', events=converted_events, is_admin=is_admin, user=user, name=name)



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
            session['user_email'] = email 
            session['user_password'] = password 
            session['user_name'] = user_name 
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/criar', methods=['POST'])
def criar():
    # Check if the user is logged in
    if 'user_email' not in session:
        flash("You must be logged in to access this page", category='error')
        return redirect('/login')

    # Check if the user is an admin
    if session['user_email'] != "admin@gmail.com":
        flash("Não tem permissões para aceder aqui", category='error')
        return redirect('/')
    else:
        event_date = request.form['eventDate']
        event_description = request.form['eventDescription']

        connection = sqlite3.connect('data.db', check_same_thread=False)
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO events (date, description) VALUES (?, ?)", (event_date, event_description))
            connection.commit()
            return "Event created successfully"
        except Exception as e:
            print(e)
            return "An error occurred while creating the event" 
        
        
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

    if events is None:
        flash('An error occurred while searching for events', category='error')
        return redirect('/')

    # Convert the date strings to datetime objects
    converted_events = []
    for event in events:
        converted_event = list(event)
        converted_event[5] = datetime.strptime(event[5], '%Y-%m-%d').date()
        converted_events.append(tuple(converted_event))

    return render_template('index.html', events=converted_events)

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    session.pop('user_password', None)
    session.pop('user_name', None)
    return redirect('/login')

#                              FUNÇÕES AUXILIARES 

# funcao para a pesquisa 
def search_events(search_term):
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM events WHERE name LIKE ? OR description LIKE ? ", ('%'+search_term+'%', '%'+search_term+'%'))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)
        return None
    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    home()