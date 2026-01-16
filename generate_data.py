import pandas as pd
import random
from datetime import datetime, timedelta

# Ürün Listesi ve Fiyatları
products = {
    'Elektronik': [('Laptop', 15000), ('Kulaklık', 2000), ('Mouse', 500), ('Klavye', 800), ('Monitör', 4000)],
    'Giyim': [('T-Shirt', 300), ('Kot Pantolon', 800), ('Mont', 2500), ('Spor Ayakkabı', 1500)],
    'Ev & Yaşam': [('Kahve Makinesi', 3000), ('Blender', 1200), ('Lamba', 400), ('Tablo', 250)]
}

# Veri Üretme Fonksiyonu
def generate_sales_data(num_rows=1000):
    data = []
    
    start_date = datetime(2025, 1, 1)
    
    for i in range(num_rows):
        # Rastgele Tarih (2025 yılı içinde)
        random_days = random.randint(0, 365)
        date = start_date + timedelta(days=random_days)
        
        # Rastgele Kategori ve Ürün
        category = random.choice(list(products.keys()))
        product_name, price = random.choice(products[category])
        
        # Rastgele Adet (1 ile 5 arası)
        quantity = random.randint(1, 5)
        
        # Toplam Tutar
        total_price = price * quantity
        
        # Ödeme Yöntemi
        payment_method = random.choice(['Kredi Kartı', 'Havale', 'Kapıda Ödeme'])
        
        data.append([
            date.strftime("%Y-%m-%d"),
            category,
            product_name,
            price,
            quantity,
            total_price,
            payment_method
        ])
        
    return data

# DataFrame oluştur ve Excel'e kaydet
print("Veri üretiliyor...")
data = generate_sales_data()
columns = ['Tarih', 'Kategori', 'Ürün Adı', 'Birim Fiyat', 'Adet', 'Toplam Tutar', 'Ödeme Yöntemi']
df = pd.DataFrame(data, columns=columns)

file_name = "satis_verileri.xlsx"
df.to_excel(file_name, index=False)

print(f"✅ Harika! '{file_name}' dosyası başarıyla oluşturuldu.")
print(f"Toplam {len(df)} satır veri var.")