"""
Couche d'acces aux donnees : toutes les requetes SQL sur la table 'produits'.
Chaque fonction ouvre une connexion, execute sa requete, ferme proprement.
"""
from decimal import Decimal

from database import get_connection


def _normaliser(produit):
    """Convertit le prix (Decimal MySQL) en float pour la serialisation JSON."""
    if produit and isinstance(produit.get("prix"), Decimal):
        produit["prix"] = float(produit["prix"])
    return produit


def get_all_products():
    """Retourne tous les produits (liste de dictionnaires)."""
    connexion = get_connection()
    curseur = connexion.cursor(dictionary=True)
    curseur.execute("SELECT id, nom, prix, stock FROM produits")
    produits = curseur.fetchall()
    curseur.close()
    connexion.close()
    return [_normaliser(p) for p in produits]


def get_product_by_id(product_id):
    """Retourne un produit precis, ou None s'il n'existe pas."""
    connexion = get_connection()
    curseur = connexion.cursor(dictionary=True)
    curseur.execute(
        "SELECT id, nom, prix, stock FROM produits WHERE id = %s",
        (product_id,),
    )
    produit = curseur.fetchone()
    curseur.close()
    connexion.close()
    return _normaliser(produit)


def create_product(nom, prix, stock):
    """Insere un nouveau produit et retourne son id."""
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute(
        "INSERT INTO produits (nom, prix, stock) VALUES (%s, %s, %s)",
        (nom, prix, stock),
    )
    connexion.commit()
    nouvel_id = curseur.lastrowid
    curseur.close()
    connexion.close()
    return nouvel_id


def update_product(product_id, nom, prix, stock):
    """Modifie un produit existant. Retourne le nombre de lignes affectees."""
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute(
        "UPDATE produits SET nom = %s, prix = %s, stock = %s WHERE id = %s",
        (nom, prix, stock, product_id),
    )
    connexion.commit()
    lignes = curseur.rowcount
    curseur.close()
    connexion.close()
    return lignes


def delete_product(product_id):
    """Supprime un produit. Retourne le nombre de lignes affectees."""
    connexion = get_connection()
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM produits WHERE id = %s", (product_id,))
    connexion.commit()
    lignes = curseur.rowcount
    curseur.close()
    connexion.close()
    return lignes
