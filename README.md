# Yerel RAG Destekli Soru-Cevap API'si

## 📌 Proje Hakkında
Bu proje, yerel (local) bir Büyük Dil Modeli (LLM) kullanarak kullanıcıların PDF dokümanları üzerinden soru sorabilmesini sağlayan bir RAG (Retrieval-Augmented Generation) servisidir. Veriler dışarıya veya buluta çıkmaz, tamamen yerel ortamda işlenir.

## 🛠 Kullanılan Teknolojiler ve Nedenleri
* **Ollama (gemma3:4b):** Sohbet (LLM) modeli olarak kullanıldı. İnternet gerektirmemesi ve kişisel/kurumsal veri gizliliği sağlaması sebebiyle tercih edildi.
* **Ollama (nomic-embed-text):** Metinleri vektörlere dönüştürmek (embedding) için kullanıldı. RAG sistemleri için hızlı ve özel optimize edilmiş bir model olması sebebiyle seçildi.
* **LangChain & FAISS:** PDF işleme, metinleri anlamlı parçalara bölme (chunking) ve hızlı vektör araması (FAISS) yapmak için kullanıldı.
* **FastAPI:** Hızlı, modern ve otomatik dokümantasyon (Swagger UI) sağladığı için REST API katmanında tercih edildi.
* **Pytest:** API uç noktalarını otomatik olarak test edip sistemin kararlılığını kanıtlamak için kullanıldı.

## 🚀 Kurulum Adımları

**1. Gereksinimleri Yükleyin:**
Projeyi indirdikten sonra terminalde sanal ortamınızı aktif edin ve gerekli kütüphaneleri kurun:
```bash
pip install -r requirements.txt