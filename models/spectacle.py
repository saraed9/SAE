from .extensions import db
from datetime import datetime

class GrandSpectacle(db.Model):
    __tablename__ = 'grand_spectacle'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500))
    description = db.Column(db.String(1000))
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
