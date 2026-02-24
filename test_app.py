from fastapi.testclient import TestClient
from app import app

# API'mizi test etmek için sanal bir istemci (client) oluşturuyoruz
client = TestClient(app)

def test_health_check():
    """Servisin ayakta olup olmadığını test eder."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Servis ayakta ve çalışıyor!"}

def test_ask_valid_question():
    """Geçerli bir soru sorulduğunda 200 Başarılı kodu ve cevap döndüğünü test eder."""
    response = client.post("/ask", json={"soru": "Duru'nun hedefleri nelerdir?"})
    assert response.status_code == 200
    assert "yapay_zeka_cevabi" in response.json()

def test_ask_empty_question():
    """Kullanıcı boş soru gönderdiğinde sistemin çökmediğini ve 400 Hata kodu verdiğini test eder."""
    response = client.post("/ask", json={"soru": ""})
    assert response.status_code == 400
    assert response.json()["detail"] == "Soru alanı boş bırakılamaz!"