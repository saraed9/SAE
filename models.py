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
        self.mdps = bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def register(email, password):
        if User.query.filter_by(email=email).first():
            return None  # L'email existe déjà
        
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$'
        if not re.match(pattern, password):
            return None  # Le mot de passe ne respecte pas les critères de sécurité
        
        user = User(email=email, password=password)
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


class GrandSpectacle(db.Model):
    __tablename__ = 'grand_spectacle'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500))
    description = db.Column(db.String(1000))
    representations = db.relationship('Spectacle', backref='parent', lazy=True)

    @staticmethod
    def ajouter(nom):
        nouvelle = GrandSpectacle(nom=nom)
        db.session.add(nouvelle)
        db.session.commit()
        return nouvelle

    def lister_dates(self):
        return [r.date for r in self.representations]
    
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
    def tous():
        return Spectacle.query.all()

    @staticmethod
    def par_id(spectacle_id):
        return Spectacle.query.get(spectacle_id)

    @staticmethod
    def prochains():
        return Spectacle.query.filter(
            Spectacle.date >= datetime.today()
        ).order_by(Spectacle.date.asc()).all()


class Commande(db.Model):
    __tablename__ = 'commandes'
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    montant_total = db.Column(db.Numeric(8, 2), nullable=False)

    # Relations pour faciliter le code
    client = db.relationship('User', backref='mes_commandes')
    billets = db.relationship('Ticket', backref='la_commande', cascade="all, delete-orphan")

    def __init__(self, user_id, quantite, montant_total):
        self.user_id = user_id
        self.quantite = quantite
        self.montant_total = montant_total
        self.reference = f"CMD-{datetime.now().strftime('%y%m%d%H%M%S')}"

    def save(self):
        if 1 <= self.quantite <= 4:
            db.session.add(self)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_by_user(user_id):
        return Commande.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_by_id(commande_id):
        return Commande.query.get(commande_id)


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commandes.id', ondelete='CASCADE'), nullable=False)
    spectacle_id = db.Column(db.Integer, db.ForeignKey('spectacles.id'), nullable=False)
    spectacle = db.relationship('Spectacle', backref='tickets_vendus')

    def __init__(self, commande_id, spectacle_id):
        self.commande_id = commande_id
        self.spectacle_id = spectacle_id

    @staticmethod
    def generer(commande, spectacle_id):
        tickets = []
        for _ in range(commande.quantite):
            t = Ticket(commande_id=commande.id, spectacle_id=spectacle_id)
            db.session.add(t)
            tickets.append(t)
        db.session.commit()
        return tickets


class Avis(db.Model):
    __tablename__ = 'avis'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    grand_spectacle_id = db.Column(db.Integer, db.ForeignKey('grand_spectacle.id'), nullable=False)
    commentaire = db.Column(db.String(900))

    def publier(self):
        if self.commentaire and len(self.commentaire) > 2:
            db.session.add(self)
            db.session.commit()
            return True
        return False