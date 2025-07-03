import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def buat_graf_dengan_matriks_ketetanggaan():
    try:
        n = int(input("Masukkan jumlah simpul: "))
        simpul = [str(i) for i in range(1, n + 1)]
        derajat = {}

        for s in simpul:
            d = int(input(f"Derajat simpul {s}: "))
            derajat[s] = d

    except ValueError:
        print("Input harus berupa angka.")
        return

    if sum(derajat.values()) % 2 != 0:
        print("Total derajat ganjil. Graf tidak mungkin terbentuk.")
        return

    G = nx.MultiGraph()
    G.add_nodes_from(simpul)

    # Paksa 1 loop
    loop_node = next((k for k in simpul if derajat[k] >= 2), None)
    if not loop_node:
        print("Tidak ada simpul dengan derajat ≥ 2 untuk loop.")
        return
    G.add_edge(loop_node, loop_node)
    derajat[loop_node] -= 2

    # Paksa 1 sisi ganda antar dua simpul
    kandidat = [k for k in simpul if derajat[k] >= 2 and k != loop_node]
    if len(kandidat) < 2:
        print("Tidak cukup simpul untuk membentuk sisi ganda.")
        return
    u, v = random.sample(kandidat, 2)
    G.add_edge(u, v)
    G.add_edge(u, v)
    derajat[u] -= 2
    derajat[v] -= 2

    # Buat daftar stub
    stubs = []
    for k in simpul:
        if derajat[k] < 0:
            print(f"Derajat simpul {k} negatif setelah loop/sisi ganda → tidak valid.")
            return
        stubs.extend([k] * derajat[k])
    random.shuffle(stubs)

    # Pasangkan sisa stub
    while len(stubs) >= 2:
        a, b = stubs.pop(), stubs.pop()
        G.add_edge(a, b)

    print("\n--- Verifikasi Derajat ---")
    for k in simpul:
        print(f"Simpul {k}: Derajat = {G.degree(k)} (target: {derajat[k] + (2 if k == loop_node else 0) + (2 if k in [u, v] else 0)})")

    print("\n--- Matriks Ketetanggaan ---")
    idx = {node: i for i, node in enumerate(simpul)}
    A = np.zeros((n, n), dtype=int)

    for a, b in G.edges():
        i, j = idx[a], idx[b]
        A[i][j] += 1
        if i != j:
            A[j][i] += 1
    print(A)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=2000)
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    label_d = {node: f"d={G.degree(node)}" for node in G.nodes()}
    label_pos = {k: (v[0], v[1] - 0.1) for k, v in pos.items()}
    nx.draw_networkx_labels(G, label_pos, labels=label_d, font_size=10, font_color='darkblue')

    plt.title("Graf MultiGraph dengan Sisi Ganda & Loop + Matriks Ketetanggaan")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    buat_graf_dengan_matriks_ketetanggaan()
