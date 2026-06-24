"""
API REST Flask connectee a MySQL, documentee avec Swagger (Flask-RESTX).
Lancer : python app.py  ->  Swagger sur http://127.0.0.1:5000/swagger
"""
import os

import sentry_sdk
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields

from product_repository import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
)

# --- Sentry ---
# Le DSN est lu depuis la variable d'environnement SENTRY_DSN (jamais en dur).
# Sans DSN, Sentry reste inactif : l'API fonctionne normalement.
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    send_default_pii=True,        # joint le contexte requete aux erreurs
    traces_sample_rate=1.0,       # tracing performance (100% en dev)
)

app = Flask(__name__)
CORS(app)  # autorise les appels depuis un frontend / Swagger

api = Api(
    app,
    version="1.0",
    title="API Produits",
    description="API Python Flask connectee a MySQL/phpMyAdmin",
    doc="/swagger",  # interface Swagger sur /swagger
)

# Namespace = groupe de routes sous le prefixe /products
ns = api.namespace("products", description="Operations CRUD sur les produits")

# Modele decrivant un produit dans Swagger (sert a la doc + validation entree)
product_model = api.model(
    "Product",
    {
        "nom": fields.String(required=True, description="Nom du produit"),
        "prix": fields.Float(required=True, description="Prix en euros"),
        "stock": fields.Integer(required=True, description="Quantite en stock"),
    },
)


@ns.route("")
class ProductList(Resource):
    @ns.doc("lister_produits")
    def get(self):
        """Liste tous les produits."""
        return get_all_products(), 200

    @ns.doc("creer_produit")
    @ns.expect(product_model)
    def post(self):
        """Cree un nouveau produit."""
        data = api.payload
        nouvel_id = create_product(data["nom"], data["prix"], data["stock"])
        return {"message": "Produit cree", "id": nouvel_id}, 201


@ns.route("/<int:product_id>")
@ns.param("product_id", "Identifiant du produit")
class Product(Resource):
    @ns.doc("lire_produit")
    def get(self, product_id):
        """Recupere un produit par son id."""
        produit = get_product_by_id(product_id)
        if produit is None:
            return {"message": "Produit introuvable"}, 404
        return produit, 200

    @ns.doc("modifier_produit")
    @ns.expect(product_model)
    def put(self, product_id):
        """Modifie un produit existant."""
        data = api.payload
        lignes = update_product(product_id, data["nom"], data["prix"], data["stock"])
        if lignes == 0:
            return {"message": "Produit introuvable"}, 404
        return {"message": "Produit modifie"}, 200

    @ns.doc("supprimer_produit")
    def delete(self, product_id):
        """Supprime un produit."""
        lignes = delete_product(product_id)
        if lignes == 0:
            return {"message": "Produit introuvable"}, 404
        return {"message": "Produit supprime"}, 200


if __name__ == "__main__":
    app.run(debug=True)
