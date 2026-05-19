from flask import Flask, flash, redirect, render_template, request, session
from datetime import datetime
import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models.extensions import db, bcrypt
from models.user import User
from models.spectacle import GrandSpectacle, Spectacle
from models.avis import Avis
from models.commande import Commande
from models.ticket import Ticket
from models.panier import PanierItem


# Configuration de l'application Flask
app = Flask(__name__)

# Configuration du rate limiter pour limiter les requêtes par adresse IP
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"     # stockage en mémoire vive du serveur
)

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
@limiter.limit("5 per minute", exempt_when=lambda: request.method == "GET", error_message="Trop de tentatives de connexion. Veuillez réessayer dans 1 minute.")  # Limite de 5 tentatives de connexion par minute
def login():
    if 'user_id' in session:
        return redirect('/profil')

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Authentification
        user = User.check_login(email, password)
        if user is not None:
            session.clear()  # Réinitialiser les tentatives après une connexion réussie
            session['user_id'] = user.id
            session['email'] = user.email
            return redirect('/')
        
        flash("Email ou mot de passe incorrect", "error")        
        return redirect('/login')
    
    return render_template('login.html')

@app.route('/forgot_password')
def forgot_password():
    flash("Sorry... La réinitialisation par email est désactivée sur cet environnement de test.", "info")
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect('/profil')
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        result = User.register(email, password)
        if "user" in result:
            user = result["user"]
            session['user_id'] = user.id
            session['email'] = user.email
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

@app.route('/panier')
def panier():
    if 'user_id' not in session:
        flash("Vous devez être connecté pour accéder à votre panier", "info")
        return redirect('/login')
    
    panier = PanierItem.query.filter_by(user_id=session['user_id']).order_by(PanierItem.id).all()

    cart_items = []
    total = 0
    for item in panier:
        spectacle = Spectacle.par_id(item.spectacle_id)
        if spectacle:
            sous_total = float(spectacle.prix) * item.quantite
            total += sous_total
            cart_items.append({
                "id": spectacle.id,
                "title": spectacle.titre,
                "price": float(spectacle.prix),
                "quantity": item.quantite,
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
    
    user_id = session['user_id']
    item = PanierItem.query.filter_by(user_id=user_id, spectacle_id=spectacle_id).first()
    if item:
        if item.quantite < 4:
            item.quantite += 1
        else:
            flash("Vous ne pouvez pas ajouter plus de 4 billets pour ce spectacle", "error")
            return redirect('/panier')
    else:
        item = PanierItem(user_id=user_id, spectacle_id=spectacle_id, quantite=1)
        db.session.add(item)
    
    db.session.commit()
    return redirect('/panier')

@app.route('/panier/diminuer/<int:spectacle_id>')
def diminuer_panier(spectacle_id):
    if 'user_id' not in session:
        flash("Vous devez être connecté pour modifier votre panier", "info")
        return redirect('/login')
    
    item = PanierItem.query.filter_by(user_id=session['user_id'], spectacle_id=spectacle_id).first()
    if item:
        if item.quantite > 1:
            item.quantite -= 1
        else:
            db.session.delete(item)
        db.session.commit()
    return redirect('/panier')

@app.route('/panier/supprimer/<int:spectacle_id>')
def supprimer_panier(spectacle_id):
    if 'user_id' not in session:
        flash("Vous devez être connecté pour modifier votre panier", "info")
        return redirect('/login')
    
    item = PanierItem.query.filter_by(user_id=session['user_id'], spectacle_id=spectacle_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Spectacle supprimé du panier", "info")
    return redirect('/panier')

@app.route('/paiement', methods=['GET', 'POST'])
def paiement():
    if 'user_id' not in session:
        flash("Vous devez être connecté pour payer", "info")
        return redirect('/login')

    panier = PanierItem.query.filter_by(user_id=session['user_id']).all()
    if not panier:
        flash("Votre panier est vide", "info")
        return redirect('/panier')
    
    if request.method == 'POST':
        total = 0
        quantite_totale = 0
        for item in panier:
            if item.quantite < 1 or item.quantite > 4:
                flash("Limite de 4 billets maximum par spectacle dépassée.", "error")
                return redirect('/panier')
            
            spectacle = Spectacle.par_id(item.spectacle_id)
            if spectacle:
                total += float(spectacle.prix) * item.quantite
                quantite_totale += item.quantite

        nouvelle_commande = Commande(
            user_id=session['user_id'],
            quantite=quantite_totale,
            montant_total=total
        )
        
        if nouvelle_commande.save():
            for item in panier:
                Ticket.generer(commande_id=nouvelle_commande.id, spectacle_id=item.spectacle_id, quantite=item.quantite)
            
            # Supprime le panier après le paiement réussi
            PanierItem.query.filter_by(user_id=session['user_id']).delete()
            db.session.commit()

            # Stocke l'ID de la commande récente pour la page de confirmation
            session['commande_recente_id'] = nouvelle_commande.id
            flash("Paiement validé !", "success")
            return redirect('/confirmation')
        else:
            flash("Une erreur est survenue lors du paiement", "error")
            return redirect('/panier')

    return render_template('paiement.html')

@app.route('/confirmation')
def confirmation():
    if 'user_id' not in session:
        flash("Vous devez être connecté", "info")
        return redirect('/login')
    
    commande_id = session.pop('commande_recente_id', None)
    if not commande_id:
        flash("Aucune commande payée récemment", "info")
        return redirect('/')

    order = Commande.query.filter_by(user_id=session['user_id']).order_by(Commande.id.desc()).first()
    if not order:
        flash("Aucune commande trouvée", "error")
        return redirect('/')
    
    cpt_spectacles = {}
    for ticket in order.tickets:
        cpt_spectacles[ticket.spectacle_id] = cpt_spectacles.get(ticket.spectacle_id, 0) + 1

    details = []
    for id_sp, quantite in cpt_spectacles.items():
        spectacle = Spectacle.par_id(int(id_sp))
        if spectacle:
            details.append({
                'spectacle': spectacle,
                'quantite': quantite,
                'sous_total': float(spectacle.prix) * quantite
            })
            
    return render_template('confirmation.html', order=order, details=details)
    

if __name__ == '__main__':
    app.run(debug=False)