# e-commerce-dashboard-streamlit

## Deskripsi Proyek
Dashboard ini dibuat untuk menganalisis data transaksi e-commerce dengan visualisasi interaktif menggunakan Streamlit. Proyek ini mencakup eksplorasi data dan pembuatan dashboard berbasis Python.

## Struktur Proyek
```
e-commerce-dashboard-streamlit/
│── dashboard/
│   │── dashboard.py  # Aplikasi Streamlit untuk visualisasi data
│   │── master_orders_2018.csv  # Dataset utama
│
│── data/
│   # Folder ini bisa digunakan untuk menyimpan dataset tambahan jika diperlukan
│
│── Proyek_Analisis_Data.ipynb  # Notebook untuk eksplorasi dan analisis data
│── README.md  # Dokumentasi proyek
│── requirements.txt  # Daftar dependensi untuk menjalankan proyek
│── url.txt  # URL referensi terkait proyek
```

## Persiapan Environment
### Menggunakan Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```
### Menggunakan Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```
## Menjalankan Streamlit App
```
streamlit run dashboard/dashboard.py
```

## Library yang Digunakan
- pandas: Manipulasi data
- matplotlib & seaborn: Visualisasi data
- streamlit: Pembuatan dashboard interaktif
- plotly: Visualisasi interaktif tambahan
- babel: Formatting angka dan mata uang

## Catatan
Pastikan semua dependensi telah diinstal sebelum menjalankan proyek. Jika terdapat error terkait dataset, pastikan path ke file CSV sudah benar sesuai struktur folder di atas.
