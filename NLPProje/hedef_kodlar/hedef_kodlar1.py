import datetime
import random

# --- 1. KATMAN: ALTYAPI VE VERİTABANI (Infrastructure) ---

class Logger:
    """Sistemin log kayıtlarını tutan sınıf."""
    def log(self, message):
        print(f"[LOG - {datetime.datetime.now()}]: {message}")

class DatabaseConnection:
    """Veritabanı bağlantısını simüle eder."""
    def connect(self):
        print("Veritabanına bağlanıldı...")
        return True

class OrderRepository:
    """Veritabanı işlemlerini yapan Repository katmanı."""
    def __init__(self, db_conn):
        self.db = db_conn

    def save_order(self, order_data):
        # SQL Insert işlemi simülasyonu
        print(f"INSERT INTO orders VALUES ({order_data['id']}, {order_data['amount']})")
        return True

# --- 2. KATMAN: SERVİSLER VE İŞ MANTIĞI (Services) ---

class NotificationService:
    """Müşteriye E-posta veya SMS atan servis."""
    def send_email(self, user_email, subject):
        print(f"EMAIL GÖNDERİLİYOR -> Kime: {user_email} | Konu: {subject}")

# Ödeme Yöntemleri için Miras Alma (Inheritance) Örneği
class PaymentProcessor:
    """Temel ödeme sınıfı (Base Class)."""
    def process_payment(self, amount):
        raise NotImplementedError("Bu metod alt sınıflarda doldurulmalı.")

class CreditCardPayment(PaymentProcessor):
    """Kredi kartı ile ödeme."""
    def process_payment(self, amount):
        print(f"Kredi Kartı ile {amount} TL çekildi.")
        return True

class BitcoinPayment(PaymentProcessor):
    """Kripto para ile ödeme."""
    def process_payment(self, amount):
        print(f"Bitcoin cüzdanından {amount} TL karşılığı BTC transfer edildi.")
        return True

class OrderService:
    """Sipariş iş mantığını yöneten ana servis (Business Logic)."""
    def __init__(self):
        # Bağımlılıklar burada oluşturuluyor (Composition)
        self.logger = Logger()
        self.db_conn = DatabaseConnection()
        self.repository = OrderRepository(self.db_conn)
        self.notification = NotificationService()

    def place_order(self, user, amount, payment_method_type="cc"):
        self.logger.log(f"Yeni sipariş isteği: {user}")
        
        # Ödeme Yöntemini Seç (Factory Pattern benzeri)
        if payment_method_type == "btc":
            payment_processor = BitcoinPayment()
        else:
            payment_processor = CreditCardPayment()
            
        # Ödemeyi Al
        if payment_processor.process_payment(amount):
            # Veritabanına Kaydet
            order_data = {"id": random.randint(1000, 9999), "amount": amount}
            self.repository.save_order(order_data)
            
            # Müşteriye Bildir
            self.notification.send_email(user, "Siparişiniz Alındı")
            self.logger.log("Sipariş başarıyla tamamlandı.")
        else:
            self.logger.log("Ödeme başarısız!")

# --- 3. KATMAN: ARAYÜZ / KONTROL (Controller) ---

class OrderController:
    """Web sitesinden veya API'den gelen isteği karşılayan sınıf."""
    def __init__(self):
        self.service = OrderService()

    def post(self, user_name, total_price):
        print(f"--- API İsteği Geldi: {user_name} ---")
        self.service.place_order(user_name, total_price)

# --- UYGULAMA BAŞLANGICI ---
if __name__ == "__main__":
    controller = OrderController()
    controller.post("baris.okten@example.com", 1500)