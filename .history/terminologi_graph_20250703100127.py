import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

def buat_graf_dengan_sisi_ganda_dan_loop():
    """
    Membuat MultiGraph dari barisan derajat.
    Mengizinkan sisi ganda dan loop agar semua derajat dapat terpenuhi.
    """

    # --- 1. Input Pengguna ---
    try:
        jumlah_simpul = int(input("Masukkan jumlah simpul: "))
        simpul = [str(i) for i in range(1, jumlah_simpul + 1)]

        derajat_awal = {}
        print("\n--- Input Derajat untuk Setiap Simpul ---")
        for s in simpul:
            derajat_awal[s] = int(input(f"Derajat simpul {s}: "))
    except ValueError:
        print("❌ Input tidak valid. Harap masukkan angka.")
        return

    derajat_list = list(derajat_awal.values())

    # --- 2. Validasi Jumlah Derajat Genap ---
    if sum(derajat_list) % 2 != 0:
        print("\n❌ Total derajat ganjil. Tidak mungkin membuat graf.")
        return

    print("\nℹ️ Akan dibuat graf MultiGraph dengan sisi ganda dan loop jika diperlukan.")
    print("✅ Derajat akan dipenuhi dengan membentuk sisi ganda dan/atau loop.")

    # --- 3. Buat MultiGraph ---
    G = nx.MultiGraph()
    G.add_nodes_from(simpul)

    # Buat daftar stubs sesuai derajat
    stubs = [node for node, deg in derajat_awal.items() for _ in range(deg)]
    random.shuffle(stubs)

    # Pasangkan stubs dua-dua (izinkan loop dan sisi ganda)
    while len(stubs) >= 2:
        u = stubs.pop()
        v = stubs.pop()
        G.add_edge(u, v)  # bisa u == v (loop)

    print("✅ Graf berhasil dibuat.")

    # --- 4. Verifikasi Derajat ---
    print("\n--- Verifikasi Derajat Akhir ---")
    for node in simpul:
        print(f"Simpul {node}: Derajat Input = {derajat_awal[node]}, Derajat Aktual = {G.degree(node)}")

    # --- 5. Matriks Ketetanggaan ---
    print("\n--- Matriks Ketetanggaan (MultiGraph) ---")
    matriks = nx.to_numpy_array(G, nodelist=simpul)
    print(matriks)

    # --- 6. Visualisasi ---
    print("\n🎨 Menampilkan Visualisasi Graf...")
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 9))

    nx.draw_networkx_nodes(G, pos, node_color='lightyellow', node_size=2000)
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.7)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    # Label derajat
    derajat_labels = {node: f"d={deg}" for node, deg in G.degree()}
    pos_label = {k: (v[0], v[1] - 0.15) for k, v in pos.items()}
    nx.draw_networkx_labels(G, pos_label, labels=derajat_labels, font_size=10, font_color='darkgreen')

    plt.title("Graf MultiGraph dengan Sisi Ganda dan Loop (Derajat Sesuai)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Jalankan
if __name__ == "__main__":
    buat_graf_dengan_sisi_ganda_dan_loop()
