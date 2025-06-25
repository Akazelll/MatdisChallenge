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
    menggunakan algoritma Configuration Model. Loop dan sisi ganda mungkin terbentuk
    jika diperlukan untuk memenuhi derajat.
    """
    G = nx.MultiGraph()
    
    # Buat daftar 'stub' atau 'titik koneksi' untuk setiap simpul.
    # Contoh: jika simpul 1 memiliki derajat 7, maka angka 1 akan
    # ditambahkan 7 kali ke dalam daftar.
    daftar_stub = []
    for simpul, derajat in derajat_simpul.items():
        daftar_stub.extend([simpul] * derajat)

    # Acak urutan stub untuk membuat koneksi yang acak
    random.shuffle(daftar_stub)

    # Pasangkan stub untuk membuat sisi (edges).
    # Loop melalui daftar stub secara berpasangan.
    for i in range(0, len(daftar_stub), 2):
        u = daftar_stub[i]
        # Pastikan tidak ada stub ganjil yang tersisa di akhir
        if i + 1 < len(daftar_stub):
            v = daftar_stub[i+1]
            G.add_edge(u, v)
            
    # Tambahkan simpul yang mungkin tidak memiliki sisi (derajat 0)
    G.add_nodes_from(derajat_simpul.keys())

    print("\nGraf Ganda (Multigraph) berhasil dibuat menggunakan algoritma Configuration Model.")
    print("Sisi ganda atau loop mungkin telah dibuat untuk memenuhi derajat.")
    return G

def tampilkan_info_graf(G: Optional[nx.MultiGraph]):
    """
    Menampilkan visualisasi graf dan informasi detailnya seperti
    matriks ketetanggaan dan derajat aktual setiap simpul.
    """
    if G is None:
        print("Graf tidak ada, tidak ada yang bisa ditampilkan.")
        return

    # Atur posisi simpul untuk visualisasi yang lebih baik
    pos = nx.spring_layout(G, seed=42, k=1.5/np.sqrt(G.number_of_nodes()))
    
    # Gambar graf menggunakan Matplotlib
    plt.figure(figsize=(10, 8))
    nx.draw(
        G, pos, with_labels=True, node_color='skyblue', node_size=2000,
        font_size=14, font_weight='bold', edge_color='black', width=1.5
    )
    plt.title("Visualisasi Graf Ganda (Multigraph)", size=18)
    plt.show()

    # Tampilkan informasi detail mengenai graf di terminal
    print("\n" + "="*40)
    print("Informasi Detail Graf yang Dihasilkan")
    print("="*40)
    
    print(f"\nMatriks Ketetanggaan:")
    # Membuat matriks dari graf, diurutkan agar konsisten
    matriks = nx.to_numpy_array(G, nodelist=sorted(G.nodes()))
    print(matriks)
    print("Catatan: Nilai matriks menunjukkan JUMLAH sisi antara dua simpul.")

    print("\nDerajat Aktual Setiap Simpul:")
    # Menghitung derajat akhir dari setiap simpul di graf
    derajat_aktual = dict(G.degree())
    for simpul, nilai_derajat in sorted(derajat_aktual.items()):
        print(f"  - Simpul {simpul}: {nilai_derajat}")

def main():
    """Fungsi utama untuk menjalankan seluruh alur program."""
    print("--- Program Pembuat Graf Ganda (Multigraph) dari Derajat ---")
    
    jumlah_simpul = get_input_angka("Masukkan jumlah total simpul (nodes): ")
    if jumlah_simpul == 0:
        print("Tidak ada simpul yang dibuat. Program selesai.")
        return

    # Membuat daftar simpul, misal: [1, 2, 3, ...]
    simpul_list = range(1, jumlah_simpul + 1)
    print("-" * 30)

    # Meminta input derajat untuk setiap simpul
    derajat_input: Dict[int, int] = {}
    for simpul in simpul_list:
        derajat_input[simpul] = get_input_angka(f"Masukkan derajat untuk simpul {simpul}: ")
    
    # Validasi WAJIB: total dari semua derajat harus genap
    if sum(derajat_input.values()) % 2 != 0:
        print("\n[!] GAGAL: Total semua derajat harus bilangan genap.")
        print("    Program dihentikan karena graf tidak mungkin dibuat.")
        return
    
    # Jika validasi berhasil, langsung buat dan tampilkan graf
    graf_hasil = buat_graf_dari_derajat(derajat_input)
    tampilkan_info_graf(graf_hasil)
    
    print("\nProgram selesai.")

# Titik masuk utama saat script dijalankan
if __name__ == "__main__":
    main()