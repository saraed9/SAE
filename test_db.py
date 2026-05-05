from main import app, db
from models import User, Spectacle, Commande, Ticket, Avis

with app.app_context():
    print("=== TEST BASE DE DONNÉES ===\n")

    users = User.query.all()
    print(f"👤 Utilisateurs ({len(users)}) :")
    for u in users:
        print(f"   - ID: {u.id} | Email: {u.email}")

    spectacles = Spectacle.query.all()
    print(f"\n🎭 Spectacles ({len(spectacles)}) :")
    for s in spectacles:
        print(f"   - ID: {s.id} | Titre: {s.titre} | Prix: {s.prix}€")

    print("\n✅ Connexion BDD OK !")