import xmlrpc.client
import pandas as pd

# **Odoo Sunucu Bilgileri**
url = "http://odooadresiniz.com"
db = "db-name"
username = "kullanici-adi"
password = "parola"

# **Odoo API Bağlantısı**
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

if not uid:
    raise Exception("Kimlik doğrulama başarısız!")

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# **Excel dosyasını oku ve sütun isimlerini temizle**
df = pd.read_excel("urunler.xlsx")
df.columns = df.columns.str.strip()  # Boşlukları temizle
df = df.fillna('')  # Tüm NaN değerleri boş string olarak değiştir

# **Ürün bilgilerini saklamak için değişkenler**
current_product = None
product_nitelikler = []

for index, row in df.iterrows():
    # **Eğer İç Referans boş değilse, yeni ürün başlıyor**
    if row['İç Referans'] != '':
        # Önceki ürün varsa Odoo'ya kaydet veya güncelle
        if current_product:
            # **Barkod Kontrolü**
            existing_product = models.execute_kw(db, uid, password, 'product.template', 'search',
                                                 [[('barcode', '=', current_product['barcode'])]])

            if existing_product:
                product_id = existing_product[0]
                print(f"🔄 {current_product['name']} ürünü zaten mevcut! Güncelleniyor...")

                # **Mevcut Ürünü Güncelle**
                models.execute_kw(db, uid, password, 'product.template', 'write',
                                  [[product_id], current_product])
            else:
                # **Yeni Ürünü Odoo'ya Kaydet**
                product_id = models.execute_kw(db, uid, password, 'product.template', 'create', [current_product])
                print(f"✅ {current_product['name']} ürünü başarıyla eklendi!")

            # **Ürüne Ait Nitelikleri Ekle veya Güncelle**
            for attr_name, attr_value in product_nitelikler:
                attribute_id = models.execute_kw(db, uid, password, 'product.attribute', 'search',
                                                 [[('name', '=', attr_name)]])
                if not attribute_id:
                    attribute_id = models.execute_kw(db, uid, password, 'product.attribute', 'create',
                                                     [{'name': attr_name}])
                else:
                    attribute_id = attribute_id[0]

                value_id = models.execute_kw(db, uid, password, 'product.attribute.value', 'search',
                                             [[('name', '=', attr_value), ('attribute_id', '=', attribute_id)]])
                if not value_id:
                    value_id = models.execute_kw(db, uid, password, 'product.attribute.value', 'create',
                                                 [{'name': attr_value, 'attribute_id': attribute_id}])
                else:
                    value_id = value_id[0]

                # **Ürüne Nitelik Ekle**
                models.execute_kw(db, uid, password, 'product.template.attribute.line', 'create', [{
                    'product_tmpl_id': product_id,
                    'attribute_id': attribute_id,
                    'value_ids': [(6, 0, [value_id])]
                }])

        # **Barkod ve İç Referansı Temizle**
        barcode = str(row['Barkod']).strip()
        if barcode.endswith(".0"):  # Eğer barkod .0 ile bitiyorsa kaldır
            barcode = barcode[:-2]

        default_code = str(row['İç Referans']).strip()
        if default_code.endswith(".0"):  # Eğer iç referans .0 ile bitiyorsa kaldır
            default_code = default_code[:-2]

        # **Ölçü Birimi İşleme**
        uom_name = str(row.get('Ölçü Birimi', '')).strip()
        if not uom_name:
            uom_name = "Units"

        uom_id = models.execute_kw(db, uid, password, 'uom.uom', 'search', [[('name', '=', uom_name)]])
        if not uom_id:
            uom_category_id = models.execute_kw(db, uid, password, 'uom.category', 'search', [[('name', '=', "Unit")]])
            if not uom_category_id:
                uom_category_id = models.execute_kw(db, uid, password, 'uom.category', 'create', [{'name': "Unit"}])
            else:
                uom_category_id = uom_category_id[0]

            uom_id = models.execute_kw(db, uid, password, 'uom.uom', 'create', [
                {'name': uom_name, 'category_id': uom_category_id, 'factor_inv': 1.0, 'uom_type': 'bigger'}])
        else:
            uom_id = uom_id[0]

        # **Kategori İşleme**
        category_name = str(row.get('Ürün Kategorisi', '')).strip()
        if not category_name:
            category_name = "Genel"

        category_id = models.execute_kw(db, uid, password, 'product.category', 'search',
                                        [[('name', '=', category_name)]])
        if not category_id:
            category_id = models.execute_kw(db, uid, password, 'product.category', 'create', [{'name': category_name}])
        else:
            category_id = category_id[0]

        current_product = {
            'name': row['Adı'],
            'default_code': default_code,
            'barcode': barcode,
            'list_price': row.get('Satış Fiyatı', 0.0),
            'uom_id': uom_id,
            'categ_id': category_id,
        }
        product_nitelikler = []  # Yeni ürün için nitelikleri sıfırla

    # **Eğer Nitelik ve Değer alanları doluysa, listeye ekle**
    attr_name = str(row['Nitelik']).strip()
    attr_value = str(row['Değer']).strip()

    if attr_name and attr_value:
        product_nitelikler.append((attr_name, attr_value))

# **Son ürünü de Odoo'ya ekle veya güncelle**
if current_product:
    existing_product = models.execute_kw(db, uid, password, 'product.template', 'search',
                                         [[('barcode', '=', current_product['barcode'])]])

    if existing_product:
        product_id = existing_product[0]
        print(f"🔄 {current_product['name']} ürünü zaten mevcut! Güncelleniyor...")
        models.execute_kw(db, uid, password, 'product.template', 'write', [[product_id], current_product])
    else:
        product_id = models.execute_kw(db, uid, password, 'product.template', 'create', [current_product])
        print(f"✅ {current_product['name']} ürünü başarıyla eklendi!")

    for attr_name, attr_value in product_nitelikler:
        attribute_id = models.execute_kw(db, uid, password, 'product.attribute', 'search', [[('name', '=', attr_name)]])
        if not attribute_id:
            attribute_id = models.execute_kw(db, uid, password, 'product.attribute', 'create', [{'name': attr_name}])
        else:
            attribute_id = attribute_id[0]

        value_id = models.execute_kw(db, uid, password, 'product.attribute.value', 'search',
                                     [[('name', '=', attr_value), ('attribute_id', '=', attribute_id)]])
        if not value_id:
            value_id = models.execute_kw(db, uid, password, 'product.attribute.value', 'create',
                                         [{'name': attr_value, 'attribute_id': attribute_id}])
        else:
            value_id = value_id[0]

        models.execute_kw(db, uid, password, 'product.template.attribute.line', 'create', [{
            'product_tmpl_id': product_id,
            'attribute_id': attribute_id,
            'value_ids': [(6, 0, [value_id])]
        }])

print("🎉 Tüm ürünler başarıyla içeri aktarıldı!")
