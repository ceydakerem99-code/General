import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# .env dosyasını yükle
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Gemini modelini başlat
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  
    temperature=0.3,
    google_api_key=api_key
)

# Örnek test
soru = "LangChain nedir?"
cevap = llm.invoke(soru)
print("Yanıt:", cevap.content)
