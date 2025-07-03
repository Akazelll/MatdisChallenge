import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

def buat_graf_dari_derajat():
    """
    Membuat graf dari barisan derajat input pengguna.
    Mendukung sisi ganda (MultiGraph), dan memberikan validasi
    apakah barisan derajat valid untuk graf sederhana.
    """

    # --- 1. Input Pengguna ---
    try:
        jumlah_simpul = int(input("Masukkan jumlah simpul: "))
        simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        
        derajat_awal = {}
        print("\n--- Input Derajat untuk Masing-masing Simpul ---")
        for s in simpul:
            derajat_awal[s] = int(input(f"Derajat simpul {s}: "))
    except ValueError:
        print("❌ Input tidak valid. Harap masukkan angka.")
        return

    derajat_list = list(derajat_awal.values())

    # --- 2. Validasi Barisan Derajat ---
    if sum(derajat_list) % 2 != 0:
        print("\n❌ Total derajat ganjil. Graf tidak mungkin dibentuk.")
        return

    if not nx.is_valid_degree_sequence_erdos_gallai(derajat_list):
        print("\n⚠️ Barisan derajat tidak valid untuk graf sederhana.")
        print("   Akan dibuat MultiGraph (dengan kemungkinan sisi ganda atau loop).")

    # --- 3. Pembuatan MultiGraph ---
    print("\n🔧 Membuat MultiGraph (dengan kemungkinan sisi ganda)...")
    graf = nx.MultiGraph()
    graf.add_nodes_from(simpul)

    # Membuat daftar stubs sesuai derajat
    stubs = [node for node, deg in derajat_awal.items() for _ in range(deg)]
    random.shuffle(stubs)

    while len(stubs) >= 2:
        u = stubs.pop()
        v = stubs.pop()
        graf.add_edge(u, v)

    print("✅ Graf berhasil dibuat.")

    # --- 4. Verifikasi Derajat dan Matriks ---
    print("\n--- Derajat Akhir Tiap Simpul ---")
    for node in simpul:
        print(f"Simpul {node}: Derajat Input = {derajat_awal[node]}, Derajat Aktual = {graf.degree(node)}")

    print("\n--- Matriks Ketetanggaan ---")
    matriks = nx.to_numpy_array(graf, nodelist=simpul)
    print(matriks)

    # --- 5. Visualisasi Graf ---
    print("\n🎨 Menampilkan Visualisasi Graf...")
    pos = nx.spring_layout(graf, seed=42)
    plt.figure(figsize=(12, 9))
    
    nx.draw_networkx_nodes(graf, pos, node_color='lightblue', node_size=2000)
    nx.draw_networkx_edges(graf, pos, width=2, alpha=0.7)
    nx.draw_networkx_labels(graf, pos, font_size=12, font_weight='bold')
    
    # Tampilkan derajat di bawah node
    derajat_labels = {node: f"d={deg}" for node, deg in graf.degree()}
    pos_derajat = {k: (v[0], v[1] - 0.15) for k, v in pos.items()}
    nx.draw_networkx_labels(graf, pos_derajat, labels=derajat_labels, font_size=10, font_color='darkred')

    plt.title("Visualisasi Graf (MultiGraph dengan Derajat Sesuai)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Jalankan fungsi utama
if __name__ == "__main__":
    buat_graf_dari_derajat()
