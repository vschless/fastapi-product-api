# README_STUDENT

## Umgesetzte Features

Ich habe eine FastAPI Product API implementiert.

Folgende Funktionen sind enthalten:

- Health Endpoint: `GET /health`
- Produkt erstellen: `POST /products/`
- Alle Produkte anzeigen: `GET /products/`
- Einzelnes Produkt anzeigen: `GET /products/{product_id}`
- Produkt aktualisieren: `PUT /products/{product_id}`
- Produkt löschen: `DELETE /products/{product_id}`
- Pagination mit `skip` und `limit`
- Filter nach `category`
- Preisfilter mit `min_price` und `max_price`
- Erweiterung um das Feld `stock`
- Fehlerbehandlung wenn `min_price > max_price`

## Starten der API

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py