# Partner Grade - Odoo Module

**Partner Grade** adalah modul kustom Odoo yang menambahkan fitur pengelompokan mitra (partner) berdasarkan **tingkatan atau grade** tertentu, berguna untuk segmentasi pelanggan, pemasok, atau mitra bisnis lainnya.

## Fitur Utama

- Tambahan field `grade` pada model `res.partner`
- Pengelompokan partner berdasarkan grade (misalnya: A, B, C, VIP, dll.)
- Tampilan kolom grade pada list view partner
- Filter dan pencarian berdasarkan grade
- Cocok untuk analisis, CRM, dan segmentasi pemasaran

## Struktur Modul

- **Model**
  - Menambahkan field `grade` ke model `res.partner` menggunakan `inherit`
- **View**
  - Modifikasi form dan tree view partner untuk menampilkan dan mengedit grade
- **Data**
  - Tambahan domain/filter untuk pencarian berdasarkan grade (opsional)

## Instalasi

1. Clone repositori ini ke dalam direktori `addons` Odoo kamu:

   ```bash
   git clone https://github.com/yourusername/partner_grade.git
