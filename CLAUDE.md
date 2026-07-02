# Eshop projekt

Django REST API + HTML/JS frontend pro eshop s auty.

## Spuštění projektu

```bash
source venv/bin/activate
python manage.py runserver
```

Frontend: http://127.0.0.1:8000/
API: http://127.0.0.1:8000/api/products/

## Spuštění testů

```bash
source venv/bin/activate
python manage.py test products
```

Testy se nacházejí v `products/tests.py` a pokrývají:

- **PageSmokeTest** — ověří že se otevřou stránky `/`, `/api/`, `/api/products/`, `/admin/`
- **ProductModelTest** — vytvoření produktu, výchozí hodnota logo_url, uložení logo_url
- **ProductAPITest** — GET seznam, GET detail, POST vytvoření, PUT aktualizace, PATCH částečná aktualizace, DELETE smazání, 404 pro neexistující produkt, validace chybějícího názvu
