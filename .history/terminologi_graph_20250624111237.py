import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from typing import Dict, Optional, Union

def get_input_angka(prompt: str) -> int:
    """Fungsi untuk memastikan input adalah angka integer non-negatif."""
    while True:
        try:
            nilai = int(input(prompt))
            if nilai >= 0:
                return nilai
            else:
                print("Input tidak boleh negatif. Silakan coba lagi.")
        except ValueError:
            print("Input tidak valid. Harap masukkan sebuah angka integer.")

def buat_graf_sederhana_havel_hakimi(derajat_simpul: Dict[int, int]) -> Optional[nx.Graph]:
    """
    Membuat Graf Sederhana menggunakan algoritma Havel-Hakimi.
    Mengembalikan None jika urutan derajat tidak bisa dibuat menjadi Graf Sederhana.
    """
    urutan_derajat = list(derajat_simpul.values())
    
    # Validasi Havel-Hakimi
    if not nx.is_graphical(urutan_derajat, method='havel-hakimi'):
        print("\n[!] GAGAL: Urutan derajat ini TIDAK BISA dibentuk menjadi Graf Sederhana.")
        print("    Coba periksa apakah ada derajat yang lebih besar atau sama dengan jumlah simpul.")
        return None

    # Jika valid, buat grafnya
    G_temp = nx.havel_hakimi_graph(urutan_derajat)
    
    # Relabel simpul dari 0,1,2... ke 1,2,3...
    G = nx.Graph()
    simpul_asli = list(derajat_simpul.keys())
    mapping = {i: simpul_asli[i] for i in range(len(simpul_asli))}
    
    for u, v in G_temp.edges():
        G.add_edge(mapping[u], mapping[v])
    G.add_nodes_from(simpul_asli) # Menambah simpul derajat 0 jika ada

    print("\nGraf Sederhana berhasil dibuat menggunakan algoritma Havel-Hakimi.")
    return G

def buat_graf_ganda_configuration_model(derajat_simpul: Dict[int, int]) -> nx.MultiGraph:
    """
    Membuat Graf Ganda (Multigraph) yang pasti memenuhi urutan derajat,
    menggunakan algoritma Configuration Model. Loop dan sisi ganda mungkin terbentuk.
    """
    G = nx.MultiGraph()
    
    # Buat daftar 'stub' atau 'titik koneksi' untuk setiap simpul
    daftar_stub = []
    for simpul, derajat in derajat_simpul.items():
        daftar_stub.extend([simpul] * derajat)

    # Acak urutan stub untuk membuat koneksi yang acak
    random.shuffle(daftar_stub)

    # Pasangkan stub untuk membuat sisi
    for i in range(0, len(daftar_stub), 2):
        u = daftar_stub[i]
        if i + 1 < len(daftar_stub):
            v = daftar_stub[i+1]
            G.add_edge(u, v)
            
    G.add_nodes_from(derajat_simpul.keys())

    print("\nGraf Ganda (Multigraph) berhasil dibuat menggunakan Configuration Model.")
    print("Sisi ganda atau loop mungkin telah dibuat untuk memenuhi derajat.")
    return G

def tampilkan_info_graf(G: Union[nx.Graph, nx.MultiGraph]):
    """Menampilkan visualisasi graf dan informasinya."""
    if G is None:
        return

    pos = nx.spring_layout(G, seed=42, k=1.5/np.sqrt(G.number_of_nodes()))
    plt.figure(figsize=(10, 8))
    nx.draw(
        G, pos, with_labels=True, node_color='skyblue', node_size=2000,
        font_size=14, font_weight='bold', edge_color='black', width=1.5
    )
    plt.title(f"Visualisasi Graf ({type(G).__name__})", size=18)
    plt.show()

    print("\n" + "="*40)
    print("Informasi Graf yang Dihasilkan")
    print("="*40)
    
    print(f"\nMatriks Ketetanggaan:")
    matriks = nx.to_numpy_array(G, nodelist=sorted(G.nodes()))
    print(matriks)
    if isinstance(G, nx.MultiGraph):
        print("Catatan: Untuk Multigraph, nilai matriks menunjukkan JUMLAH sisi/loop.")

    print("\nDerajat Aktual Setiap Simpul:")
    derajat_aktual = dict(G.degree())
    for simpul, nilai_derajat in sorted(derajat_aktual.items()):
        print(f"  - Derajat simpul {simpul}: {nilai_derajat}")

def main():
    """Fungsi utama untuk menjalankan program."""
    print("--- Program Pembuat Graf dari Urutan Derajat ---")
    
    jumlah_simpul = get_input_angka("Masukkan jumlah total simpul (nodes): ")
    if jumlah_simpul == 0:
        print("Tidak ada simpul yang dibuat. Program selesai.")
        return

    simpul_list = range(1, jumlah_simpul + 1)
    print("-" * 30)

    derajat_input: Dict[int, int] = {}
    for simpul in simpul_list:
        derajat_input[simpul] = get_input_angka(f"Masukkan derajat untuk simpul {simpul}: ")
    
    # Validasi universal: total derajat harus genap
    if sum(derajat_input.values()) % 2 != 0:
        print("\n[!] GAGAL: Total semua derajat harus genap. Program dihentikan.")
        return
    
    print("\n" + "="*40)
    print("PILIH JENIS GRAF YANG INGIN DIBUAT")
    print("1. Graf Sederhana (Aturan Ketat: Tanpa sisi ganda/loop. Mungkin gagal jika input tidak memungkinkan).")
    print("2. Graf Ganda/Multigraph (Aturan Fleksibel: Sisi ganda/loop diizinkan. Hampir selalu berhasil).")
    print("="*40)
    
    pilihan = ""
    while pilihan not in ["1", "2"]:
        pilihan = input("Masukkan pilihan Anda (1 atau 2): ")

    graf_hasil = None
    if pilihan == "1":
        graf_hasil = buat_graf_sederhana_havel_hakimi(derajat_input)
    elif pilihan == "2":
        graf_hasil = buat_graf_ganda_configuration_model(derajat_input)
        
    # Tampilkan info jika graf berhasil dibuat
    if graf_hasil:
        tampilkan_info_graf(graf_hasil)
    
    print("\nProgram selesai.")

if __name__ == "__main__":
    main()