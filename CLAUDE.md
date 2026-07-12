# Eshop projekt

Django REST API + HTML/JS frontend pro eshop s auty.

## Spuštění projektu

```bash
source venv/bin/activate
python manage.py runserver
```

Frontend: http://127.0.0.1:8000/
API: http://127.0.0.1:8000/api/
Admin: http://127.0.0.1:8000/admin/

## Spuštění testů

```bash
source venv/bin/activate
python manage.py test products
```

Testy se nacházejí v `products/tests.py` a pokrývají:

- **PageSmokeTest** — ověří že se otevřou stránky `/`, `/api/`, `/api/products/`, `/admin/`
- **ProductModelTest** — vytvoření produktu, výchozí hodnota logo_url, uložení logo_url
- **ProductAPITest** — GET seznam, GET detail, POST vytvoření, PUT aktualizace, PATCH částečná aktualizace, DELETE smazání, 404 pro neexistující produkt, validace chybějícího názvu

## Datový model

### Katalog
- **Brand** — výrobce (name, logo_url, country)
- **Category** — kategorie vozidla (name, slug)
- **Product** — produkt/auto (name, description, price, stock, logo_url, brand FK, category FK)
- **ProductImage** — více fotek k produktu (product FK, url, alt, order)

### Zákazníci
- **Customer** — rozšíření Django User (user OneToOne, phone)
- **Address** — doručovací adresa (customer FK, street, city, zip_code, country, is_default)

### Objednávky
- **Order** — objednávka (customer FK, shipping_address FK, status, total)
  - Status: `pending` → `confirmed` → `shipped` → `delivered` / `cancelled`
- **OrderItem** — položka objednávky (order FK, product FK, quantity, unit_price)

### Košík & Hodnocení
- **Cart** — košík zákazníka (customer OneToOne)
- **CartItem** — položka košíku (cart FK, product FK, quantity)
- **Review** — hodnocení produktu (product FK, customer FK, rating, text); unikátní na (product, customer)

## API endpointy

| Endpoint | Model |
|---|---|
| `/api/brands/` | Brand |
| `/api/categories/` | Category |
| `/api/products/` | Product |
| `/api/product-images/` | ProductImage |
| `/api/customers/` | Customer |
| `/api/addresses/` | Address |
| `/api/orders/` | Order |
| `/api/order-items/` | OrderItem |
| `/api/reviews/` | Review |
| `/api/carts/` | Cart |
| `/api/cart-items/` | CartItem |

Všechny endpointy podporují plný CRUD (GET list, GET detail, POST, PUT, PATCH, DELETE).
