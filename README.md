# 🛒 Odoo API ile Excel'den Ürün Aktarma

Bu proje, **Odoo API kullanarak** Excel dosyanızdaki ürünleri **otomatik olarak Odoo'ya eklemenizi veya güncellemenizi sağlar.**  
🚀 **Barkod tekrarlarını kontrol eder ve mevcut ürünleri günceller.**  
📦 **Ürün niteliklerini doğru şekilde eşleştirir.**  
🛠 **Ölçü birimi ve kategori eksikliklerini otomatik tamamlar.**

---

## 📌 Özellikler

✅ **Excel'den ürünleri Odoo'ya aktarır**  
✅ **Mevcut ürünleri günceller, tekrar eklemeyi engeller**  
✅ **Ürün niteliklerini doğru şekilde içeri alır**  
✅ **Otomatik ölçü birimi ve kategori tanımlamaları yapar**  
✅ **Barkod hatalarını önler, iç referansları temizler**  

---

## 🛠 Gereksinimler

- **Python 3.8+**
- **pandas** kütüphanesi
- **xmlrpc.client** modülü

Kurulum:
```sh
pip install pandas
```
# 🚀 Kullanım

## 1️⃣ Excel Dosyanızı Hazırlayın

Başlık satırlarının şu şekilde olduğundan emin olun:

![Ekran Resmi 2025-03-17 15 20 47](https://github.com/user-attachments/assets/2991f0bd-87a7-44d7-9487-95ff16376edf)

## 2️⃣ Odoo Bağlantısını Güncelleyin
```python
url = "http://odooadresiniz.com"
db = "db-name"
username = "admin"
password = "şifre"
```
## 3️⃣ Script’i Çalıştırın
```sh
python main.py
```
![Ekran Resmi 2025-03-17 15 23 10](https://github.com/user-attachments/assets/4a221c2f-5b01-4b4e-a8c5-145be09d4ded)

![Ekran Resmi 2025-03-17 15 23 27](https://github.com/user-attachments/assets/acb3f78d-6fcc-4fdc-9652-289e58603eb2)


# ✅ Ürünler Odoo’ya aktarılacak ve güncellenecek! 🎉
