from .extensions import db
import bleach

class Avis(db.Model):
    __tablename__ = 'avis'
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    grand_spectacle_id = db.Column(db.Integer, db.ForeignKey('grand_spectacle.id'), nullable=False)
    commentaire = db.Column(db.String(900))

    def __init__(self, utilisateur_id, grand_spectacle_id, commentaire):
        self.utilisateur_id = utilisateur_id
        self.grand_spectacle_id = grand_spectacle_id
        self.commentaire = commentaire

    def publier(self):
      if self.commentaire:
        # Supprime tout HTML/JavaScript malveillant (protection XSS)
        self.commentaire = bleach.clean(self.commentaire, tags=[], strip=True)
        self.commentaire = self.commentaire.strip()
        # Vérifie la longueur APRÈS nettoyage
        if 2 < len(self.commentaire) <= 900:
            db.session.add(self)
            db.session.commit()
            return True
      return False