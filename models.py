from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import re


db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mdps = db.Column(db.String(120), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.mdps = password

    @staticmethod
    def register(email, password):
        if User.query.filter_by(email=email).first():
            return None  # L'email existe déjà
        
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$'
        if not re.match(pattern, password):
            return None  # Le mot de passe ne respecte pas les critères de sécurité
        
        user = User(email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def check_login(email, pwd):
        """Retourne l'utilisateur s'il existe et que le mot de passe est correct, sinon None"""
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.mdps, pwd):
            return user
        return None




class Commande(db.Model):
    __tablename__ = 'commandes'

    # Colonnes basées strictement sur ton dump SQL
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    montant_total = db.Column(db.Numeric(8, 2), nullable=False)

    # Relations pour faciliter le code
    client = db.relationship('User', backref='mes_commandes')
    billets = db.relationship('Ticket', backref='la_commande', cascade="all, delete-orphan")

    def __init__(self, user_id, quantite, montant_total, reference=None):
        self.user_id = user_id
        self.quantite = quantite
        self.montant_total = montant_total
        # Génère une référence auto si non fournie
        self.reference = reference or f"CMD-{datetime.now().strftime('%y%m%d%H%M%S')}"

    # --- FONCTIONS UTILES ---

    def save_to_db(self):
        """Enregistre la commande en respectant les règles SQL."""
        # Vérification de la contrainte CHECK (quantite >= 1 AND <= 4) du SQL
        if 1 <= self.quantite <= 4:
            db.session.add(self)
            db.session.commit()
            return True
        else:
            print("Erreur : La quantité doit être entre 1 et 4.")
            return False

    @staticmethod
    def get_by_reference(ref):
        """Retrouve une commande par sa référence unique."""
        return Commande.query.filter_by(reference=ref).first()
    


class Ticket(db.Model):
    __tablename__ = 'tickets'

    # Colonnes basées sur ton dump SQL
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commandes.id', ondelete='CASCADE'), nullable=False)
    spectacle_id = db.Column(db.Integer, db.ForeignKey('spectacles.id'), nullable=False)

    # Relations pour naviguer facilement dans ton code
    # Permet de faire ticket.spectacle.titre pour avoir le nom du spectacle
    spectacle = db.relationship('Spectacle', backref='tickets_vendus')

    def __init__(self, commande_id, spectacle_id):
        self.commande_id = commande_id
        self.spectacle_id = spectacle_id

    # --- FONCTIONS UTILES ---

    def details(self):
        """Affiche les infos du billet proprement."""
        return f"Ticket #{self.id} - Spectacle: {self.spectacle.titre} (Date: {self.spectacle.date})"

    @staticmethod
    def generer_tickets(commande_obj, spectacle_id):
        """
        Crée autant de tickets que la quantité indiquée dans la commande.
        Ex: Si l'utilisateur a commandé 3 places, on génère 3 lignes dans la table tickets.
        """
        tickets_crees = []
        for _ in range(commande_obj.quantite):
            nouveau_ticket = Ticket(commande_id=commande_obj.id, spectacle_id=spectacle_id)
            db.session.add(nouveau_ticket)
            tickets_crees.append(nouveau_ticket)
        
        db.session.commit()
        return tickets_crees
    
class GrandSpectacle(db.Model):
    __tablename__ = 'grand_spectacle'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(500))  # URL de l'image

    
    # Relation : permet de faire mon_grand_spectacle.representations
    representations = db.relationship('Spectacle', backref='parent', lazy=True)
    
    @staticmethod
    def lister_tous():
        return GrandSpectacle.query.all()


class Spectacle(db.Model):
    __tablename__ = 'spectacles'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    lieu = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Numeric(8, 2), nullable=False)
    grand_spectacle_id = db.Column(db.Integer, db.ForeignKey('grand_spectacle.id'))

    @staticmethod
    def trouver_par_lieu(nom_lieu):
        """Filtre les spectacles qui se jouent à un endroit précis."""
        return Spectacle.query.filter_by(lieu=nom_lieu).all()

    @staticmethod
    def prochaines_dates():
        """Affiche les spectacles à venir (du plus proche au plus lointain)."""
        return Spectacle.query.filter(Spectacle.date >= datetime.today()).order_by(Spectacle.date.asc()).all()

    def modifier_prix(self, nouveau_prix):
        """Permet de mettre à jour le tarif d'une séance."""
        self.prix = nouveau_prix
        db.session.commit()


class Avis(db.Model):
    __tablename__ = 'avis'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    grand_spectacle_id = db.Column(db.Integer, db.ForeignKey('grand_spectacle.id'), nullable=False)
    commentaire = db.Column(db.String(900))

    def publier(self):
        """Enregistre le commentaire s'il n'est pas vide."""
        if self.commentaire and len(self.commentaire) > 2:
            db.session.add(self)
            db.session.commit()
            return True
        return False