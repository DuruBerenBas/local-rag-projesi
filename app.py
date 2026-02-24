from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_engine import process_pdf, answer_question

print("API Başlatılıyor... PDF okunup hafızaya alınıyor...")
db = process_pdf("belge.pdf")
print("Sistem Hazır! Gelen sorular bekleniyor...")

app = FastAPI(title="Duru'nun RAG Motoru")


class SoruIstegi(BaseModel):
    soru: str


# --- 1. YENİ EKLENEN: Health Endpoint'i ---
@app.get("/health")
def health_check():
    """Servisin ayakta olup olmadığını kontrol eden uç nokta."""
    return {"status": "ok", "message": "Servis ayakta ve çalışıyor!"}


@app.get("/")
def read_root():
    return {"mesaj": "RAG API tıkır tıkır çalışıyor! Soruları /ask adresine gönderin."}


@app.post("/ask")
def ask_ai(istek: SoruIstegi):
    # --- 2. YENİ EKLENEN: Hata Yakalama (Boş soru kontrolü) ---
    if not istek.soru or istek.soru.strip() == "":
        raise HTTPException(status_code=400, detail="Soru alanı boş bırakılamaz!")

    yapay_zeka_cevabi = answer_question(db, istek.soru)

    return {
        "senin_sorun": istek.soru,
        "yapay_zeka_cevabi": yapay_zeka_cevabi
    }