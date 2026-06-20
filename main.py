from datetime import datetime, timezone
import os
from typing import List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


APP_NAME = os.getenv("APP_NAME", "API Katalog Buku")
APP_ENV = os.getenv("APP_ENV", "development")

app = FastAPI(
    title=APP_NAME,
    description="API sederhana untuk praktikum deployment PaaS.",
    version="1.0.0",
)


class Buku(BaseModel):
    id_buku: int = Field(gt=0)
    judul: str = Field(min_length=2, max_length=100)
    penulis: str = Field(min_length=2, max_length=100)
    tahun: int = Field(ge=1900, le=2100)
    kategori: str = Field(min_length=2, max_length=50)


# Data disimpan di memory dan tidak permanen.
data_buku: List[dict] = [
    {
        "id_buku": 1,
        "judul": "Dasar Cloud Computing",
        "penulis": "Andi Pratama",
        "tahun": 2025,
        "kategori": "Teknologi",
    },
    {
        "id_buku": 2,
        "judul": "Pemrograman API dengan FastAPI",
        "penulis": "Siti Rahma",
        "tahun": 2026,
        "kategori": "Pemrograman",
    },
    {
        "id_buku": 3,
        "judul": "Pengenalan DevOps",
        "penulis": "Budi Santoso",
        "tahun": 2024,
        "kategori": "Infrastruktur",
    },
]


@app.get("/")
def home():
    return {
        "message": f"{APP_NAME} aktif",
        "environment": APP_ENV,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": APP_NAME,
        "environment": APP_ENV,
        "time_utc": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/identitas")
def identitas():
    return {
        "nama": "Nama Mahasiswa",
        "nim": "23123456",
        "kelas": "TI-5A",
    }


@app.get("/buku")
def get_semua_buku():
    return {
        "jumlah": len(data_buku),
        "data": data_buku,
    }


@app.get("/buku/{id_buku}")
def get_buku_by_id(id_buku: int):
    for buku in data_buku:
        if buku["id_buku"] == id_buku:
            return {"data": buku}

    raise HTTPException(status_code=404, detail="Buku tidak ditemukan")


@app.post("/buku", status_code=status.HTTP_201_CREATED)
def tambah_buku(buku: Buku):
    for item in data_buku:
        if item["id_buku"] == buku.id_buku:
            raise HTTPException(
                status_code=400,
                detail="ID buku sudah digunakan",
            )

    buku_baru = buku.model_dump()
    data_buku.append(buku_baru)

    return {
        "message": "Buku berhasil ditambahkan",
        "data": buku_baru,
    }


@app.put("/buku/{id_buku}")
def ubah_buku(id_buku: int, buku: Buku):
    if id_buku != buku.id_buku:
        raise HTTPException(
            status_code=400,
            detail="ID pada URL harus sama dengan ID pada body",
        )

    for index, item in enumerate(data_buku):
        if item["id_buku"] == id_buku:
            data_buku[index] = buku.model_dump()
            return {
                "message": "Buku berhasil diperbarui",
                "data": data_buku[index],
            }

    raise HTTPException(status_code=404, detail="Buku tidak ditemukan")


@app.delete("/buku/{id_buku}")
def hapus_buku(id_buku: int):
    for index, item in enumerate(data_buku):
        if item["id_buku"] == id_buku:
            buku_dihapus = data_buku.pop(index)
            return {
                "message": "Buku berhasil dihapus",
                "data": buku_dihapus,
            }

    raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
