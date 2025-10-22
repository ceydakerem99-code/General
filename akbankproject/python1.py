import os
import fitz  # PyMuPDF
# Hata düzeltmesi: LangChain v1.0+ için Document artık langchain_core'dan gelir
from langchain_core.documents import Document 
import pickle

TEZLER_KLASORU = r"C:\Users\ceyda\Desktop\tezler"
CIKTI_DOSYASI = "tez_dokumanlari.pkl"

def pdf_metin_cikarici(klasor_yolu):
    """
    Belirtilen klasördeki tüm PDF dosyalarının metinlerini çıkarır
    ve LangChain Document nesneleri listesi olarak döndürür.
    """
    dokumanlar = []
    print(f"'{klasor_yolu}' klasöründeki PDF'ler işleniyor...")
    
    for dosya_adi in os.listdir(klasor_yolu):
        if dosya_adi.endswith(".pdf"):
            dosya_yolu = os.path.join(klasor_yolu, dosya_adi)
            try:
                # PyMuPDF ile PDF'i aç
                with fitz.open(dosya_yolu) as doc:
                    metin = ""
                    # Her sayfanın metnini al
                    for sayfa in doc:
                        metin += sayfa.get_text()
                
                # Sadece anlamlı metinleri tutmak için basit bir temizlik
                metin = "\n".join(filter(lambda x: len(x) > 20, metin.split('\n')))

                if metin:
                    # LangChain Document nesnesi oluştur
                    # Metadata, chatbot'un kaynağı belirtmesi için önemlidir
                    dokuman = Document(
                        page_content=metin,
                        metadata={"source": dosya_adi}
                    )
                    dokumanlar.append(dokuman)
                    print(f"  - {dosya_adi} başarıyla işlendi.")
                else:
                    print(f"  - UYARI: {dosya_adi} içinden metin çıkarılamadı.")

            except Exception as e:
                print(f"  - HATA: {dosya_adi} işlenirken bir hata oluştu: {e}")
    
    return dokumanlar

if __name__ == "__main__":
    if not os.path.exists(TEZLER_KLASORU):
        print(f"Hata: '{TEZLER_KLASORU}' adında bir klasör bulunamadı. Lütfen PDF tezlerinizi bu klasöre koyun.")
    else:
        tez_dokumanlari = pdf_metin_cikarici(TEZLER_KLASORU)
        if tez_dokumanlari:
            # İşlenmiş dokümanları bir sonraki adımda kullanmak üzere kaydet
            with open(CIKTI_DOSYASI, "wb") as f:
                pickle.dump(tez_dokumanlari, f)
            print(f"\nToplam {len(tez_dokumanlari)} adet tez işlendi ve '{CIKTI_DOSYASI}' dosyasına kaydedildi.")
        else:
            print("\nHiçbir tez işlenemedi. 'tezler' klasöründe PDF olduğundan emin olun.")