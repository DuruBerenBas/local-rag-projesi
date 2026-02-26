
#Yerel RAG (Retrieval-Augmented Generation) API Motoru

##Projenin Kısa Açıklaması
Bu proje, veri gizliliğini (data privacy) korumak amacıyla tamamen yerel (local) donanım üzerinde çalışan, dışarıya kapalı bir RAG (Retrieval-Augmented Generation) arama motorudur. Sistem, verilen PDF dokümanlarını okuyup vektör uzayında indeksler ve kullanıcının sorularını "açık kitap sınavı" mantığıyla sadece bu belgeler bağlamında yanıtlar. Dış dünyadan gelen veriler, modern bir REST API (FastAPI) mimarisi ile karşılanarak büyük dil modelinin (LLM) bilgi uydurması (halüsinasyon) kesin olarak engellenir.

---

##Kullanılan Ana Teknolojiler ve Tercih Nedenleri

Sistemi tasarlarken performans, güvenlik ve "Görevlerin Ayrılığı (Separation of Concerns)" prensiplerine göre aşağıdaki teknolojiler seçilmiştir:

* **Ollama & gemma3:4b (LLM):** Bulut API'lerini (OpenAI vb.) kullanmak şirket verilerinin dışarı çıkması anlamına geldiği için reddedildi. Bunun yerine arka planda servis olarak çok hafif çalışan Ollama ve yüksek performanslı açık kaynaklı `gemma3:4b` modeli tercih edildi.
* **LangChain:** Projeyi spagetti koddan kurtarıp modüler (lego gibi sökülüp takılabilir) bir orkestrasyona oturtmak için kullanıldı. Veri parçalama (chunking) ve LLM zincirleme işlemlerini inanılmaz hızlandırdı.
* **FAISS (Vektör Veritabanı):** Hızın kritik olduğu bu sistemde ağır SQL sorguları yerine, bilgisayarın anlık belleğinde (In-Memory) çalışan ve Kosinüs Benzerliği (Cosine Similarity) aramalarını milisaniyeler içinde yapan FAISS kullanıldı.
* **nomic-embed-text:** Büyük sohbet modelini metinleri sayılara (vektörlere) çevirmekle yormak yerine, sadece vektörleştirme işlemi için özel eğitilmiş olan bu küçük ve hızlı model seçildi.
* **FastAPI & Pydantic:** RAG motorunu dış dünyanın kullanımına (REST API) açmak için kullanıldı. Doğuştan asenkron olması performansı artırırken, **Pydantic** kütüphanesi sayesinde hatalı sorgular motoru çökertmeden API kapısında `HTTP 422` hatasıyla engellendi.

---

##Kurulum ve Çalıştırma Adımları

Projeyi kendi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla izleyin:

**1. Projeyi Klonlayın ve Klasöre Girin**
```bash
git clone [https://github.com/DuruBerenBas/local-rag-projesi.git](https://github.com/DuruBerenBas/local-rag-projesi.git)
cd local-rag-projesi

2. Sanal Ortam (Virtual Environment) Oluşturun ve Aktif Edin
python -m venv .venv
# Windows için:
.venv\Scripts\activate
# Mac/Linux için:
source .venv/bin/activate

3. Gerekli Kütüphaneleri Yükleyin
pip install -r requirements.txt

4. Ollama Modellerini İndirin
(Bilgisayarınızda Ollama'nın kurulu ve çalışıyor olduğundan emin olun.)
ollama pull gemma3:4b
ollama pull nomic-embed-text

5. Dokümanlarınızı Ekleyin
Okutmak istediğiniz PDF dosyalarını ana dizindeki dokumanlar klasörünün içine yerleştirin.
6. Sunucuyu Başlatın
uvicorn app:app --reload

7. API'yi Test Edin (Swagger UI)
Tarayıcınızı açın ve aşağıdaki adrese giderek projeyi görsel arayüzden test edin:
👉 http://127.0.0.1:8000/docs



