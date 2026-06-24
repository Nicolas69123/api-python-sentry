"""Connexion reutilisable a la base MySQL/MariaDB 'magasin' (XAMPP)."""
import mysql.connector


def get_connection():
    """Ouvre et retourne une connexion active vers la base 'magasin'."""
    return mysql.connector.connect(
        host="localhost",   # MySQL tourne en local
        user="root",        # utilisateur XAMPP
        password="",        # mot de passe vide sur XAMPP
        database="magasin", # base reutilisee du cours precedent
        port=3306,          # port standard MySQL
    )
