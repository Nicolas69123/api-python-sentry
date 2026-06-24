"""
Test de regression pour l'issue #1 (ZeroDivisionError sur /debug-sentry).
Verifie que la route de test n'existe plus -> l'erreur ne peut plus se produire.
"""
import app


def test_debug_sentry_route_supprimee():
    """La route /debug-sentry (division par zero) ne doit plus exister."""
    routes = [str(r) for r in app.app.url_map.iter_rules()]
    assert not any("debug-sentry" in r for r in routes), (
        "La route /debug-sentry est revenue : risque de ZeroDivisionError (#1)"
    )


def test_route_produits_existe():
    """L'API expose toujours ses routes metier."""
    routes = [str(r) for r in app.app.url_map.iter_rules()]
    assert any("/products" in r for r in routes)


if __name__ == "__main__":
    test_debug_sentry_route_supprimee()
    test_route_produits_existe()
    print("OK - tous les tests de regression passent")
