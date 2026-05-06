from .extensions import db

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