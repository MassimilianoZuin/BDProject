from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user, login_remembered
from sqlalchemy import *
import os.path
import sys
from Login import LoginBP

app = Flask(__name__)
app.register_blueprint(LoginBP)
app.config['SECRET_KEY'] = 'ubersecret'
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):  # costruttore di classe
    def __init__(self, id, email, nome, cognome, nick, birthday, Password):  # active=True
        self.id = id
        self.email = email
        self.nome = nome
        self.cognome = cognome
        self.nick = nick
        self.birthday = birthday
        self.Password = Password
        # self.active = active


def get_user_by_email(email):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Utenti WHERE Email = ?', email)
    user = rs.fetchone()
    conn.close()
    return User(user.Id_Utenti, user.Email, user.Nome, user.Cognome, user.Nickname, user.Data_Nascita, user.Password)


@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    rs = conn.execute('SELECT * FROM Utenti WHERE Id_Utenti = ?', user_id)
    user = rs.fetchone()
    conn.close()
    return User(user.Id_Utenti, user.Email, user.Nome, user.Cognome, user.Nickname, user.Data_Nascita, user.Password)

'''
export FLASK_APP=Login.py
export FLASK_ENV=development
flask run

set FLASK_APP=Login.py
set FLASK_ENV=development
$env:FLASK_APP = "Login.py"
flask run
'''
'''
# Controllo che esista database e, in caso non esistesse, lo genero
try:
    os.path.realpath('database.bd', strict=True)
except:
    # Il database manca, quindi provo a generarlo. Controllo che ci sia il file csv per farlo
    # Se non c'è il file csv, mando una eccezione
    try:
        os.path.realpath('./songdb.csv', strict=True)
    except:
        raise Exception('Manca il file csv per generare il database')
    if(sys.version_info[0]<3):
        execfile('gendb.py')
        execfile('popdb.py')
    else:
        exec(open('gendb.py').read())
        exec(open('popdb.py').read())
'''