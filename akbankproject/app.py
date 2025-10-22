import os
import gradio as gr
from dotenv import load_dotenv

# LangChain v1.0+ için güncellenmiş import'lar
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings 

# Temel bileşenler artık 'langchain-core' paketinden gelir
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


# .env dosyasından API anahtarını yükle
load_dotenv()

# Sabitler
DB_KLASORU = "vector_db"
EMBEDDING_MODELI = "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr"

# --- 1. Model ve Veritabanı Yükleme ---
print("Uygulama başlatılıyor...")

# Google Gemini modelini yükle
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3, convert_system_message_to_human=True)
    print("Google Gemini modeli başarıyla yüklendi.")
except Exception as e:
    print(f"Gemini modeli yüklenirken hata oluştu: {e}")
    print("Lütfen GOOGLE_API_KEY'inizin doğru ayarlandığından emin olun.")
    exit()


# Embedding modelini yükle
print("Embedding modeli yükleniyor...")
model_kwargs = {'device': 'cpu'}
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODELI,
    model_kwargs=model_kwargs
)
print("Embedding modeli yüklendi.")

# Mevcut Vektör Veritabanını yükle
if not os.path.exists(DB_KLASORU):
    print(f"Hata: '{DB_KLASORU}' veritabanı klasörü bulunamadı.")
    print("Lütfen önce '02_db_olustur.py' scriptini çalıştırarak veritabanını oluşturun.")
    exit()

db = Chroma(persist_directory=DB_KLASORU, embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 3}) # Kullanıcı sorusuna en benzer 3 metin parçasını getir
print("Vektör veritabanı başarıyla yüklendi.")

# --- 2. Prompt Şablonu ve RAG Zinciri ---

# LLM'e nasıl davranması gerektiğini söyleyen talimatlar
template = """
Sen Türkiye'deki akademik tezler hakkında soruları yanıtlayan bir yapay zeka asistanısın.
Sadece aşağıda verilen bağlamdaki (context) bilgileri kullanarak soruyu cevapla.
Eğer bağlamda cevap yoksa, "Bu konuda tezlerde bir bilgi bulamadım." de.
Cevabının sonunda, hangi tezden bilgi aldığını 'Kaynak' olarak belirt.

Bağlam (Context):
{context}

Soru:
{question}

Cevap:
"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# RAG zincirini (chain) LangChain Expression Language (LCEL) ile oluştur
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("RAG zinciri oluşturuldu. Uygulama hazır.")


# --- KRİTİK BAĞLANTI TESTİ FONKSİYONU ---
def simple_llm_test(llm_instance):
    """Sadece LLM'i test etmek için basit bir fonksiyon."""
    print("\n--- LLM BAĞLANTI TESTİ BAŞLIYOR ---")
    try:
        # Basit bir API çağrısı yaparak bağlantıyı kontrol et
        response = llm_instance.invoke("Türkiye'nin başkenti neresidir? Cevabın tek kelime olsun.")
        
        # Eğer cevap gelirse
        if response.content:
             print(f"✅ LLM TEST BAŞARILI. API Bağlantısı OK. Cevap: {response.content.strip()[:20]}...")
        else:
             print("❌ LLM TEST BAŞARISIZ. API'den boş cevap döndü.")

    except Exception as e:
        print(f"❌ KRİTİK LLM TEST HATASI. Sorunun kaynağı API: {e}")
        print("Lütfen GOOGLE_API_KEY'inizi, kotanızı ve ağ bağlantınızı kontrol edin.")
    print("--- LLM BAĞLANTI TESTİ BİTTİ ---")


# --- 3. Gradio Arayüzü ---

def chatbot_response(message, history):
    """Gradio arayüzü için chatbot cevap fonksiyonu."""
    if not message.strip():
        return "Lütfen bir soru sorun."
    
    # RAG zincirini çağırarak cevabı al
    response = rag_chain.invoke(message)
    return response

# Gradio arayüzünü oluştur
iface = gr.ChatInterface(
    fn=chatbot_response,
    title="YÖKTez-AI: Akademik Tez Chatbot'u",
    description="Türkiye'deki öğretim üyelerinin tezleri hakkında sorular sorun. Veri seti, YÖK Ulusal Tez Merkezi'nden alınan örnek tezlerden oluşmaktadır.",
    theme="soft",
    examples=[
        ["Yapay sinir ağları ile ilgili hangi çalışmalar var?"],
        ["Osmanlı dönemi mimarisi hakkında bilgi içeren tezler hangileri?"],
        ["Biyoinformatik alanında yapılan tezlerde hangi yöntemler kullanılmış?"]
    ]
)

# Arayüzü başlat
if __name__ == "__main__":
    # Arayüzü başlatmadan önce bağlantıyı test et
    simple_llm_test(llm) 
    
    iface.launch()