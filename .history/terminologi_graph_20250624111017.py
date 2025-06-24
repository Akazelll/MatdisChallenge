import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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

def dapatkan_matriks_ketetanggaan() -> np.ndarray:
    """
    Memandu pengguna untuk membuat matriks ketetanggaan (adjacency matrix).
    Matriks ini akan bersifat simetris.
    """
    print("-" * 40)
    print("Langkah 1: Membuat Matriks Ketetanggaan")
    print("-" * 40)
    
    n = get_input_angka("Masukkan jumlah simpul (ukuran matriks N x N): ")
    if n == 0:
        return np.array([])
        
    # Inisialisasi matriks dengan nol
    matriks = np.zeros((n, n), dtype=int)
    
    print("\nSilakan masukkan nilai untuk setiap elemen matriks.")
    print("Nilai merepresentasikan jumlah sisi antara dua simpul.")
    print("Contoh: nilai 2 antara simpul 1 dan 3 berarti ada 2 sisi yang menghubungkan mereka.")
    print("Nilai pada diagonal (misal: M[1,1]) merepresentasikan loop.")
    print("-" * 40)

    # Hanya meminta input untuk bagian atas matriks (termasuk diagonal)
    # karena matriks ketetanggaan untuk graf tidak berarah adalah simetris.
    for i in range(n):
        for j in range(i, n):
            # Untuk diagonal (loop)
            if i == j:
                prompt = f"Masukkan nilai untuk M[{i+1},{j+1}] (jumlah loop pada simpul {i+1}): "
                nilai = get_input_angka(prompt)
                matriks[i, j] = nilai
            # Untuk elemen lainnya
            else:
                prompt = f"Masukkan nilai untuk M[{i+1},{j+1}] (jumlah sisi antara simpul {i+1} dan {j+1}): "
                nilai = get_input_angka(prompt)
                matriks[i, j] = nilai
                matriks[j, i] = nilai # Otomatis mengisi elemen simetrisnya
                
    print("\nMatriks Ketetanggaan berhasil dibuat:")
    print(matriks)
    return matriks

def buat_dan_visualisasikan_graf(matriks: np.ndarray):
    """
    Membuat graf dari matriks ketetanggaan dan menampilkannya.
    """
    if matriks.size == 0:
        print("\nMatriks kosong, tidak ada graf yang dibuat.")
        return

    # Membuat graf dari matriks NumPy.
    # create_using=nx.MultiGraph() memungkinkan sisi ganda dan loop.
    G = nx.from_numpy_array(matriks, create_using=nx.MultiGraph())
    
    # Simpul dari from_numpy_array diberi label 0, 1, 2, ...
    # Kita perlu me-relabel menjadi 1, 2, 3, ... agar sesuai dengan input pengguna.
    n = matriks.shape[0]
    mapping_label = {i: i + 1 for i in range(n)}
    nx.relabel_nodes(G, mapping_label, copy=False)

    print("\n" + "-"*40)
    print("Langkah 2: Visualisasi Graf")
    print("-" * 40)

    # Visualisasi graf
    pos = nx.spring_layout(G, seed=42, k=1.5) # k untuk menambah jarak antar simpul
    plt.figure(figsize=(10, 8))
    
    nx.draw(
        G, 
        pos, 
        with_labels=True, 
        node_color='skyblue', 
        node_size=2000, 
        font_size=14, 
        font_weight='bold', 
        edge_color='gray', 
        width=1.5
    )
    plt.title("Visualisasi Graf dari Matriks Ketetanggaan", size=18)
    plt.show()

    # Tampilkan informasi tambahan
    print("\nInformasi Graf:")
    print(f"Total Simpul: {G.number_of_nodes()}")
    print(f"Total Sisi (termasuk ganda/loop): {G.number_of_edges()}")
    
    print("\nDerajat setiap simpul:")
    # Derajat dihitung dengan benar oleh NetworkX, loop dihitung sebagai 2.
    derajat = dict(G.degree())
    for simpul, nilai_derajat in derajat.items():
        print(f"  - Simpul {simpul}: {nilai_derajat}")


if __name__ == "__main__":
    print("--- Program Visualisasi Graf dari Matriks Ketetanggaan ---")
    matriks_input = dapatkan_matriks_ketetanggaan()
    buat_dan_visualisasikan_graf(matriks_input)
    print("\nProgram selesai.")