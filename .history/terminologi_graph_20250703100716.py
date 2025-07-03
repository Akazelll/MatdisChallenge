import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def buat_multigraf_wajib_sisi_ganda_dan_loop():
    """
    Membuat MultiGraph dari input derajat dengan memaksa penggunaan
    sisi ganda dan loop agar derajat terpenuhi secara tepat.
    Matriks ketetanggaan menampilkan jumlah sisi antar simpul.
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

    total_derajat = sum(derajat_awal.values())

    # --- 2. Validasi Jumlah Derajat Genap ---
    if total_derajat % 2 != 0:
        print("\n❌ Total derajat ganjil. Tidak mungkin membuat graf.")
        return

    print("\nℹ️ MultiGraph AKAN menggunakan sisi ganda dan loop untuk memenuhi derajat.")
    print("   Matriks akan merepresentasikan jumlah sisi antar simpul, termasuk loop.")

    # --- 3. Inisialisasi MultiGraph ---
    G = nx.MultiGraph()
    G.add_nodes_from(simpul)

    # Daftar stubs (ujung sisi)
    stubs = [node for node, deg in derajat_awal.items() for _ in range(deg)]
    random.shuffle(stubs)

    # --- 4. Pasangkan Stubs (WAJIB pakai loop & sisi ganda) ---
    while len(stubs) >= 2:
        u = stubs.pop()
        v = stubs.pop()

        # Tambahkan edge langsung, meskipun u == v (loop), atau sudah terhubung (sisi ganda)
        G.add_edge(u, v)

    print("✅ Graf berhasil dibuat menggunakan sisi ganda dan loop.")

    # --- 5. Verifikasi Derajat ---
    print("\n--- Verifikasi Derajat ---")
    semua_sesuai = True
    for node in simpul:
        aktual = G.degree(node)
        target = derajat_awal[node]
        status = "✅" if aktual == target else "❌"
        print(f"{status} Simpul {node}: Derajat Input = {target}, Derajat Aktual = {aktual}")
        if aktual != target:
            semua_sesuai = False

    if not semua_sesuai:
        print("\n⚠️ Perhatian: Terjadi ketidaksesuaian derajat. Coba ulang atau gunakan seed tetap.")

    # --- 6. Matriks Ketetanggaan ---
    print("\n--- Matriks Ketetanggaan (jumlah sisi antar simpul) ---")
    matriks = np.zeros((jumlah_simpul, jumlah_simpul), dtype=int)
    indeks = {simpul[i]: i for i in range(jumlah_simpul)}

    for u, v in G.edges():
        i = indeks[u]
        j = indeks[v]
        matriks[i][j] += 1
        if i != j:
            matriks[j][i] += 1

    print(matriks)

    # --- 7. Visualisasi ---
    print("\n🎨 Menampilkan Visualisasi Graf...")
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 9))

    nx.draw_networkx_nodes(G, pos, node_color='lightcoral', node_size=2000)
    nx.draw_networkx_edges(G, pos, width=2.5, alpha=0.85)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    # Label derajat
    label_derajat = {n: f"d={G.degree(n)}" for n in G.nodes()}
    pos_label = {k: (v[0], v[1] - 0.15) for k, v in pos.items()}
    nx.draw_networkx_labels(G, pos_label, labels=label_derajat, font_size=10, font_color='darkred')

    plt.title("Graf MultiGraph (WAJIB Gunakan Sisi Ganda & Loop)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Jalankan
if __name__ == "__main__":
    buat_multigraf_wajib_sisi_ganda_dan_loop()
