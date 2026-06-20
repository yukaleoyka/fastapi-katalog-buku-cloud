# Praktikum 12 - Deployment FastAPI

API katalog buku sederhana untuk praktikum Cloud Computing.

## Endpoint utama
- `/`
- `/health`
- `/identitas`
- `/buku`
- `/docs`

## Menjalankan secara lokal
```bash
python -m uvicorn main:app --reload
```

## Deployment
Platform: Render Web Service
Build command: `pip install -r requirements.txt`
Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
