# Impor library yang dibutuhkan
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from typing import Dict, Optional

def get_input_angka(prompt: str) -> int:
    """
    Fungsi untuk meminta input dari pengguna dan memastikan inputnya adalah
    sebuah angka integer non-negatif (0 atau lebih besar).
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
    Membuat Graf Ganda (Multigraph) yang pasti memenuhi urutan derajat,
    menggunakan algoritma Configuration Model. Loop dan sisi ganda akan terbentuk
    jika diperlukan untuk memenuhi derajat.
    """
    G = nx.MultiGraph()
    
    # Buat daftar 'stub' atau 'titik koneksi' untuk setiap simpul.
    daftar_stub = []
    for simpul, derajat in derajat_simpul.items():
        daftar_stub.extend([simpul] * derajat)

    # Acak urutan stub untuk membuat koneksi yang acak
    random.shuffle(daftar_stub)

    # Pasangkan stub untuk membuat sisi (edges).
    for i in range(0, len(daftar_stub), 2):
        u = daftar_stub[i]
        if i + 1 < len(daftar_stub):
            v = daftar_stub[i+1]
            G.add_edge(u, v)
            
    G.add_nodes_from(derajat_simpul.keys())

    print("\nGraf Ganda (Multigraph) berhasil dibuat menggunakan algoritma Configuration Model.")
    print("Sisi ganda dan loop digunakan untuk memenuhi derajat.")
    return G

def tampilkan_info_graf(G: Optional[nx.MultiGraph]):
    """
    Menampilkan visualisasi graf dan informasi detailnya.
    """
    if G is None:
        return

    pos = nx.spring_layout(G, seed=42, k=1.5/np.sqrt(G.number_of_nodes()))
    
    plt.figure(figsize=(10, 8))
    nx.draw(
        G, pos, with_labels=True, node_color='skyblue', node_size=2000,
        font_size=14, font_weight='bold', edge_color='black', width=1.5
    )
    plt.title("Visualisasi Graf Ganda (Multigraph)", size=18)
    plt.show()

    print("\n" + "="*40)
    print("Informasi Detail Graf yang Dihasilkan")
    print("="*40)
    
    print(f"\nMatriks Ketetanggaan:")
    matriks = nx.to_numpy_array(G, nodelist=sorted(G.nodes()))
    print(matriks)
    print("Catatan: Nilai matriks menunjukkan JUMLAH sisi antara dua simpul.")

    print("\nDerajat Aktual Setiap Simpul (HASIL AKHIR):")
    derajat_aktual = dict(G.degree())
    for simpul, nilai_derajat in sorted(derajat_aktual.items()):
        print(f"  - Simpul {simpul}: {nilai_derajat}")

def main():
    """Fungsi utama untuk menjalankan seluruh alur program."""
    
    # ================== PRINT DIAGNOSTIK ==================
    print("--- MENJALANKAN KODE VERSI FINAL (DENGAN CONFIGURATION MODEL) ---")
    # ======================================================
    
    jumlah_simpul = get_input_angka("Masukkan jumlah total simpul (nodes): ")
    if jumlah_simpul == 0:
        print("Tidak ada simpul yang dibuat. Program selesai.")
        return

    simpul_list = range(1, jumlah_simpul + 1)
    print("-" * 30)

    derajat_input: Dict[int, int] = {}
    for simpul in simpul_list:
        derajat_input[simpul] = get_input_angka(f"Masukkan derajat untuk simpul {simpul}: ")
    
    if sum(derajat_input.values()) % 2 != 0:
        print("\n[!] GAGAL: Total semua derajat harus bilangan genap.")
        print("    Program dihentikan karena graf tidak mungkin dibuat.")
        return
    
    graf_hasil = buat_graf_dari_derajat(derajat_input)
    tampilkan_info_graf(graf_hasil)
    
    print("\nProgram selesai.")

if __name__ == "__main__":
    main()