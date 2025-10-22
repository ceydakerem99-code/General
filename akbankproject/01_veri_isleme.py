import os
import pickle
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

# PDF klasörünün yolu
TEZLER_KLASORU = r"C:\Users\ceyda\Desktop\tezler"
CIKTI_DOSYASI = "tez_dokumanlari.pkl"

def tezleri_yukle_ve_kaydet(klasor_yolu, cikti_dosyasi):
    """
    Belirtilen klasördeki tüm PDF dosyalarını yükler ve 
    LangChain Document nesneleri listesi olarak bir dosyaya kaydeder.
    """
    if not os.path.exists(klasor_yolu):
        print(f"Hata: '{klasor_yolu}' klasörü bulunamadı.")
        return

    pdf_files = [f for f in os.listdir(klasor_yolu) if f.endswith(".pdf")]
    
    if not pdf_files:
        print(f"'{klasor_yolu}' klasöründe yüklenecek PDF dosyası bulunamadı.")
        return

    all_docs = []
    print(f"'{klasor_yolu}' klasöründeki {len(pdf_files)} PDF dosyası işleniyor...")

    for pdf_file in pdf_files:
        path = os.path.join(klasor_yolu, pdf_file)
        
        # PyPDFLoader'ı kullanma
        try:
            loader = PyPDFLoader(path)
            docs = loader.load()
            
            # Kaynak bilgisini (metadata) her parçaya eklemek
            for doc in docs:
                doc.metadata["source"] = pdf_file
            
            all_docs.extend(docs)
            print(f"  - {pdf_file} yüklendi. Parça sayısı: {len(docs)}")
        
        except Exception as e:
            print(f"  - HATA: {pdf_file} yüklenirken bir sorun oluştu: {e}")

    # Veriyi kaydet
    if all_docs:
        with open(cikti_dosyasi, "wb") as f:
            pickle.dump(all_docs, f)
        
        print(f"\nBaşarılı! Toplam {len(all_docs)} belge parçası ('{cikti_dosyasi}' dosyasına) kaydedildi.")
    else:
        print("\nİşlem tamamlandı, ancak hiçbir belge parçası yüklenemedi.")

if __name__ == "__main__":
    tezleri_yukle_ve_kaydet(TEZLER_KLASORU, CIKTI_DOSYASI)