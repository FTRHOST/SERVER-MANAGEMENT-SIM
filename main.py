import json
import os
import random
import time
import sys
from typing import List, Dict, Any

# ==========================================
# 🎨 VISUAL STYLING & CONFIG
# ==========================================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'  # Kuning
    FAIL = '\033[91m'     # Merah
    ENDC = '\033[0m'      # Reset warna
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

DATA_FILE = "cloud_server_data.json"
ServerRecord = Dict[str, Any]
ServerDataSet = List[ServerRecord]

# ==========================================
# 🛠️ HELPER FUNCTIONS (Visuals)
# ==========================================

def clear_screen():
    """Membersihkan layar dengan dukungan Google Colab."""
    try:
        # Cek jika berjalan di Google Colab / Jupyter
        from IPython.display import clear_output
        clear_output(wait=True)
    except ImportError:
        # Jika di Terminal biasa (Windows/Linux)
        os.system("cls" if os.name == "nt" else "clear")

def print_banner():
    """Menampilkan ASCII Art Header."""
    banner = f"""{Colors.CYAN}{Colors.BOLD}
   ______ __                     __  __  __
  / ____// /____  __  __ ____   / / / / / /__  __
 / /    / // __ \/ / / // __ \ / / / / / // / / /
/ /___ / // /_/ // /_/ // /_/ // /_/ // // /_/ /
\____//_/ \____/ \__,_//_____/ \____//_/ \__,_/
       -- SERVER MANAGEMENT SIMULATOR BY FTR--
    {Colors.ENDC}"""
    print(banner)

def draw_progress_bar(percentage: float, width: int = 10) -> str:
    """Membuat visual bar chart sederhana: [|||||     ]"""
    filled_length = int(width * percentage // 100)
    bar = '█' * filled_length + '░' * (width - filled_length)

    # Tentukan warna berdasarkan load
    color = Colors.GREEN
    if percentage > 50: color = Colors.WARNING
    if percentage > 80: color = Colors.FAIL

    return f"{color}[{bar}] {percentage:>5.1f}%{Colors.ENDC}"

def print_table_header():
    """Mencetak header tabel dashboard."""
    print(f"{Colors.HEADER}{'ID':<8} | {'NAMA SERVER':<15} | {'LOKASI':<10} | {'STATUS':<10} | {'CPU LOAD':<18} | {'RAM LOAD':<18} | {'UPTIME'}{Colors.ENDC}")
    print("-" * 105)

# ==========================================
# 💾 FILE HANDLING
# ==========================================

def load_data(filename: str) -> ServerDataSet:
    if not os.path.exists(filename): return []
    try:
        with open(filename, "r") as f: return json.load(f)
    except: return []

def save_data(filename: str, data: ServerDataSet) -> None:
    with open(filename, "w") as f: json.dump(data, f, indent=4)
    print(f"\n{Colors.GREEN}✅ Data tersimpan otomatis.{Colors.ENDC}")
    time.sleep(1)

# ==========================================
# 🎮 LOGIC SIMULASI & CRUD
# ==========================================

def simulate_activity(data: ServerDataSet) -> ServerDataSet:
    """Mengupdate statistik server agar terlihat 'hidup'."""
    for server in data:
        if server["status"] == "Aktif":
            server["uptime"] += 1

            # Simulasi fluktuasi CPU
            change = random.uniform(-5.0, 5.0)
            server["penggunaan_cpu"] = max(0.0, min(100.0, server["penggunaan_cpu"] + change))

            # Simulasi fluktuasi RAM
            change_ram = random.uniform(-2.0, 2.0)
            server["penggunaan_memori"] = max(0.0, min(100.0, server["penggunaan_memori"] + change_ram))

            # Random event: Server crash jarang terjadi (1% chance)
            if random.random() < 0.01:
                server["status"] = "CRASHED"
                server["penggunaan_cpu"] = 0.0

    return data

def create_server(data: ServerDataSet) -> ServerDataSet:
    print(f"\n{Colors.CYAN}--- ➕ DEPLOY SERVER BARU ---{Colors.ENDC}")
    new_server = {
        "id": input("ID Server (unik) : "),
        "nama": input("Nama Server    : "),
        "lokasi": input("Lokasi Datacenter: "),
        "status": "Aktif",
        "uptime": 0,
        "penggunaan_cpu": random.uniform(10, 30),
        "penggunaan_memori": random.uniform(10, 20)
    }
    data.append(new_server)
    print(f"{Colors.GREEN}Server berhasil di-deploy!{Colors.ENDC}")
    time.sleep(1)
    return data

def read_dashboard(data: ServerDataSet):
    """Menampilkan dashboard utama."""
    clear_screen()
    print_banner()

    if not data:
        print(f"\n{Colors.WARNING}Belum ada server yang aktif. Silakan deploy server baru.{Colors.ENDC}")
        return

    print_table_header()
    for s in data:
        # Warna Status
        status_display = f"{Colors.GREEN}● Aktif{Colors.ENDC}"
        if s['status'] != "Aktif":
            status_display = f"{Colors.FAIL}■ {s['status']}{Colors.ENDC}"

        print(f"{s['id']:<8} | {s['nama']:<15} | {s['lokasi']:<10} | {status_display:<19} | {draw_progress_bar(s['penggunaan_cpu'])} | {draw_progress_bar(s['penggunaan_memori'])} | {s['uptime']}s")

    print("-" * 105)

def update_server(data: ServerDataSet) -> ServerDataSet:
    target = input(f"\n{Colors.BLUE}Masukkan ID Server yang ingin dikonfigurasi: {Colors.ENDC}")
    for s in data:
        if s['id'] == target:
            print(f"Mengedit {s['nama']}... (Tekan Enter untuk skip)")
            nama = input(f"Nama baru [{s['nama']}]: ")
            status = input(f"Status (Aktif/Maintenance/Off) [{s['status']}]: ")

            if nama: s['nama'] = nama
            if status: s['status'] = status
            print(f"{Colors.GREEN}Konfigurasi diupdate.{Colors.ENDC}")
            return data
    print(f"{Colors.FAIL}ID tidak ditemukan.{Colors.ENDC}")
    time.sleep(1)
    return data

def delete_server(data: ServerDataSet) -> ServerDataSet:
    target = input(f"\n{Colors.FAIL}Masukkan ID Server untuk TERMINASI: {Colors.ENDC}")
    initial_len = len(data)
    data = [s for s in data if s['id'] != target]
    if len(data) < initial_len:
        print(f"{Colors.WARNING}Server telah dihapus dari cluster.{Colors.ENDC}")
    else:
        print("Server tidak ditemukan.")
    time.sleep(1)
    return data

def search_server(data: ServerDataSet):
    q = input(f"\n{Colors.BLUE}🔍 Cari (Nama/Lokasi): {Colors.ENDC}").lower()
    found = [s for s in data if q in s['nama'].lower() or q in s['lokasi'].lower()]

    print(f"\n{Colors.BOLD}--- HASIL PENCARIAN ---{Colors.ENDC}")
    for s in found:
         print(f"ID: {s['id']} | Nama: {s['nama']} | Lokasi: {s['lokasi']}")
    input("\nTekan Enter untuk kembali...")

def calculate_stats(data: ServerDataSet):
    if not data: return
    total_cpu = sum(s['penggunaan_cpu'] for s in data)
    avg_cpu = total_cpu / len(data)

    print(f"\n{Colors.BOLD}--- 📊 ANALITIK CLUSTER ---{Colors.ENDC}")
    print(f"Total Server : {len(data)}")
    print(f"Rata-rata CPU: {avg_cpu:.2f}%")
    print(f"Total Uptime : {sum(s['uptime'] for s in data)} detik")

    if avg_cpu > 80:
        print(f"{Colors.FAIL}PERINGATAN: Cluster Overload! Tambahkan server baru.{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}Status Cluster: Sehat{Colors.ENDC}")
    input("\nTekan Enter untuk kembali...")

def sort_servers(data: ServerDataSet) -> ServerDataSet:
    print("\nUrutkan berdasarkan: [1] CPU Load  [2] Nama  [3] Uptime")
    c = input("Pilihan: ")
    if c == '1':
        data.sort(key=lambda x: x['penggunaan_cpu'], reverse=True)
    elif c == '2':
        data.sort(key=lambda x: x['nama'])
    elif c == '3':
        data.sort(key=lambda x: x['uptime'], reverse=True)
    return data

# ==========================================
# 🚀 MAIN LOOP
# ==========================================

def main():
    data = load_data(DATA_FILE)

    while True:
        # 1. Update Simulasi
        data = simulate_activity(data)

        # 2. Render Tampilan
        read_dashboard(data)

        # 3. Tampilkan Menu
        print(f"\n{Colors.BOLD}COMMAND CENTER:{Colors.ENDC}")
        print(f"[1] {Colors.GREEN}Deploy Server{Colors.ENDC}   [2] {Colors.BLUE}Config Server{Colors.ENDC}   [3] {Colors.FAIL}Terminasi Server{Colors.ENDC}")
        print(f"[4] Search          [5] Analitik        [6] Sortir")
        print(f"[7] {Colors.WARNING}Save & Exit{Colors.ENDC}     [Enter] Refresh")

        choice = input(f"\n{Colors.CYAN}root@cloud-manager:~$ {Colors.ENDC}")

        if choice == "1": data = create_server(data)
        elif choice == "2": data = update_server(data)
        elif choice == "3": data = delete_server(data)
        elif choice == "4": search_server(data)
        elif choice == "5": calculate_stats(data)
        elif choice == "6": data = sort_servers(data)
        elif choice == "7":
            save_data(DATA_FILE, data)
            print("Shutting down system...")
            break
        elif choice == "":
            pass
        else:
            print("Command unknown.")
            time.sleep(0.5)

if __name__ == "__main__":
    main()
