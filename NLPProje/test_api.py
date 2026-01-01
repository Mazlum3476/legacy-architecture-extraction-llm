import google.generativeai as genai

# Anahtarını buraya yapıştır
TEST_KEY = "AIzaSyAlqu1friLTyrh7lHxlxwF2NMd5-Ah9KW8"

genai.configure(api_key=TEST_KEY)

print("🔍 Hesabının erişebildiği modeller aranıyor...\n")

try:
    bulunan_modeller = []
    for m in genai.list_models():
        # Sadece metin üretebilen (generateContent destekleyen) modelleri al
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")
            bulunan_modeller.append(m.name)
            
    print(f"\n✅ Toplam {len(bulunan_modeller)} uygun model bulundu.")
    
    # Otomatik test yapalım: İlk uygun modeli deneyelim
    if bulunan_modeller:
        secilen_model = bulunan_modeller[0].name # Listeden ilkini al (örn: models/gemini-pro)
        print(f"\n🧪 Test için seçilen model: {secilen_model}")
        
        # 'models/' ön ekini atıp saf ismi almayı deneriz bazen, ama genelde bu haliyle çalışır
        model = genai.GenerativeModel(secilen_model)
        response = model.generate_content("Merhaba, çalışıyor musun?")
        print(f"✅ SONUÇ: {response.text}")
        
except Exception as e:
    print("\n❌ HATA:")
    print(e)