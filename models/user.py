from .extensions import db, bcrypt
import re

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
            return {"error": "email_existe"} # L'email existe déjà
        
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$'
        if not re.match(pattern, password):
            return {"error": "mdp_faible"}  # Le mot de passe ne respecte pas les critères de sécurité
        
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return {"user": user}

    @staticmethod
    def check_login(email, pwd):
        """Retourne l'utilisateur s'il existe et que le mot de passe est correct, sinon None"""
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.mdps, pwd):
            return user
        return None