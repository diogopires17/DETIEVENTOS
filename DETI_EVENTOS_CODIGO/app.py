from datetime import datetime
import sqlite3
from models import *
from flask import Flask, flash, redirect, render_template, request, session, url_for



app = Flask(__name__)
app.secret_key = 'IDHASIHDAIDHASKPCLS'  

app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 7}

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
    #print(session)
    user_id = get_user_id(session.get('user_email'))
    print(user_id)
    if 'user_email' not in session:
        return redirect(url_for('login'))  
    
    events = get_events()
    
    converted_events = []
    for event in events:
        converted_event = list(event)
        converted_event[5] = datetime.strptime(event[5], '%Y-%m-%d').date()
        converted_events.append(tuple(converted_event))
    converted_events.sort(key=lambda x: x[5])

    user_events = get_user_events(user_id)
    user_events = list(user_events)
    registered_event_ids = [event[1] for event in user_events]
    print(registered_event_ids)
    
    is_admin = 'user_email' in session and session.get('user_email') == "admin@gmail.com"
    name  = session.get('user_name')
    if name is  not None:
        user = True
    event = get_events()
    return render_template('index.html', events=converted_events, is_admin=is_admin, user=user, name=name, event=event,  user_id = user_id, user_events=user_events, registered_event_ids = registered_event_ids)

@app.route('/todos_os_eventos')
def todos_os_eventos():
    #print(session)
    user_id = get_user_id(session.get('user_email'))
    print(user_id)
    if 'user_email' not in session:
        return redirect(url_for('login'))  
    
    events = get_events()
    
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
    event = get_events()
    return render_template('todos_os_eventos.html', events=converted_events, is_admin=is_admin, user=user, name=name, event=event)

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
    if 'user_email' not in session:
        flash("You must be logged in to access this page", category='error')
        return redirect('/login')

    if session['user_email'] != "admin@gmail.com":
        flash("Não tem permissões para aceder aqui", category='error')
        return redirect('/')
    else:
        eventName = request.form['eventName']
        event_description = request.form['eventDescription']
        event_location = request.form['eventLocation']
        #image = request.form['image']
        date = request.form['eventDate']
        event_date = request.form['eventDate']
        #colaborator = request.form['colaborator']
        vagas = 0
        image = 'static/img/mobile.jpg'
        lotacao = request.form['eventCapacity']
        colaborator = 'NEI'
        preco =  request.form['eventPrice']
        connection = sqlite3.connect('data.db', check_same_thread=False)
        cursor = connection.cursor()

        # gets current user id from session
        session_email = session.get('user_email')
        cursor.execute("SELECT id FROM users WHERE email = ?", (session_email,))
        user_id = cursor.fetchone()[0]
        try:
            cursor.execute("INSERT INTO events (name, description, location, date, user_id, colaborator, vagas, lotacao, preco, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (eventName, event_description, event_location, event_date, user_id, colaborator, 0, lotacao, preco, image))           
            connection.commit()
            flash('Event created successfully', category='success')
            return redirect('/')
        except Exception as e:
            print("erro")
            print( e)
            return "An error occurred while creating the event" 
        

@app.route('/meus_eventos')
def meus_eventos():
    # Fetch events associated with user 2
    user_id = get_user_id(session.get('user_email'))
    events = get_user_associated_events(user_id)
    user_img = get_user_img(user_id)

    converted_events = []
    for event in events:
        converted_event = list(event)
        converted_event[5] = datetime.strptime(event[5], '%Y-%m-%d').date()
        converted_events.append(tuple(converted_event))
    
    converted_events.sort(key=lambda x: x[5])
    
    user = 'user_email' in session
    name = session.get('user_name')
    user_events = get_user_events(user_id)
    user_events = list(user_events)
    event = get_events()
    registered_event_ids = [event[1] for event in user_events]
    registered_events = [event for event in converted_events if event[0] in registered_event_ids]



    return render_template('eventos.html', is_admin=False, user_id=2, name=name, user=user, user_events=user_events, event=event, registered_event_ids = registered_event_ids, events=registered_events, user_img=user_img)


@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/search_meus', methods=['GET'])
def searchmeus():
    search_term = request.args.get('q', '')  
    events = search_events(search_term)
    user_id = get_user_id(session.get('user_email'))
    if events is None:
        flash('An error occurred while searching for events', category='error')
        return redirect('/')

    converted_events = []
    for event in events:
        converted_event = list(event)
        converted_event[5] = datetime.strptime(event[5], '%Y-%m-%d').date()
        converted_events.append(tuple(converted_event))
    
    user_events = get_user_events(user_id)
    user_events = list(user_events)

    is_admin = 'user_email' in session and session.get('user_email') == "admin@gmail.com"
    name = session.get('user_name')
    user = 'user_email' in session
    user_id = 2

    return render_template('eventos.html', events=converted_events, is_admin=is_admin, user_id=user_id, name=name, user_events=user_events, user=user)


@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('q', '')  
    events = search_events(search_term)
    user_id = get_user_id(session.get('user_email'))

    if events is None:
        flash('An error occurred while searching for events', category='error')
        return redirect('/')

    converted_events = []
    for event in events:
        converted_event = list(event)
        converted_event[5] = datetime.strptime(event[5], '%Y-%m-%d').date()
        converted_events.append(tuple(converted_event))

    user_events = get_user_events(user_id)
    user_events = list(user_events)
    is_admin = 'user_email' in session and session.get('user_email') == "admin@gmail.com"
    name = session.get('user_name')
    user = 'user_email' in session
    return render_template('index.html', events=converted_events, is_admin=is_admin, user=user, name=name,user_id=user_id, user_events=user_events)


@app.route('/update/<int:event_id>', methods=['GET', 'POST'])
def update_event(event_id):
    if 'user_email' not in session:
        flash("You must be logged in to access this page", category='error')
        return redirect('/login')

    if session['user_email'] != "admin@gmail.com":
        flash("Não tem permissões para aceder aqui", category='error')
        return redirect('/')

    if request.method == 'POST':
        eventName = request.form['eventName']
        eventDescription = request.form['eventDescription']
        eventLocation = request.form['eventLocation']
        eventDate = request.form['eventDate']
        eventCapacity = request.form['eventCapacity']
        eventPrice = request.form['eventPrice']

        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE events 
                SET name=?, description=?, location=?, date=?, lotacao=?, preco=?
                WHERE id=?
            """, (eventName, eventDescription, eventLocation, eventDate, eventCapacity, eventPrice, event_id))
            connection.commit()
            flash('Event updated successfully', category='success')
            return redirect('/')
        except sqlite3.Error as e:
            print("Error updating event:", e)
            flash('An error occurred while updating the event', category='error')
            return redirect('/')
        finally:
            if connection:
                connection.close()

    else:
        events = get_events()
        for event in events:
            if event[0] == event_id:
                eventName = event[1]
                eventDescription = event[2]
                eventLocation = event[3]
                eventDate = event[5]
                eventCapacity = event[9]
                print(eventCapacity)
                eventPrice = event[10]
                print(eventPrice)
                eventImage = event[4]
                print(eventImage)

                return render_template('update.html', eventName=eventName, eventDescription=eventDescription, eventLocation=eventLocation, eventDate=eventDate, eventCapacity=eventCapacity, eventPrice=eventPrice, event_id=event_id, eventImage=eventImage)

        flash('Event not found', category='error')
        return redirect('/')
    
@app.route('/inscrever/<int:event_id>', methods=['POST'])
def inscrever(event_id):
    if 'user_email' not in session:
        flash("You must be logged in to access this page", category='error')
        return redirect('/login')

    user_email = session.get('user_email')
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    user_id = cursor.fetchone()[0]  

    try:
        cursor.execute("INSERT INTO user_events (user_id, event_id) VALUES (?, ?)", (user_id, event_id)) 
        connection.commit()
        flash('Inscrição realizada com sucesso', category='success')
    except sqlite3.IntegrityError:
        flash('Você já está inscrito neste evento', category='error')
    except sqlite3.Error as e:
        print("Error inserting user event:", e)
        flash('An error occurred while registering for the event', category='error')
    finally:
        connection.close()
    
    return redirect('/')


@app.route('/desinscrever/<int:event_id>', methods=['POST'])
def desinscrever(event_id):
    if 'user_email' not in session:
        flash("You must be logged in to access this page", category='error')
        return redirect('/login')

    user_email = session.get('user_email')
    connection = sqlite3.connect('data.db', check_same_thread=False)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    user_id = cursor.fetchone()[0]

    try:
        cursor.execute("DELETE FROM user_events WHERE user_id = ? AND event_id = ?", (user_id, event_id)) 
        connection.commit()
        flash('Desinscrição realizada com sucesso', category='success')
        return redirect('/')
    except sqlite3.Error as e:
        print("Error unsubscribing user from event:", e)
        flash('An error occurred while unsubscribing from the event', category='error')
        return redirect('/')
    finally:
        if connection:
            connection.close()

    
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
        print("ERRO" + e)
        return None
# funcao para ter o id


def get_event_by_id(event_id):
    try:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        event = cursor.fetchone()
        return event
    except sqlite3.Error as e:
        print("Error retrieving event:", e)
        return None
    finally:
        if connection:
            connection.close()

    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    home()