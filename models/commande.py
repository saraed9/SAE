from .extensions import db
from datetime import datetime

class Commande(db.Model):
    __tablename__ = 'commandes'
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    montant_total = db.Column(db.Numeric(8, 2), nullable=False)

    # Relations pour faciliter le code
    client = db.relationship('User', backref='mes_commandes')
    tickets = db.relationship('Ticket', backref='commande', cascade="all, delete-orphan")

    def __init__(self, user_id, quantite, montant_total):
        self.user_id = user_id
        self.quantite = quantite
        self.montant_total = montant_total
        self.reference = f"CMD-{datetime.now().strftime('%y%m%d%H%M%S')}"

    def save(self):
        if self.quantite >= 1:
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

