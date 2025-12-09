[![Run on Replit](https://img.shields.io/badge/Replit-Run%20on%20Replit-blue?logo=replit&logoColor=white)](https://replit.com/@fathironmy3/SERVER-MANAGEMENT-SIM?v=1)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/FTRHOST/SERVER-MANAGEMENT-SIM/blob/main/UAS_PemroDas.ipynb)
# Server Management Simulator

Simulasi manajemen server sederhana berbasis terminal (CLI) yang ditulis dengan Python. Proyek ini mensimulasikan dashboard monitoring cloud server di mana Anda dapat melakukan deploy, konfigurasi, monitoring, dan manajemen server.

## Fitur

- **Dashboard Monitoring Real-time**: Menampilkan status server, penggunaan CPU, RAM, dan uptime.
- **Simulasi Aktivitas**: CPU dan RAM load berubah-ubah secara dinamis untuk mensimulasikan server yang sedang bekerja.
- **Manajemen Server (CRUD)**:
  - **Deploy**: Menambahkan server baru.
  - **Config**: Mengubah nama atau status server (Aktif/Maintenance/Off).
  - **Terminasi**: Menghapus server dari cluster.
- **Pencarian & Sortir**: Mencari server berdasarkan nama/lokasi dan mengurutkan berdasarkan beban CPU atau nama.
- **Analitik**: Melihat statistik rata-rata penggunaan resource cluster.
- **Penyimpanan Data**: Data server disimpan dalam format JSON (`cloud_server_data.json`) sehingga tidak hilang saat program ditutup.

## Cara Menjalankan di Replit

Proyek ini sudah dikonfigurasi untuk berjalan langsung di Replit.

1. **Fork/Clone** repositori ini ke akun Replit Anda.
2. Klik tombol **Run** (berwarna hijau) di bagian atas layar.
3. Program akan berjalan di tab "Console".
4. Gunakan input angka [1-7] untuk berinteraksi dengan menu.

## Struktur File

- `main.py`: Kode utama program.
- `cloud_server_data.json`: File database (dibuat otomatis jika belum ada).
- `.replit`: Konfigurasi untuk menjalankan project di Replit.
- `replit.nix`: Konfigurasi environment (Python) di Replit.

## Kontrol

- `[Enter]` di menu utama akan me-refresh dashboard dan memperbarui data simulasi (CPU/RAM usage).
- `Ctrl + C` untuk menghentikan program secara paksa (data mungkin tidak tersimpan), disarankan menggunakan menu `[7] Save & Exit`.

---
Dibuat untuk tujuan edukasi dan simulasi sederhana.
