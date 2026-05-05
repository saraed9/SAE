from main import app
from extensions import db, bcrypt
from models import User

with app.app_context():
    users = User.query.all()
    for user in users:
        # On vérifie si le mot de passe n'est pas déjà hashé
        if not user.mdps.startswith('$2b$'):
            user.mdps = bcrypt.generate_password_hash(user.mdps).decode('utf-8')
            print(f" {user.email} hashé")
        else:
            print(f" {user.email} déjà hashé")
    db.session.commit()
    print("\nTerminé !")