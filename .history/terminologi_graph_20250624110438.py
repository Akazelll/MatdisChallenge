import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Optional

def dapatkan_input_angka(prompt: str) -> int:
    """
    Meminta input dari pengguna dan memastikan input adalah integer non-negatif.
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

def buat_graf_sederhana_havel_hakimi(derajat_simpul: Dict[int, int]) -> Optional[nx.Graph]:
    """
    Membuat sebuah Graf Sederhana (tanpa loop/sisi ganda) menggunakan
    implementasi dari algoritma Havel-Hakimi.

    Args:
        derajat_simpul (Dict[int, int]): Dictionary dengan simpul sebagai kunci
                                         dan derajat yang diinginkan sebagai nilai.

    Returns:
        Optional[nx.Graph]: Graf yang telah dibuat jika urutan derajat valid.
                            Mengembalikan None jika tidak valid.
    """
    # NetworkX sudah memiliki implementasi Havel-Hakimi yang andal
    # nx.is_graphical() memeriksa apakah urutan derajat bisa membentuk graf sederhana.
    # Urutan derajat harus dalam bentuk list atau tuple.
    urutan_derajat = list(derajat_simpul.values())
    
    if not nx.is_graphical(urutan_derajat):
        print("\n[!] GAGAL: Urutan derajat yang Anda masukkan TIDAK BISA dibentuk menjadi Graf Sederhana.")
        print("    (Menurut Teorema Havel-Hakimi, urutan ini tidak 'graphical').")
        return None

    # Jika valid, buat grafnya menggunakan nx.havel_hakimi_graph
    # Fungsi ini secara otomatis membangun graf sederhana dari urutan derajat.
    # Penting: Fungsi ini menghasilkan graf dengan simpul 0, 1, 2, ...
    # Kita perlu me-relabel simpul agar sesuai dengan input pengguna (1, 2, 3, ...)
    G_temp = nx.havel_hakimi_graph(urutan_derajat)
    
    # Buat graf baru dan relabel simpulnya
    G = nx.Graph()
    simpul_asli = list(derajat_simpul.keys())
    mapping = {i: simpul_asli[i] for i in range(len(simpul_asli))}
    
    # Salin sisi dengan label baru
    for u, v in G_temp.edges():
        G.add_edge(mapping[u], mapping[v])
        
    # Tambahkan simpul yang mungkin tidak punya sisi (derajat 0)
    G.add_nodes_from(simpul_asli)

    print("\nGraf Sederhana berhasil dibuat menggunakan algoritma Havel-Hakimi.")
    return G


def tampilkan_info_graf(G: Optional[nx.Graph]):
    """
    Menampilkan visualisasi graf, matriks ketetanggaan, dan derajat simpul.
    """
    if G is None:
        print("Tidak ada graf untuk ditampilkan.")
        return

    # --- 1. Visualisasi Graf ---
    print("\n" + "="*40)
    print("1. Visualisasi Graf")
    print("="*40)
    pos = nx.spring_layout(G, seed=42, k=1.5/np.sqrt(G.number_of_nodes()))
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000,
              font_size=14, font_weight='bold', edge_color='black', width=2.0)
    plt.title("Visualisasi Graf Sederhana (Havel-Hakimi)", size=18)
    plt.show()

    # --- 2. Matriks Ketetanggaan ---
    print("\n" + "="*40)
    print("2. Matriks Ketetanggaan (Adjacency Matrix)")
    print("="*40)
    simpul_terurut = sorted(G.nodes())
    matriks = nx.to_numpy_array(G, nodelist=simpul_terurut)
    print(f"Simpul diurutkan sebagai: {simpul_terurut}")
    print(matriks)
    print("\nCatatan: Untuk Graf Sederhana, nilai matriks adalah 1 jika ada sisi, 0 jika tidak.")

    # --- 3. Derajat Aktual Simpul ---
    print("\n" + "="*40)
    print("3. Derajat Aktual Setiap Simpul (Hasil Akhir)")
    print("="*40)
    derajat_aktual = dict(G.degree())
    for simpul, nilai_derajat in sorted(derajat_aktual.items()):
        print(f"  - Derajat simpul {simpul}: {nilai_derajat}")

def main():
    """Fungsi utama untuk menjalankan program."""
    print("--- Program Pembuat Graf Sederhana (Havel-Hakimi) ---")
    
    jumlah_simpul = dapatkan_input_angka("Masukkan jumlah total simpul (nodes): ")
    if jumlah_simpul == 0:
        print("Tidak ada simpul yang dibuat. Program selesai.")
        return

    simpul_list = range(1, jumlah_simpul + 1)
    print(f"Simpul akan diberi label dari 1 hingga {jumlah_simpul}.")
    print("-" * 30)

    derajat_input: Dict[int, int] = {}
    for simpul in simpul_list:
        derajat_input[simpul] = dapatkan_input_angka(f"Masukkan derajat untuk simpul {simpul}: ")
    
    # Prasyarat dasar: jumlah semua derajat harus genap
    if sum(derajat_input.values()) % 2 != 0:
        print("\n[!] GAGAL: Total semua derajat harus genap. Program dihentikan.")
        return
        
    # Buat dan tampilkan graf menggunakan Havel-Hakimi
    graf_hasil = buat_graf_sederhana_havel_hakimi(derajat_input)
    
    # Hanya tampilkan info jika graf berhasil dibuat
    if graf_hasil:
        tampilkan_info_graf(graf_hasil)

if __name__ == "__main__":
    main()