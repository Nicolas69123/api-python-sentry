# API Produits

API REST Flask connectee a MySQL (base magasin), documentee avec Swagger.

## Lancer

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Swagger : http://127.0.0.1:5000/swagger

## Routes

- GET    /products          lister
- POST   /products          creer
- GET    /products/{id}     lire un
- PUT    /products/{id}     modifier
- DELETE /products/{id}     supprimer
