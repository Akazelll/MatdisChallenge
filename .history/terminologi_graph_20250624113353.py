# Impor library yang dibutuhkan
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# 'random' tidak lagi dibutuhkan karena networkx yang akan mengacak
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

def buat_graf_paling_andal(derajat_simpul: Dict[int, int]) -> nx.MultiGraph:
    """
    Membuat Graf Ganda (Multigraph) menggunakan FUNGSI BAWAAN networkx,
    yaitu nx.configuration_model(). Ini adalah metode paling andal.
    """
    # Buat urutan derajat dalam bentuk list, sesuai urutan simpul 1, 2, 3, ...
    # Ini penting karena nx.configuration_model perlu input list
    simpul_terurut = sorted(derajat_simpul.keys())
    urutan_derajat = [derajat_simpul[s] for s in simpul_terurut]

    # === INTI PERUBAHAN ADA DI SINI ===
    # Buat graf langsung menggunakan fungsi bawaan networkx.
    # Fungsi ini menghasilkan graf dengan simpul berlabel 0, 1, 2, ...
    G_temp = nx.configuration_model(urutan_derajat, create_using=nx.MultiGraph)
    
    # Karena G_temp memiliki simpul 0, 1, 2..., kita perlu me-relabel
    # kembali ke label asli Anda yaitu 1, 2, 3, ...
    mapping_label = {i: simpul_terurut[i] for i in range(len(simpul_terurut))}
    G = nx.relabel_nodes(G_temp, mapping_label)
    # ==================================

    print("\nGraf Ganda (Multigraph) berhasil dibuat menggunakan FUNGSI RESMI networkx.")
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
    plt.title("Visualisasi Graf Ganda (Multigraph) - Versi Final", size=18)
    plt.show()

    print("\n" + "="*40)
    print("Informasi Detail Graf yang Dihasilkan")
    print("="*40)
    
    print(f"\nMatriks Ketetanggaan:")
    matriks = nx.to_numpy_array(G, nodelist=sorted(G.nodes()))
    print(matriks)

    print("\nDerajat Aktual Setiap Simpul (HASIL AKHIR):")
    derajat_aktual = dict(G.degree())
    for simpul, nilai_derajat in sorted(derajat_aktual.items()):
        print(f"  - Simpul {simpul}: {nilai_derajat}")

def main():
    """Fungsi utama untuk menjalankan seluruh alur program."""
    print("--- MENJALANKAN KODE VERSI PAMUNGKAS (DENGAN FUNGSI BAWAAN NX) ---")
    
    jumlah_simpul = get_input_angka("Masukkan jumlah total simpul (nodes): ")
    if jumlah_simpul == 0:
        return

    simpul_list = range(1, jumlah_simpul + 1)
    print("-" * 30)

    derajat_input: Dict[int, int] = {}
    for simpul in simpul_list:
        derajat_input[simpul] = get_input_angka(f"Masukkan derajat untuk simpul {simpul}: ")
    
    if sum(derajat_input.values()) % 2 != 0:
        print("\n[!] GAGAL: Total semua derajat harus bilangan genap.")
        return
    
    # Mengganti pemanggilan fungsi ke versi yang paling andal
    graf_hasil = buat_graf_paling_andal(derajat_input)
    tampilkan_info_graf(graf_hasil)
    
    print("\nProgram selesai.")

if __name__ == "__main__":
    main()