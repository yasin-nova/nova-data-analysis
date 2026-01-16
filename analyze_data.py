import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Görselleştirme Ayarları (Daha şık grafikler için)
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def analyze_sales():
    print("🔄 Veriler yükleniyor ve analiz ediliyor...")
    
    # 1. Excel Dosyasını Oku
    try:
        df = pd.read_excel("satis_verileri.xlsx")
    except FileNotFoundError:
        print("❌ Hata: 'satis_verileri.xlsx' dosyası bulunamadı. Önce veri üretin.")
        return

    # Tarih sütununu datetime formatına çevir (Hata önlemek için)
    df['Tarih'] = pd.to_datetime(df['Tarih'])

    # --- ANALİZLER ---

    # 1. Toplam Ciro Hesapla
    total_revenue = df['Toplam Tutar'].sum()
    print(f"\n💰 TOPLAM YILLIK CİRO: {total_revenue:,.2f} TL")

    # 2. Kategori Bazlı Satışlar (En çok ne satmış?)
    category_sales = df.groupby('Kategori')['Toplam Tutar'].sum().sort_values(ascending=False)
    best_category = category_sales.index[0]
    print(f"🏆 EN ÇOK SATAN KATEGORİ: {best_category} ({category_sales.iloc[0]:,.2f} TL)")

    # 3. Aylık Satış Trendi
    # Tarihten 'Ay' bilgisini çekiyoruz (Örn: 2025-01 -> January)
    df['Ay'] = df['Tarih'].dt.month_name()
    # Ayları sıraya dizmek için kategorik veri yapıyoruz
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    df['Ay'] = pd.Categorical(df['Ay'], categories=months_order, ordered=True)
    
    monthly_sales = df.groupby('Ay', observed=True)['Toplam Tutar'].sum()

    # --- GÖRSELLEŞTİRME (GRAFİKLER) ---
    print("📊 Grafikler çiziliyor...")

    # İki grafik yan yana olsun (1 Satır, 2 Sütun)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Grafik 1: Kategori Satışları (Bar Chart)
    sns.barplot(x=category_sales.index, y=category_sales.values, ax=axes[0], palette="viridis", hue=category_sales.index, legend=False)
    axes[0].set_title("Kategori Bazlı Toplam Satışlar")
    axes[0].set_ylabel("Tutar (TL)")
    axes[0].tick_params(axis='x', rotation=45)

    # Grafik 2: Aylık Satış Trendi (Line Chart)
    sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, ax=axes[1], marker='o', color='b', linewidth=2.5)
    axes[1].set_title("Aylık Satış Performansı")
    axes[1].set_ylabel("Tutar (TL)")
    axes[1].tick_params(axis='x', rotation=45)
    
    # Başlık ve Düzen
    plt.suptitle(f"2025 Yılı Satış Analiz Raporu\nToplam Ciro: {total_revenue:,.0f} TL", fontsize=16)
    plt.tight_layout()

    # Grafiği Kaydet
    plt.savefig("satis_raporu.png")
    print("✅ Başarılı! 'satis_raporu.png' olarak grafik kaydedildi.")
    
    # Dosyayı otomatik aç (Windows için)
    os.startfile("satis_raporu.png")

if __name__ == "__main__":
    analyze_sales()