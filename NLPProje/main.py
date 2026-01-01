import os
import ast
import json
import time
import google.generativeai as genai

# --- AYARLAR --- 
# BURAYA GEÇERLİ API ANAHTARINI YAPIŞTIR
API_KEY = "BURAYA_KENDI_API_KEYINIZI_YAZIN" 

HEDEF_KLASOR = "hedef_kodlar"
CIKTI_KLASOR = "cikti"

# KULLANILACAK MODELLER (Sırayla dener)
MODELLER = [
    "models/gemini-2.5-pro",         # En güçlü
    "models/gemini-2.5-flash",       # Çok hızlı
    "models/gemini-2.0-flash",       # Standart 2.0
    "models/gemini-exp-1206",        # Deneysel
    "models/gemini-2.0-flash-exp",   # Deneysel Alternatif
]

genai.configure(api_key=API_KEY)

class PythonAnalizcisi(ast.NodeVisitor):
    def __init__(self):
        self.yapisal_veri = {"siniflar": [], "fonksiyonlar": [], "importlar": []}
    def visit_Import(self, node):
        for alias in node.names: self.yapisal_veri["importlar"].append(alias.name)
        self.generic_visit(node)
    def visit_ImportFrom(self, node):
        module = node.module if node.module else ""
        for alias in node.names: self.yapisal_veri["importlar"].append(f"{module}.{alias.name}")
        self.generic_visit(node)
    def visit_ClassDef(self, node):
        self.yapisal_veri["siniflar"].append(node.name)
        self.generic_visit(node)
    def visit_FunctionDef(self, node):
        self.yapisal_veri["fonksiyonlar"].append(node.name)
        self.generic_visit(node)

def dosya_analiz_et(dosya_yolu):
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            kod_icerigi = f.read()
        tree = ast.parse(kod_icerigi)
        analizci = PythonAnalizcisi()
        analizci.visit(tree)
        return analizci.yapisal_veri
    except Exception as e:
        return {"hata": str(e)}

def dosyalari_listele(klasor_yolu, uzantilar=None):
    kod_dosyalari = []
    for root, dirs, files in os.walk(klasor_yolu):
        for file in files:
            if uzantilar:
                if any(file.endswith(ext) for ext in uzantilar):
                    kod_dosyalari.append(os.path.join(root, file))
            else:
                kod_dosyalari.append(os.path.join(root, file))
    return kod_dosyalari

def llm_ile_mimari_cikar(json_verisi):
    prompt = f"""
    Sen uzman bir Yazılım Mimarisin. Aşağıdaki JSON verisi, eski bir projenin yapısal analizidir.
    
    GÖREV:
    Bu veriye dayanarak SADECE "Mermaid JS" formatında bir Class Diagram (Sınıf Diyagramı) kodu üret.
    Kodu ```mermaid ve ``` blokları arasına yaz. Başka açıklama yapma.
    
    VERİ:
    {json.dumps(json_verisi, indent=2)}
    """
    
    for model_adi in MODELLER:
        print(f"\n🔄 Model deneniyor: {model_adi}")
        try:
            model = genai.GenerativeModel(model_adi)
            response = model.generate_content(prompt)
            
            if response.text and ("mermaid" in response.text or "classDiagram" in response.text):
                 print(f"✅ BAŞARILI! {model_adi} cevap verdi.")
                 return response.text
            else:
                print(f"⚠️ {model_adi} boş cevap döndü. Sıradakine geçiliyor...")
                
        except Exception as e:
            hata = str(e)
            if "429" in hata:
                print(f"⛔ Kota dolu (429). {model_adi} pas geçiliyor...")
            elif "404" in hata:
                print(f"⛔ Model bulunamadı (404). {model_adi} pas geçiliyor...")
            else:
                print(f"⛔ Hata: {hata}")
            time.sleep(1) 
            continue

    return "HATA: Modellerden yanıt alınamadı."

def main():
    print("--- 220401066 Barış Ökten & 220401024 Mazlum Dağcı ---")
    print("--- Kod Mimarisi Çıkarıcı (Final Sürüm) ---")
    
    dosyalar = dosyalari_listele(HEDEF_KLASOR, uzantilar=[".py"])
    if not dosyalar:
        print("Dosya bulunamadı.")
        return

    proje_ozeti = {}
    for dosya_yolu in dosyalar:
        print(f" - Okunuyor: {dosya_yolu}")
        proje_ozeti[dosya_yolu] = dosya_analiz_et(dosya_yolu)

    llm_cevabi = llm_ile_mimari_cikar(proje_ozeti)
    
    if not os.path.exists(CIKTI_KLASOR):
        os.makedirs(CIKTI_KLASOR)

    rapor_yolu = os.path.join(CIKTI_KLASOR, "llm_raporu.md")
    
    with open(rapor_yolu, "w", encoding="utf-8") as f:
        f.write(llm_cevabi)
        
    if "HATA" in llm_cevabi:
        print(f"\n❌ {llm_cevabi}")
    else:
        # İSTEDİĞİN ÖZEL MESAJ BÖLÜMÜ BURASI
        print(f"\n✅ İşlem TAMAMLANDI! Sonuç: {rapor_yolu}")
        print("-" * 60)
        print(f"SON ADIM: '{rapor_yolu}' dosyasını aç.")
        print("İçindeki ```mermaid ile başlayan kodu kopyala ve")
        print("[https://mermaid.live](https://mermaid.live) adresine yapıştırarak grafiğini gör.")
        print("-" * 60)

if __name__ == "__main__":
    main()