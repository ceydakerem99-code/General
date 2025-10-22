# 🧠 ZetBotAi — Akademik Tez Chatbot'u

### 🇹🇷 Türkçe Açıklama


ZetBotAi, Türkiye’deki öğretim üyelerinin tezlerinden oluşan veri setleriyle eğitilmiş bir RAG (Retrieval-Augmented Generation) tabanlı yapay zekâ destekli chatbot sistemidir.
Kullanıcılar, akademik tezlerle ilgili sorular sorabilir ve sistem, tezlerden aldığı bağlamla sorulara anlamlı, tez adıyla kaynak göstererek yanıtlar üretir.
Sistem, tezleri PDF’lerden çıkarır, metinleri parçalara böler ve her parça için embedding oluşturarak vektör veritabanında saklar. Bu sayede, kullanıcı sorusu geldiğinde ilgili tez parçalarını hızlıca bulur ve yanıt üretir.

---

## 🎯 Projenin Amacı

* Akademik bilgilere erişimi kolaylaştırmak
* Tez araştırmalarını hızlandırmak
* Türkçe veriyle çalışan bir **LLM + RAG** sistemi oluşturmak
* Google Gemini API’sini LangChain yapısında etkin biçimde kullanmak

---
🔍 Arama ve Yanıt Süreci

ZetBotAi, kullanıcının sorduğu soruya cevap üretmeden önce tez veritabanında arama yapar. İşleyiş şöyle:

1-PDF’lerden Metin Çıkarma: tezler/ klasöründeki tezler okunur ve metinleri tez_dokumanlari.pkl dosyasına kaydedilir.

2-Parçalama ve Embedding: Her tez parçalara ayrılır ve Türkçe embedding modeli ile vektör haline getirilir (vector_db/).

3-Vektör Tabanlı Arama: Kullanıcı bir soru sorduğunda, sistem en ilgili tez parçalarını vektör veritabanında bulur.

4-Yanıt Üretimi (RAG): Bulunan tez parçaları bağlam olarak Google Gemini modeline verilir ve kaynaklı cevap üretilir.

Yani kullanıcı her soruda doğrudan veritabanındaki tezleri tarayan ve kaynak belirten bir yanıt üreten bir sistemle etkileşime girer.


## 🧩 Proje Mimarisi

```text
┌────────────────────────────┐
│        Kullanıcı Sorgusu   │
└──────────────┬─────────────┘
               │
               ▼
   HuggingFace Embedding Modeli
               │
               ▼
        Chroma Vektör DB
               │
               ▼
      Google Gemini API (LLM)
               │
               ▼
        Gradio Web Arayüzü
```

---

## 📂 Proje Klasör Yapısı

```text
C:\Users\ceyda\Desktop\akbankproject
│
├── .env                        # Google API anahtarı
├── run_project.bat             # Otomatik başlatıcı (3 adımlı)
│
├── 01_veri_isleme.py           # PDF tezleri okur, Document nesneleri oluşturur
├── python1.py                  # Tezleri embedding’lere dönüştürüp Chroma DB oluşturur
├── app.py                      # RAG pipeline ve Gradio chatbot arayüzü
├── python.py                   # Gemini API test dosyası
│
├── tezler/                     # Yüklenen PDF tezleri (873793.pdf, vb.)
├── vector_db/                  # Embedding veritabanı (Chroma)
└── tez_dokumanlari.pkl         # Tezlerden çıkarılmış Document nesneleri
├──Readme.md
```

---

## ⚙️ Kullanılan Teknolojiler

| Bileşen                 | Teknoloji                                          |
| ----------------------- | -------------------------------------------------- |
| **LLM (Yanıt üretimi)** | Google Gemini API                                  |
| **Embedding Modeli**    | `emrecan/bert-base-turkish-cased-mean-nli-stsb-tr` |
| **Vektör Veritabanı**   | Chroma                                             |
| **Pipeline Framework**  | LangChain                                          |
| **Web Arayüzü**         | Gradio                                             |
| **Veri İşleme**         | PyMuPDF, PyPDFLoader                               |
| **Ortam Yönetimi**      | python-dotenv                                      |
| **Otomatik Çalıştırma** | Batch Script (`run_project.bat`)                   |

---

## 🧠 Çalışma Adımları

### 🔹 1️⃣ PDF Tezleri İşleme (`01_veri_isleme.py`)

PDF’ler okunur, her sayfadan metin çıkarılır, `LangChain Document` nesnelerine dönüştürülür ve `tez_dokumanlari.pkl` dosyasına kaydedilir.

### 🔹 2️⃣ Embedding Veritabanı Oluşturma (`python1.py`)

Tez parçaları `RecursiveCharacterTextSplitter` ile bölünür, Türkçe embedding modeliyle vektörleştirilir ve **Chroma DB**'ye kaydedilir.

### 🔹 3️⃣ Chatbot Arayüzü (`app.py`)

RAG zinciri oluşturulur:

* **Retriever:** En ilgili 3 tez parçasını getirir
* **PromptTemplate:** Kullanıcıya verilecek yanıt biçimi belirlenir
* **LLM (Gemini):** Kaynaklardan yanıt üretir
* **Gradio:** Web arayüzü başlatılır

---

## 🧪 API Test Dosyası (`python.py`)

Gemini API bağlantısı test edilir:

```python
soru = "LangChain nedir?"
cevap = llm.invoke(soru)
print("Yanıt:", cevap.content)
```

---

## 🔧 Otomatik Çalıştırma (`run_project.bat`)

Windows üzerinde proje 3 adımda otomatik başlatılır 👇

```bat
[1/3] Veriler işleniyor...
python 01_veri_isleme.py

[2/3] Embedding veritabani olusturuluyor...
python python1.py

[3/3] Uygulama baslatiliyor...
python app.py
```

💻 Başarıyla tamamlandığında:

```
🌐 Tarayıcı: http://127.0.0.1:7860/
```

---

## 🌐 Web Arayüzü

**Başlık:**

> YÖKTez-AI: Akademik Tez Chatbot'u

**Açıklama:**

> Türkiye'deki öğretim üyelerinin tezleri hakkında sorular sorun. Veri seti, YÖK Ulusal Tez Merkezi'nden alınan örnek tezlerden oluşmaktadır.

**Örnek Sorular:**

* “Yapay sinir ağları ile ilgili hangi çalışmalar var?”
* “Osmanlı dönemi mimarisi hakkında bilgi içeren tezler hangileri?”
* “Biyoinformatik alanında yapılan tezlerde hangi yöntemler kullanılmış?”

---

## ⚠️ Uyarılar

* `LangChainDeprecationWarning` mesajlarını önlemek için şu komutu çalıştır:

  ```bash
  pip install -U langchain-huggingface langchain-chroma
  ```
* `.env` dosyanda şu satır bulunmalıdır:

  ```
  GOOGLE_API_KEY=AIzaSyBk8ziC7GjnS215tPdyvrxSxTJi800TqS8
  ```
* İlk çalıştırmada embedding işlemi uzun sürebilir (PDF boyutuna göre).

---

## 📦 Gereksinimler

`requirements.txt` dosyası içeriği 👇

```txt
langchain
langchain-core
langchain-community
langchain-text-splitters
gradio
chromadb
python-dotenv
fitz
PyMuPDF
google-generativeai
huggingface_hub
sentence-transformers
```

---

## 📑 Proje Özeti (Kısa Sunum Metni)

> **Proje Adı:** YÖKTez-AI — Akademik Tez Chatbot’u
> **Amaç:** Akademik tezler üzerinden anlamlı ve kaynaklı yanıtlar üreten Türkçe bir RAG sistemi geliştirmek
> **Model:** Google Gemini 2.5 Flash + Türkçe BERT Embedding
> **Çıktı:** Tezlerden elde edilen 1094 belge parçası ile çalışan, Gradio tabanlı interaktif sohbet arayüzü

---

## 🧾 Lisans ve Katkı

Bu proje, **Akbank Generative AI 101 Bootcamp** kapsamında geliştirilmiştir.
Eğitim, demo ve araştırma amaçlıdır.



## 🧾 Ekip Üyeleri
Ceydanur Kerem, 

Muhammed Uğur Özmen

