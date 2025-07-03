import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import defaultdict

def buat_multigraf_dengan_loop_dan_sisi_ganda():
    try:
        n = int(input("Masukkan jumlah simpul: "))
        simpul = [str(i) for i in range(1, n + 1)]

        derajat = {}
        for s in simpul:
            d = int(input(f"Derajat simpul {s}: "))
            if d < 0:
                print("Derajat tidak boleh negatif.")
                return
            derajat[s] = d

    except ValueError:
        print("Input tidak valid.")
        return

    total_deg = sum(derajat.values())
    if total_deg % 2 != 0:
        print("Jumlah total derajat harus genap.")
        return

    G = nx.MultiGraph()
    G.add_nodes_from(simpul)

    stubs = [node for node, deg in derajat.items() for _ in range(deg)]
    random.shuffle(stubs)

    pasangan_terpakai = defaultdict(int)
    loop_dibuat = False
    sisi_ganda_dibuat = False

    while len(stubs) >= 2:
        u = stubs.pop()
        v = stubs.pop()

        # Jika belum ada loop, dan u == v → jadikan loop
        if not loop_dibuat and u == v:
            loop_dibuat = True

        # Jika belum ada sisi ganda, dan (u, v) sudah pernah digunakan
        if not sisi_ganda_dibuat:
            key = tuple(sorted((u, v)))
            pasangan_terpakai[key] += 1
            if pasangan_terpakai[key] == 2:
                sisi_ganda_dibuat = True

        G.add_edge(u, v)

    # Jika belum ada loop, paksa loop secara manual
    if not loop_dibuat:
        kandidat_loop = [node for node in simpul if G.degree(node) + 2 <= derajat[node]]
        if not kandidat_loop:
            print("❌ Tidak bisa memaksa loop, tidak ada simpul yang sisa derajatnya ≥ 2.")
            return
        node = random.choice(kandidat_loop)
        G.add_edge(node, node)

    # Jika belum ada sisi ganda, paksa secara manual
    if not sisi_ganda_dibuat:
        kandidat = [
            (u, v) for u in simpul for v in simpul
            if u != v and G.degree(u) + 2 <= derajat[u] and G.degree(v) + 2 <= derajat[v]
        ]
        if not kandidat:
            print("❌ Tidak bisa memaksa sisi ganda, tidak ada pasangan simpul dengan sisa derajat cukup.")
            return
        u, v = random.choice(kandidat)
        G.add_edge(u, v)
        G.add_edge(u, v)

    # Verifikasi derajat akhir
    print("\n--- Verifikasi Derajat ---")
    for node in simpul:
        print(f"Simpul {node}: Derajat input = {derajat[node]}, Derajat aktual = {G.degree(node)}")
        if G.degree(node) != derajat[node]:
            print("❌ Derajat tidak sesuai. Gagal.")
            return

    # Matriks ketetanggaan
    print("\n--- Matriks Ketetanggaan ---")
    idx = {node: i for i, node in enumerate(simpul)}
    A = np.zeros((n, n), dtype=int)
    for a, b in G.edges():
        i, j = idx[a], idx[b]
        A[i][j] += 1
        if i != j:
            A[j][i] += 1
    print(A)

    # Visualisasi
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000)
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    label_derajat = {n: f"d={G.degree(n)}" for n in G.nodes()}
    label_pos = {k: (v[0], v[1] - 0.1) for k, v in pos.items()}
    nx.draw_networkx_labels(G, label_pos, labels=label_derajat, font_size=10, font_color='darkred')

    plt.title("Graf MultiGraph dengan Loop dan Sisi Ganda (Wajib)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    buat_multigraf_dengan_loop_dan_sisi_ganda()
