import pickle
import os
from dotenv import load_dotenv

# LangChain v1.0+ için güncellenmiş import'lar
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
# Chat modeli için gerekli import
from langchain_google_genai import ChatGoogleGenerativeAI
# Gemini Embeddings kullanacaksanız bu gerekli, ancak HuggingFace modelini kullandığınız için şimdilik tutarlılık için yoruma alıyorum.
# Eğer Google Embeddings kullanmak isterseniz alttaki satırı aktif edip HuggingFaceEmbeddings satırlarını düzenlemelisiniz.
# from langchain_google_genai import GoogleGenerativeAIEmbeddings 

load_dotenv() 

# --- Sabitler ---
DOKUMAN_DOSYASI = "tez_dokumanlari.pkl"
DB_KLASORU = "vector_db"
EMBEDDING_MODELI = "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr"

# --- Model Tanımı (Fonksiyon içinde kullanılmayacağı için yoruma alındı) ---
# Bu script sadece veritabanı oluşturduğu için LLM'ye ihtiyacı yoktur.
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-pro",  # listeden doğru modeli seç
#     google_api_key=os.getenv("GOOGLE_API_KEY")
# )

# --- Embedding Tanımı ---
# Kodunuzun üst kısmındaki bu tanım gereksizdir ve fonksiyon içindeki tanımla çakışır. Sadece fonksiyonda tanımlamak yeterlidir.
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") 

def veritabani_olustur():
    try:
        with open(DOKUMAN_DOSYASI, "rb") as f:
            # Document objeleri için artık langchain_core import'u gerekiyor.
            dokumanlar = pickle.load(f)
    except FileNotFoundError:
        print(f"Hata: '{DOKUMAN_DOSYASI}' bulunamadı. Önce veri işleme scriptini çalıştırın.")
        return

    # Text Splitter artık 'langchain_text_splitters' paketinden gelir.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    parcalar = text_splitter.split_documents(dokumanlar)

    if not parcalar:
        print("Veritabanına eklenecek metin parçası bulunamadı.")
        return

    print(f"Toplam {len(dokumanlar)} doküman, {len(parcalar)} parçaya bölündü.")

    # HuggingFaceEmbeddings doğru bir şekilde langchain_community'den import edildi.
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODELI,
        model_kwargs={'device': 'cpu'}
    )
    print(f"Embedding modeli ({EMBEDDING_MODELI}) yüklendi.")

    # Chroma.from_documents doğru bir şekilde langchain_community'den import edildi.
    db = Chroma.from_documents(
        documents=parcalar,
        embedding=embeddings,
        persist_directory=DB_KLASORU
    )
    # Persist işlemi için db objesinin kapatılması gerekir.
    db.persist()
    print(f"Veritabanı başarıyla '{DB_KLASORU}' klasörüne kaydedildi.")

if __name__ == "__main__":
    veritabani_olustur()