import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def buat_multigraf_dengan_loop_dan_sisi_ganda():
    try:
        n = int(input("Masukkan jumlah simpul: "))
        simpul = [str(i) for i in range(1, n + 1)]

        derajat = {}
        for s in simpul:
            d = int(input(f"Derajat simpul {s}: "))
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

    # Paksa satu loop (kontribusi +2)
    loop_candidates = [node for node in simpul if derajat[node] >= 2]
    if not loop_candidates:
        print("Tidak ada simpul dengan derajat >= 2 untuk loop.")
        return
    loop_node = random.choice(loop_candidates)
    G.add_edge(loop_node, loop_node)
    derajat[loop_node] -= 2

    # Paksa satu sisi ganda antar dua simpul berbeda
    ganda_candidates = [node for node in simpul if derajat[node] >= 2 and node != loop_node]
    found = False
    for i in range(len(ganda_candidates)):
        for j in range(i+1, len(ganda_candidates)):
            u = ganda_candidates[i]
            v = ganda_candidates[j]
            G.add_edge(u, v)
            G.add_edge(u, v)
            derajat[u] -= 2
            derajat[v] -= 2
            found = True
            break
        if found:
            break
    if not found:
        print("Tidak bisa membuat sisi ganda antar dua simpul berbeda.")
        return

    # Buat stub list
    stubs = [node for node, deg in derajat.items() for _ in range(deg)]
    random.shuffle(stubs)

    # Pasangkan stub
    while len(stubs) >= 2:
        u = stubs.pop()
        v = stubs.pop()
        G.add_edge(u, v)

    # Verifikasi derajat
    print("\n--- Verifikasi Derajat ---")
    for node in simpul:
        print(f"Simpul {node}: Derajat input = {derajat[node] + (2 if node == loop_node else 0) + (2 if node in [u, v] else 0)}, Derajat aktual = {G.degree(node)}")

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

    plt.title("Graf MultiGraph (WAJIB: Loop dan Sisi Ganda)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    buat_multigraf_dengan_loop_dan_sisi_ganda()
