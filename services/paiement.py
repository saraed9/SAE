from datetime import datetime
from flask import flash

def verifCarte(form):
    card_name = form.get('card_name').strip()
    card_number = form.get('card_number').replace(" ", "")
    expiry = form.get('card_expiry').strip()
    cvv = form.get('card_cvv').strip()

    # Vérification du nom sur la carte
    if not card_name or len(card_name) < 2:
        flash("Le nom sur la carte n'est pas valie. (minimum 2 caractères)", "error")
        return False

    # Vérification du numéro de carte 
    if not card_number.isdigit() or len(card_number) != 16:
        flash("Numéro de carte invalide. Il doit contenir exactement 16 chiffres.", "error")
        return False
    
    if not verifNumCarte(card_number):
        flash("Numéro de carte invalide. Le numéro ne respecte pas l'algorithme de Luhn.", "error")
        return False

    # Vérification de la date d'expiration
    if not verifDateExpiration(expiry):
        return False
    
    # Vérification du code CVV
    if not cvv.isdigit() or len(cvv) != 3:
        flash("Code CVV invalide. Il doit contenir exactement 3 chiffres.", "error")
        return False

    return True

def verifNumCarte(numero_carte):
    """Vérifie si un numéro de carte est mathématiquement valide (Algorithme de Luhn)."""
    somme = 0
    alterne = False
    
    # On parcourt les chiffres en partant de la fin
    for chiffre in reversed(numero_carte):
        num = int(chiffre)
        if alterne:
            num *= 2
            if num > 9:
                num -= 9
        somme += num
        alterne = not alterne
        
    return (somme % 10 == 0)

def verifDateExpiration(expiry):
    if not expiry or '/' not in expiry:
        flash("Format de date d'expiration invalide (attendu: MM/AA).", "error")
        return False
    
    parts = expiry.split('/')
    month = int(parts[0])
    year = int(parts[1]) + 2000 # On transforme '26' en '2026' pour comparer les dates

    # Validation du mois et vérification que la carte n'est pas expirée
    current_year = datetime.now().year
    current_month = datetime.now().month

    if month < 1 or month > 12:
        flash("Date d'expiration invalide (MM/AA).", "error")
        return False
    
    if year < current_year or (year == current_year and month < current_month):
        flash("La carte bancaire est expirée.", "error")
        return False

    return True

from models.commande import Commande
from models.ticket import Ticket
from models.panier import PanierItem
from models.extensions import db # Importe ton instance SQLAlchemy

def executer_commande(user_id, donnees_panier):
    """Enregistre la commande, génère les tickets et vide le panier en BDD."""
    try:
        # 1. Création de la commande
        nouvelle_commande = Commande(
            user_id=user_id,
            quantite=donnees_panier['nombre_billets'],
            montant_total=donnees_panier['montant_total']
        )
        nouvelle_commande.save() # Sauvegarde initiale pour obtenir l'ID

        # 2. Génération des tickets individuels
        items_panier = PanierItem.query.filter_by(user_id=user_id).all()
        for item in items_panier:
            Ticket.generer(
                commande_id=nouvelle_commande.id, 
                spectacle_id=item.spectacle_id, 
                quantite=item.quantite
            )

        # 3. Vidage du panier de l'utilisateur
        PanierItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        return nouvelle_commande.id
    except Exception as e:
        db.session.rollback()
        print(f"Erreur lors du traitement de la commande : {e}")
        return None