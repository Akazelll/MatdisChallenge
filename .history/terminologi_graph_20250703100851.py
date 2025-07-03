import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def buat_multigraf_wajib_sisi_ganda_dan_loop():
    try:
        jumlah_simpul = int(input("Masukkan jumlah simpul: "))
        simpul = [str(i) for i in range(1, jumlah_simpul + 1)]

        derajat_awal = {}
        for s in simpul:
            derajat_awal[s] = int(input(f"Derajat simpul {s}: "))
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return

    total_derajat = sum(derajat_awal.values())
    if total_derajat % 2 != 0:
        print("Total derajat harus genap.")
        return

    G = nx.MultiGraph()
    G.add_nodes_from(simpul)

    stubs = [node for node, deg in derajat_awal.items() for _ in range(deg)]
    random.shuffle(stubs)

    loop_dibuat = False
    sisi_ganda_dibuat = False
    pasangan_terhubung = set()

    while len(stubs) >= 2:
        u, v = stubs.pop(), stubs.pop()

        if u == v and not loop_dibuat:
            G.add_edge(u, v)
            loop_dibuat = True
        elif (u, v) in pasangan_terhubung or (v, u) in pasangan_terhubung:
            G.add_edge(u, v)
            sisi_ganda_dibuat = True
        else:
            G.add_edge(u, v)
            pasangan_terhubung.add((u, v))

    if not loop_dibuat:
        node = random.choice(simpul)
        G.add_edge(node, node)

    if not sisi_ganda_dibuat:
        node1, node2 = random.sample(simpul, 2)
        G.add_edge(node1, node2)
        G.add_edge(node1, node2)

    print("\nVerifikasi Derajat:")
    for node in simpul:
        print(f"Simpul {node}: Derajat Input = {derajat_awal[node]}, Derajat Aktual = {G.degree(node)}")

    print("\nMatriks Ketetanggaan:")
    matriks = np.zeros((jumlah_simpul, jumlah_simpul), dtype=int)
    indeks = {simpul[i]: i for i in range(jumlah_simpul)}
    for u, v in G.edges():
        i, j = indeks[u], indeks[v]
        matriks[i][j] += 1
        if i != j:
            matriks[j][i] += 1
    print(matriks)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 9))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000)
    nx.draw_networkx_edges(G, pos, width=2.5)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    label_derajat = {n: f"d={G.degree(n)}" for n in G.nodes()}
    pos_label = {k: (v[0], v[1] - 0.15) for k, v in pos.items()}
    nx.draw_networkx_labels(G, pos_label, labels=label_derajat, font_size=10, font_color='darkred')

    plt.title("Graf MultiGraph (Sisi Ganda & Loop Wajib Digunakan)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    buat_multigraf_wajib_sisi_ganda_dan_loop()
