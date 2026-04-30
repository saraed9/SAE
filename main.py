from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Connexion à PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:141039@localhost/tickets_spectacle'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cle_secrete_a_changer'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

@app.route('/')
def hello():
    return render_template('accueil.html')

if __name__ == '__main__':
    app.run(debug=True)