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
    
    @classmethod
    def getPanierComplet(self, user_id):
        """Calcule les totaux et extrait les détails du panier d'un utilisateur."""
        from models.spectacle import Spectacle  # Évite les imports circulaires
        
        panier = self.query.filter_by(user_id=user_id).order_by(self.id).all()
        cart_items = []
        total = 0
        quantite_totale = 0

        for item in panier:
            spectacle = Spectacle.par_id(item.spectacle_id)
            if spectacle:
                sous_total = float(spectacle.prix) * item.quantite
                total += sous_total
                quantite_totale += item.quantite
                cart_items.append({
                    "id": spectacle.id,
                    "titre": spectacle.titre,
                    "price": float(spectacle.prix),
                    "quantity": item.quantite,
                    "location": spectacle.lieu,
                    "date": spectacle.date,
                    "subtotal": sous_total
                })

        return {
            "items": cart_items,
            "montant_total": total,
            "quantite_totale": quantite_totale,
            "items_raw": panier
        }