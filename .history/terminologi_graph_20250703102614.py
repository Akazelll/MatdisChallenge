import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def buat_graf_valid():
    n = int(input("Masukkan jumlah simpul: "))
    simpul = [str(i) for i in range(1, n + 1)]
    deg_input = {}

    for s in simpul:
        deg_input[s] = int(input(f"Derajat simpul {s}: "))

    if sum(deg_input.values()) % 2 != 0:
        print("❌ Jumlah total derajat harus genap.")
        return

    G = nx.MultiGraph()
    G.add_nodes_from(simpul)
    derajat_tersisa = deg_input.copy()
    loop_terpakai = set()

    # 1. Paksa 1 loop (simpul dengan derajat ≥ 2)
    kandidat_loop = [v for v in simpul if derajat_tersisa[v] >= 2]
    if not kandidat_loop:
        print("❌ Tidak ada simpul cukup derajat untuk loop.")
        return
    loop_node = random.choice(kandidat_loop)
    G.add_edge(loop_node, loop_node)
    derajat_tersisa[loop_node] -= 2
    loop_terpakai.add(loop_node)

    # 2. Paksa 1 sisi ganda antar dua simpul
    kandidat_ganda = [
        (u, v) for u in simpul for v in simpul
        if u != v and derajat_tersisa[u] >= 2 and derajat_tersisa[v] >= 2
    ]
    if not kandidat_ganda:
        print("❌ Tidak ada pasangan simpul cukup derajat untuk sisi ganda.")
        return
    u, v = random.choice(kandidat_ganda)
    G.add_edge(u, v)
    G.add_edge(u, v)
    derajat_tersisa[u] -= 2
    derajat_tersisa[v] -= 2

    # 3. Tambahkan sisi lain sesuai sisa derajat
    while True:
        # Ambil simpul-simpul dengan derajat tersisa ≥ 1
        calon = [s for s in simpul if derajat_tersisa[s] > 0]
        if len(calon) < 2:
            break  # selesai atau hanya satu simpul tersisa

        a, b = random.sample(calon, 2)
        G.add_edge(a, b)
        derajat_tersisa[a] -= 1
        derajat_tersisa[b] -= 1

    # 4. Tangani sisa deg 2 → bisa jadi loop
    for node in simpul:
        while derajat_tersisa[node] >= 2 and node not in loop_terpakai:
            G.add_edge(node, node)
            derajat_tersisa[node] -= 2
            loop_terpakai.add(node)

    # 5. Verifikasi derajat
    print("\n--- Verifikasi Derajat ---")
    valid = True
    for s in simpul:
        actual = G.degree(s)
        expected = deg_input[s]
        print(f"Simpul {s}: Input = {expected}, Aktual = {actual}")
        if actual != expected:
            valid = False
    if not valid:
        print("❌ Derajat tidak sesuai.")
        return

    # 6. Matriks Ketetanggaan
    print("\n--- Matriks Ketetanggaan ---")
    idx = {node: i for i, node in enumerate(simpul)}
    A = np.zeros((n, n), dtype=int)
    for u, v in G.edges():
        i, j = idx[u], idx[v]
        A[i][j] += 1
        if i != j:
            A[j][i] += 1
    print(A)

    # 7. Visualisasi
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=2000)
    nx.draw_networkx_edges(G, pos, width=2.5)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    label = {n: f"d={G.degree(n)}" for n in G.nodes()}
    pos_label = {k: (v[0], v[1] - 0.1) for k, v in pos.items()}
    nx.draw_networkx_labels(G, pos_label, labels=label, font_size=10, font_color='darkred')

    plt.title("Graf MultiGraph (Valid: Loop + Sisi Ganda)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    buat_graf_valid()
