import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from typing import Dict, List, Optional

def dapatkan_input_angka(prompt: str) -> int:
    """
    Meminta input dari pengguna dan memastikan input adalah integer non-negatif.

    Args:
        prompt (str): Pesan yang akan ditampilkan kepada pengguna.

    Returns:
        int: Angka integer non-negatif yang dimasukkan oleh pengguna.
    """
    while True:
        try:
            nilai = int(input(prompt))
            if nilai >= 0:
                return nilai
            else:
                print("Input tidak boleh negatif. Silakan coba lagi.")
        except ValueError:
            print("Input tidak valid. Harap masukkan sebuah angka integer.")

def buat_graf_dari_derajat(derajat_simpul: Dict[int, int]) -> nx.MultiGraph:
    """
    Membuat sebuah MultiGraph menggunakan algoritma Configuration Model berdasarkan
    urutan derajat yang diberikan.

    Algoritma ini secara alami dapat menghasilkan sisi ganda (multiple edges) dan
    gelung (loops) untuk memenuhi derajat yang ditentukan.

    Args:
        derajat_simpul (Dict[int, int]): Dictionary dengan simpul sebagai kunci
                                         dan derajat yang diinginkan sebagai nilai.

    Returns:
        nx.MultiGraph: Graf yang telah dibuat.
    """
    G = nx.MultiGraph()
    
    # Buat daftar 'stub' atau 'titik koneksi' untuk setiap simpul
    # Contoh: jika simpul 1 memiliki derajat 3, ia akan muncul 3 kali
    daftar_stub = []
    for simpul, derajat in derajat_simpul.items():
        daftar_stub.extend([simpul] * derajat)

    # Acak urutan stub untuk membuat koneksi yang acak
    random.shuffle(daftar_stub)

    # Pasangkan stub untuk membuat sisi
    # Loop melalui daftar stub secara berpasangan
    for i in range(0, len(daftar_stub), 2):
        u = daftar_stub[i]
        # Pastikan tidak ada stub ganjil yang tersisa
        if i + 1 < len(daftar_stub):
            v = daftar_stub[i+1]
            G.add_edge(u, v)
            
    # Tambahkan simpul yang mungkin tidak memiliki sisi (derajat 0)
    G.add_nodes_from(derajat_simpul.keys())

    print("\nGraf berhasil dibuat menggunakan Configuration Model.")
    print(f"Total simpul: {G.number_of_nodes()}")
    print(f"Total sisi (termasuk sisi ganda/loop): {G.number_of_edges()}")
    return G

def tampilkan_info_graf(G: Optional[nx.MultiGraph]):
    """
    Menampilkan visualisasi graf, matriks ketetanggaan, daftar sisi, dan
    derajat setiap simpul.

    Args:
        G (Optional[nx.MultiGraph]): Graf untuk ditampilkan. Jika None,
                                     program akan berhenti.
    """
    if G is None or not G.nodes():
        print("Graf kosong, tidak ada yang bisa ditampilkan.")
        return

    # --- 1. Visualisasi Graf ---
    print("\n" + "="*40)
    print("1. Visualisasi Graf")
    print("="*40)
    
    pos = nx.spring_layout(G, seed=42, k=0.9)  # Menambah jarak antar simpul
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2500,
              font_size=12, font_weight='bold', edge_color='gray', width=1.5,
              arrows=False)
    plt.title("Visualisasi Graf Berdasarkan Urutan Derajat", size=18)
    plt.show()

    # --- 2. Matriks Ketetanggaan ---
    print("\n" + "="*40)
    print("2. Matriks Ketetanggaan (Adjacency Matrix)")
    print("="*40)
    # Mengurutkan simpul untuk matriks yang konsisten
    simpul_terurut = sorted(G.nodes())
    matriks_ketetanggaan = nx.to_numpy_array(G, nodelist=simpul_terurut)
    print(f"Simpul diurutkan sebagai: {simpul_terurut}")
    print(matriks_ketetanggaan)
    print("\nCatatan: Untuk MultiGraph, nilai matriks ini menunjukkan jumlah sisi")
    print("antara dua simpul. Nilai pada diagonal (misal: M[i,i])")
    print("menunjukkan jumlah loop pada simpul tersebut dikali 2.")


    # --- 3. Daftar Sisi (Edge List) ---
    print("\n" + "="*40)
    print("3. Daftar Semua Sisi (Edge List)")
    print("="*40)
    print("Menampilkan semua koneksi, termasuk sisi ganda dan loop.")
    print(list(G.edges()))
    
    # --- 4. Derajat Aktual Simpul ---
    print("\n" + "="*40)
    print("4. Derajat Aktual Setiap Simpul")
    print("="*40)
    derajat_aktual = dict(G.degree())
    for simpul, nilai_derajat in derajat_aktual.items():
        print(f"  - Derajat simpul {simpul}: {nilai_derajat}")

def main():
    """Fungsi utama untuk menjalankan program."""
    print("--- Program Pembuat Graf Otomatis ---")
    
    # Meminta jumlah simpul
    jumlah_simpul = dapatkan_input_angka("Masukkan jumlah total simpul (nodes): ")
    if jumlah_simpul == 0:
        print("Tidak ada simpul yang dibuat. Program selesai.")
        return

    simpul_list = range(1, jumlah_simpul + 1)
    print(f"Simpul akan diberi label dari 1 hingga {jumlah_simpul}.")
    print("-" * 30)

    # Meminta derajat dari masing-masing simpul
    derajat_input: Dict[int, int] = {}
    for simpul in simpul_list:
        derajat_input[simpul] = dapatkan_input_angka(f"Masukkan derajat untuk simpul {simpul}: ")

    # Validasi jumlah total derajat (prasyarat teorema jabat tangan)
    total_derajat = sum(derajat_input.values())
    if total_derajat % 2 != 0:
        print("\n[!] Gagal: Total semua derajat harus genap agar graf dapat dibuat.")
        print("    Jumlah derajat yang Anda masukkan adalah ganjil. Program selesai.")
        return
        
    # Buat dan tampilkan graf
    graf_hasil = buat_graf_dari_derajat(derajat_input)
    tampilkan_info_graf(graf_hasil)

if __name__ == "__main__":
    main()