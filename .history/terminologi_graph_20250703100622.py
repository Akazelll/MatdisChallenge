import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def buat_multigraf_wajib_loop_dan_sisi_ganda():
    """
    Membuat MultiGraph yang PASTI mengandung:
    - Sisi ganda
    - Loop
    Serta memastikan derajat tiap simpul sesuai input.
    """

    # --- 1. Input User ---
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
    if total_derajat % 2 != 0:
        print("\n❌ Jumlah total derajat ganjil. Graf tidak mungkin dibuat.")
        return

    print("\n📌 MultiGraph akan dibuat DENGAN loop & sisi ganda secara eksplisit.")

    # --- 2. Inisialisasi Graf ---
    G = nx.MultiGraph()
    G.add_nodes_from(simpul)

    # --- 3. Paksa satu loop ---
    loop_node = random.choice(simpul)
    G.add_edge(loop_node, loop_node)  # loop = kontribusi derajat +2
    derajat_awal[loop_node] -= 2

    # --- 4. Paksa satu sisi ganda (dua edge antara dua simpul berbeda) ---
    candidates = [node for node in simpul if derajat_awal[node] >= 1]
    u, v = random.sample(candidates, 2)
    G.add_edge(u, v)
    G.add_edge(u, v)  # sisi ganda
    derajat_awal[u] -= 2
    derajat_awal[v] -= 2

    # --- 5. Buat daftar stub dari sisa derajat ---
    stubs = []
    for node, deg in derajat_awal.items():
        if deg < 0:
            print(f"❌ Derajat tidak bisa negatif (terjadi pada simpul {node}) — kombinasi tidak valid.")
            return
        stubs.extend([node] * deg)

    random.shuffle(stubs)

    # --- 6. Tambahkan edge dari sisa stub (boleh loop & sisi ganda) ---
    while len(stubs) >= 2:
        a = stubs.pop()
        b = stubs.pop()
        G.add_edge(a, b)

    print("✅ Graf berhasil dibuat DENGAN loop dan sisi ganda secara eksplisit.")

    # --- 7. Verifikasi Derajat ---
    print("\n--- Verifikasi Derajat ---")
    sukses = True
    for node in simpul:
        actual = G.degree(node)
        expected = sum(1 for n in G[node] for _ in G[node][n].values())
        status = "✅" if actual == derajat_awal[node] + (2 if node == loop_node else 0) + (2 if node in [u, v] else 0) else "❌"
        print(f"{status} Simpul {node}: Derajat Input = {actual}, Derajat Aktual = {G.degree(node)}")
        if status == "❌":
            sukses = False

    # --- 8. Matriks Ketetanggaan ---
    print("\n--- Matriks Ketetanggaan (Jumlah sisi antar simpul) ---")
    idx = {node: i for i, node in enumerate(simpul)}
    matriks = np.zeros((jumlah_simpul, jumlah_simpul), dtype=int)

    for u, v in G.edges():
        i, j = idx[u], idx[v]
        matriks[i][j] += 1
        if i != j:
            matriks[j][i] += 1

    print(matriks)

    # --- 9. Visualisasi ---
    print("\n🎨 Menampilkan Visualisasi Graf...")
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 9))

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000)
    nx.draw_networkx_edges(G, pos, width=2.5)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    derajat_labels = {n: f"d={G.degree(n)}" for n in G.nodes()}
    pos_label = {k: (v[0], v[1] - 0.15) for k, v in pos.items()}
    nx.draw_networkx_labels(G, pos_label, labels=derajat_labels, font_size=10, font_color='darkred')

    plt.title("Graf MultiGraph (WAJIB: Loop & Sisi Ganda Digunakan)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    buat_multigraf_wajib_loop_dan_sisi_ganda()
