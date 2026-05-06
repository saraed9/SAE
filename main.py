from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:141039@localhost/tickets_spectacle'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cle_secrete_a_changer'

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()
    print("Connexion OK")

@app.route('/')
def index():
    grands = GrandSpectacle.lister_tous()
    return render_template('accueil.html', spectacles=grands)

@app.route('/spectacle/<int:id>')
def detail_spectacle(id):
    grand = GrandSpectacle.query.get_or_404(id)
    representations = Spectacle.query.filter_by(grand_spectacle_id=id).all()
    avis = Avis.query.filter_by(grand_spectacle_id=id).all()
    return render_template('detail_spectacle.html', grand=grand, representations=representations, avis=avis)
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
    if 'user_id' not in session:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    commandes = Commande.get_by_user(session['user_id'])
    return render_template('profil.html', user=user, orders=commandes)

@app.route('/panier')
def afficher_panier():
    if 'panier' not in session:
        session['panier'] = {}

    cart_items = []
    total = 0
    for id_sp, quantite in session['panier'].items():
        spectacle = Spectacle.par_id(int(id_sp))
        if spectacle:
            sous_total = float(spectacle.prix) * quantite
            total += sous_total
            cart_items.append({
                "id": spectacle.id,
                "title": spectacle.titre,
                "price": float(spectacle.prix),
                "quantity": quantite,
                "location": spectacle.lieu,
                "date": spectacle.date,
                "subtotal": sous_total
            })

    return render_template('panier.html', items=cart_items, total=total)

@app.route('/panier/ajouter/<int:spectacle_id>')
def ajouter_panier(spectacle_id):
    if 'user_id' not in session:
        return redirect('/login')
    if 'panier' not in session:
        session['panier'] = {}
    panier = session['panier']
    cle = str(spectacle_id)
    if cle in panier:
        if panier[cle] < 4:
            panier[cle] += 1
    else:
        panier[cle] = 1
    session['panier'] = panier
    return redirect('/panier')

@app.route('/paiement', methods=['GET', 'POST'])
def paiement():
    if 'user_id' not in session:
        flash("Vous devez être connecté pour payer", "error")
        return redirect('/login')

    if request.method == 'POST':
        panier = session.get('panier', {})
        total = 0
        quantite_totale = 0

        for id_sp, quantite in panier.items():
            spectacle = Spectacle.par_id(int(id_sp))
            if spectacle:
                total += float(spectacle.prix) * quantite
                quantite_totale += quantite

        nouvelle_commande = Commande(
            user_id=session['user_id'],
            quantite=quantite_totale,
            montant_total=total
        )
        nouvelle_commande.save()
        session.pop('panier', None)
        flash("Paiement accepté ! Votre commande est en route.", "success")
        return redirect('/confirmation')

    return render_template('paiement.html')

@app.route('/confirmation')
def confirmation():
    order_data = {
        "number": "12345",
        "date": datetime.datetime.now().strftime("%d/%m/%Y"),
        "payment": "Carte Visa ****1234",
        "tickets": [],
    }
    total = 0
    return render_template('confirmation.html', order=order_data, total=total)

if __name__ == '__main__':
    app.run(debug=False)