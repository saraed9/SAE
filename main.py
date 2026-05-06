from flask import Flask, flash, redirect, render_template, request, session
from datetime import datetime
from models import *
import os

# Configuration de l'application Flask
app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Postgres113@localhost/Spectra'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(32).hex()

# Initialisation de la base de données et de Bcrypt
db.init_app(app)
bcrypt.init_app(app)

# Création de la base de données
with app.app_context():
    db.create_all()
    print("Connexion OK")

# Routes pour les pages principales
@app.route('/')
def index():
    grands = GrandSpectacle.lister_tous()
    return render_template('accueil.html', spectacles=grands)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Contrôle de sécurité : limiter les tentatives de connexion
        if 'login_attempts' not in session:
            session['login_attempts'] = 0
        if session['login_attempts'] > 5:
            return "Trop de tentatives", 429
        
        # Authentification
        user = User.check_login(email, password)
        if user is not None:
            session.clear()  # Réinitialiser les tentatives après une connexion réussie
            session['user_id'] = user.id
            session['email'] = user.email
            session['panier'] = {}
            return redirect('/')
        
        session['login_attempts'] += 1
        flash("Email ou mot de passe incorrect", "error")        
        return redirect('/login')
    
    session['login_attempts'] = 0  # Réinitialiser les tentatives à l'affichage du formulaire
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.register(email, password)
        if user is None:
            flash("Cet email est déjà utilisé", "error")
            return redirect('/register')
        
        session['user_id'] = user.id
        session['email'] = user.email
        session['panier'] = {}
        
        flash("Inscription réussie !", "success")
        return redirect('/')

    return render_template('registration.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/profil')
def profil():
    if 'user_id' not in session:
        flash("Vous devez être connecté pour voir votre profil", "info")
        return redirect('/login')
    
    user = User.query.get(session['user_id'])
    commandes = Commande.get_by_user(session['user_id'])
    return render_template('profil.html', user=user, orders=commandes)

@app.route('/spectacle/<int:id>')
def detail_spectacle(id):
    grand = GrandSpectacle.query.get_or_404(id)
    representations = Spectacle.query.filter_by(grand_spectacle_id=id).all()
    avis = Avis.query.filter_by(grand_spectacle_id=id).all()
    return render_template('detail_spectacle.html', grand=grand, representations=representations, avis=avis)

@app.route('/panier')
def panier():
    if 'user_id' not in session:
        flash("Vous devez être connecté pour accéder à votre panier", "info")
        return redirect('/login')
    
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
        flash("Vous devez être connecté pour ajouter un spectacle à votre panier", "info")
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
        flash("Vous devez être connecté pour payer", "info")
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
        return redirect('/confirmation')

    return render_template('paiement.html')

@app.route('/confirmation')
def confirmation():
    if 'user_id' not in session:
        flash("Vous devez être connecté", "info")
        return redirect('/login')
    
    order = Commande.query.filter_by(user_id=session['user_id']).order_by(Commande.id.desc()).first()
    if not order:
        flash("Aucune commande trouvée", "error")
        return redirect('/')
    
    return render_template('confirmation.html', order=order)

if __name__ == '__main__':
    app.run(debug=False)