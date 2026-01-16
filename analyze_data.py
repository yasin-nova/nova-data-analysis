import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Görselleştirme Ayarları
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def analyze_sales():
    print("--- 📊 E-TİCARET VERİ ANALİZ ARACI ---")
    print("Lütfen analiz edilecek Excel dosyasının adını girin.")
    print("(Örnek: satislar.xlsx veya sadece satislar)")
    
    # 1. Kullanıcıdan Dosya İsmi İsteme (İNTERAKTİF KISIM)
    file_input = input("Dosya Adı: ").strip() # Boşlukları temizle
    
    # Eğer kullanıcı uzantıyı yazmadıysa biz ekleyelim
    if not file_input.endswith(".xlsx"):
        file_input += ".xlsx"
    
    print(f"\n🔄 '{file_input}' dosyası aranıyor...")

    # 2. Dosya Kontrolü ve Okuma
    if not os.path.exists(file_input):
        print(f"❌ HATA: '{file_input}' adında bir dosya bulunamadı!")
        print("Lütfen dosyanın bu klasörde olduğundan emin olun.")
        input("Çıkmak için Enter'a basın...") # Konsol hemen kapanmasın diye
        sys.exit()

    try:
        df = pd.read_excel(file_input)
        print("✅ Dosya başarıyla yüklendi!")
    except Exception as e:
        print(f"❌ Dosya okunurken bir hata oluştu: {e}")
        return

    # Tarih sütununu datetime formatına çevir
    # Sütun isimleri farklı olabilir diye kontrol edelim (Opsiyonel ama güvenli)
    if 'Tarih' not in df.columns or 'Toplam Tutar' not in df.columns:
        print("❌ HATA: Excel dosyasında 'Tarih' ve 'Toplam Tutar' sütunları bulunmalı.")
        return

    df['Tarih'] = pd.to_datetime(df['Tarih'])

    # --- ANALİZLER ---

    # 1. Toplam Ciro
    total_revenue = df['Toplam Tutar'].sum()
    print(f"\n💰 TOPLAM YILLIK CİRO: {total_revenue:,.2f} TL")

    # 2. En Çok Satan Kategori
    if 'Kategori' in df.columns:
        category_sales = df.groupby('Kategori')['Toplam Tutar'].sum().sort_values(ascending=False)
        best_category = category_sales.index[0]
        print(f"🏆 EN ÇOK SATAN KATEGORİ: {best_category} ({category_sales.iloc[0]:,.2f} TL)")
    else:
        print("⚠️ 'Kategori' sütunu bulunamadığı için kategori analizi atlandı.")

    # 3. Aylık Trend
    df['Ay'] = df['Tarih'].dt.month_name()
    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    df['Ay'] = pd.Categorical(df['Ay'], categories=months_order, ordered=True)
    monthly_sales = df.groupby('Ay', observed=True)['Toplam Tutar'].sum()

    # --- GÖRSELLEŞTİRME ---
    print("📊 Grafikler çiziliyor...")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Kategori Grafiği
    if 'Kategori' in df.columns:
        sns.barplot(x=category_sales.index, y=category_sales.values, ax=axes[0], palette="viridis", hue=category_sales.index, legend=False)
        axes[0].set_title("Kategori Bazlı Satışlar")
        axes[0].tick_params(axis='x', rotation=45)
    
    # Aylık Trend Grafiği
    sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, ax=axes[1], marker='o', color='b', linewidth=2.5)
    axes[1].set_title("Aylık Satış Trendi")
    axes[1].tick_params(axis='x', rotation=45)

    plt.suptitle(f"Satış Analiz Raporu\nCiro: {total_revenue:,.0f} TL", fontsize=16)
    plt.tight_layout()

    # Rapor İsmi de Dinamik Olsun
    report_name = f"RAPOR_{file_input.replace('.xlsx', '')}.png"
    plt.savefig(report_name)
    
    print(f"✅ Analiz Bitti! '{report_name}' dosyası oluşturuldu.")
    os.startfile(report_name)

if __name__ == "__main__":
    analyze_sales()