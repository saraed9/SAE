from models.commande import Commande

from .extensions import db

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commandes.id', ondelete='CASCADE'), nullable=False)
    spectacle_id = db.Column(db.Integer, db.ForeignKey('spectacles.id'), nullable=False)
    spectacle = db.relationship('Spectacle', backref='tickets')

    def __init__(self, commande_id, spectacle_id):
        self.commande_id = commande_id
        self.spectacle_id = spectacle_id

    @staticmethod
    def generer(commande_id, spectacle_id, quantite):
        tickets = []
        for _ in range(quantite):
            t = Ticket(commande_id=commande_id, spectacle_id=spectacle_id)
            db.session.add(t)
            tickets.append(t)
        db.session.commit()
        return tickets
    
    @staticmethod
    def count_by_user_and_spectacle(user_id, spectacle_id):
        return db.session.query(Ticket).join(Commande).filter(
            Commande.user_id == user_id,
            Ticket.spectacle_id == spectacle_id
        ).count()
