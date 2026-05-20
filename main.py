from flask import Flask, flash, redirect, render_template, request, session
from datetime import datetime
import os
import re

from models.extensions import db, bcrypt
from models.user import User
from models.spectacle import GrandSpectacle, Spectacle
from models.avis import Avis
from models.commande import Commande
from models.ticket import Ticket


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres123@localhost/tickets_spectacle'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(32).hex()

db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    print("Connexion OK")

@app.route('/')
def index():
    grands = GrandSpectacle.lister_tous()
    return render_template('accueil.html', spectacles=grands, query=None)

@app.route('/recherche')
def recherche():
    query = request.args.get('q', '').strip()
    # Protection XSS : on nettoie la recherche avant de l'utiliser
    query = re.sub(r'<[^>]*>', '', query)
    if query:
        spectacles = GrandSpectacle.rechercher(query)
    else:
        spectacles = GrandSpectacle.lister_tous()
    return render_template('accueil.html', spectacles=spectacles, query=query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            flash("Email invalide", "error")
            return redirect('/login')

        if 'login_attempts' not in session:
            session['login_attempts'] = 0
        if session['login_attempts'] > 5:
            return "Trop de tentatives", 429
        
        user = User.check_login(email, password)
        if user is not None:
            session.clear()
            session['user_id'] = user.id
            session['email'] = user.email
            session['panier'] = {}
            return redirect('/')
        
        session['login_attempts'] += 1
        flash("Email ou mot de passe incorrect", "error")        
        return redirect('/login')
    
    session['login_attempts'] = 0
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            flash("Email invalide", "error")
            return redirect('/register')

        result = User.register(email, password)
        if "user" in result:
            user = result["user"]
            session['user_id'] = user.id
            session['email'] = user.email
            session['panier'] = {}
            flash("Inscription réussie !", "success")
            return redirect('/')
        elif result["error"] == "email_existe":
            flash("Cet email est déjà utilisé", "info")
        elif result["error"] == "mdp_faible":
            flash("Le mot de passe est trop faible", "error")
        return redirect('/register')

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

@app.route('/avis/ajouter/<int:grand_spectacle_id>', methods=['POST'])
def ajouter_avis(grand_spectacle_id):
    if 'user_id' not in session:
        flash("Vous devez être connecté pour laisser un avis", "error")
        return redirect('/login')

    commentaire = request.form.get('commentaire', '').strip()

    avis = Avis(
        utilisateur_id=session['user_id'],
        grand_spectacle_id=grand_spectacle_id,
        commentaire=commentaire
    )

    if avis.publier():
        flash("Avis publié avec succès !", "success")
    else:
        flash("Le commentaire doit faire entre 3 et 900 caractères", "error")

    return redirect(f'/spectacle/{grand_spectacle_id}')

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