from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from models import *

app = Flask(__name__)

# Connexion à PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Postgres113@localhost:5432/Spectra'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cle_secrete_a_changer'

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()
    print("Connexion OK")

@app.route('/')
def index():
    events = GrandSpectacle.lister_tous()
    return render_template('accueil.html', spectacles=events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # ICI : Tu ajouteras plus tard la vérification dans ta base MySQL
        user = User.check_login(email, password)
        if user is not None:
            session['user_id'] = user.id
            session['email'] = user.email
            return redirect('/')
        else:
            flash("Email ou mot de passe incorrect", "error")
        
        print(f"Tentative de connexion de : {email}")
        
        return redirect('/login')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Erreur : Tous les champs sont obligatoires", 400

        user = User.register(email, password)
        if user is None:
            print("Cet email est déjà utilisé", "error")
            return redirect('/register') 
        session['user_id'] = user.id
        session['email'] = user.email

        print(f"Inscription réussie pour : {email}")
        
        return redirect('/')

    return render_template('registration.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect('/')

@app.route('/profil')
def profil():
    # 1. Vérifier si l'utilisateur est connecté
    """
    if 'user_id' not in session:
        return redirect('/login')
    """
    # 2. Récupérer les infos de l'utilisateur
    # cursor.execute("SELECT nom, prenom, email FROM utilisateurs WHERE id = %s", (session['user_id'],))
    user_info = {"email": "jean.dupont@email.com"}

    # 3. Récupérer l'historique des commandes (Exemple de structure)
    # Ta requête SQL ressemblera à : 
    # SELECT o.id, o.date, o.total, o.status FROM orders o WHERE o.user_id = %s
    orders_history = [
        {"id": "12345", "date": "23/04/2026", "total": 140, "status": "Confirmé"},
        {"id": "12344", "date": "15/04/2026", "total": 55, "status": "Confirmé"}
    ]

    return render_template('profil.html', user=user_info, orders=orders_history)

@app.route('/panier')
def afficher_panier():
    # On simule un panier stocké en session
    # { id_spectacle: quantite }
    if 'panier' not in session:
        session['panier'] = {1: 1, 2: 2} # Données de test
    
    # On récupère les vraies infos des spectacles (normalement via ta BDD)
    tous_les_spectacles = {
        1: {"title": "Le Roi Lion", "price": 45, "location": "Zénith de Paris", "date": "15/10/2024"},
        2: {"title": "Stromae en Concert", "price": 45, "location": "AccorHotels Arena", "date": "22/10/2024"}
    }
    
    # On prépare la liste pour le HTML
    cart_items = []
    total = 0
    for id_sp, quantite in session['panier'].items():
        id_sp = int(id_sp)
        info = tous_les_spectacles[id_sp]
        sous_total = info['price'] * quantite
        total += sous_total
        cart_items.append({
            "id": id_sp,
            "title": info['title'],
            "price": info['price'],
            "quantity": quantite,
            "location": info['location'],
            "date": info['date'],
            "subtotal": sous_total
        })

    return render_template('panier.html', items=cart_items, total=total)
    
@app.route('/paiement', methods=['GET', 'POST']) # Ajoute GET ici !
def paiement():
    # Ici on traite le formulaire de carte bancaire
    """
    if 'user_email' not in session:
        flash("Vous devez être connecté pour payer", "error")
        return redirect('/login')
    """
    if request.method == 'POST':
        # On récupère les infos (pour la simulation)
        card_num = request.form.get('card_number')
        
        # 1. ICI : Tu ferais ton "INSERT INTO commandes ..." dans MySQL
        # 2. ICI : Tu récupères l'ID de la commande générée
        
        # 3. On vide le panier après le succès
        session.pop('panier', None)
        
        flash("Paiement accepté ! Votre commande est en route.", "success")
        return redirect('/confirmation')
    
    # Si c'est en GET, on affiche juste la page
    return render_template('paiement.html')

@app.route('/confirmation')
def confirmation():
    # En vrai, ces infos viendront de ta BDD après l'achat
    order_data = {
        "number": "12345",
        "date": datetime.now().strftime("%d/%m/%Y"),
        "payment": "Carte Visa ****1234",
        "tickets": [
            {"title": "Le Roi Lion", "date": "15/10/2024", "location": "Zénith de Paris", "quantity": 1, "price": 45},
            {"title": "Stromae en Concert", "date": "22/10/2024", "location": "AccorHotels Arena", "quantity": 2, "price": 90}
        ],
    }
    total = sum(t['price'] for t in order_data['tickets'])
    
    return render_template('confirmation.html', order=order_data, total=total)

if __name__ == '__main__':
    app.run(debug=False)