from .extensions import db

class PanierItem(db.Model):
    __tablename__ = 'panier_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    spectacle_id = db.Column(db.Integer, db.ForeignKey('spectacles.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False, default=1)
    
    spectacle = db.relationship('Spectacle', backref='panier_items')
    user = db.relationship('User', backref='panier_items')
    
    def __init__(self, user_id, spectacle_id, quantite=1):
        self.user_id = user_id
        self.spectacle_id = spectacle_id
        self.quantite = quantite