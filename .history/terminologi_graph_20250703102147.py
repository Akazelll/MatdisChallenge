import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def buat_graf_dengan_loop_dan_sisi_ganda():
    n = int(input("Masukkan jumlah simpul: "))
    simpul = [str(i) for i in range(1, n + 1)]
    derajat = {}
    for s in simpul:
        derajat[s] = int(input(f"Derajat simpul {s}: "))

    if sum(derajat.values()) % 2 != 0:
        print("❌ Jumlah total derajat harus genap.")
        return

    G = nx.MultiGraph()
    G.add_nodes_from(simpul)

    sisa = derajat.copy()
    loop_terpasang = set()

    # 1. Tambahkan loop ke satu simpul
    loop_kandidat = [v for v in simpul if sisa[v] >= 2]
    if not loop_kandidat:
        print("❌ Tidak ada simpul yang bisa diberi loop.")
        return
    loop_node = random.choice(loop_kandidat)
    G.add_edge(loop_node, loop_node)
    sisa[loop_node] -= 2
    loop_terpasang.add(loop_node)

    # 2. Tambahkan sisi ganda ke dua simpul berbeda
    ganda_kandidat = [
        (u, v) for i, u in enumerate(simpul)
        for v in simpul[i+1:] if sisa[u] >= 2 and sisa[v] >= 2
    ]
    if not ganda_kandidat:
        print("❌ Tidak cukup simpul untuk sisi ganda.")
        return
    u, v = random.choice(ganda_kandidat)
    G.add_edge(u, v)
    G.add_edge(u, v)
    sisa[u] -= 2
    sisa[v] -= 2

    # 3. Buat stubs dari sisa derajat
    stubs = []
    for node in simpul:
        stubs.extend([node] * sisa[node])
    random.shuffle(stubs)

    # 4. Pasangkan stubs dua-dua
    while len(stubs) >= 2:
        a = stubs.pop()
        b = stubs.pop()

        if a == b and a in loop_terpasang:
            # Hindari loop kedua pada simpul yang sama
            found = False
            for i in range(len(stubs)):
                if stubs[i] != a:
                    b_alt = stubs.pop(i)
                    G.add_edge(a, b_alt)
                    found = True
                    break
            if not found:
                G.add_edge(a, b)
        else:
            if a == b:
                loop_terpasang.add(a)
            G.add_edge(a, b)

    # 5. Verifikasi Derajat
    print("\n--- Verifikasi Derajat ---")
    valid = True
    for node in simpul:
        target = derajat[node]
        actual = G.degree(node)
        print(f"Simpul {node}: Derajat input = {target}, Derajat aktual = {actual}")
        if actual != target:
            valid = False
    if not valid:
        print("❌ Derajat tidak sesuai.")
        return

    # 6. Matriks Ketetanggaan
    print("\n--- Matriks Ketetanggaan ---")
    idx = {node: i for i, node in enumerate(simpul)}
    A = np.zeros((n, n), dtype=int)
    for a, b in G.edges():
        i, j = idx[a], idx[b]
        A[i][j] += 1
        if i != j:
            A[j][i] += 1
    print(A)

    # 7. Visualisasi
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000)
    nx.draw_networkx_edges(G, pos, width=2.5)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    label_deg = {n: f"d={G.degree(n)}" for n in G.nodes()}
    label_pos = {k: (v[0], v[1] - 0.1) for k, v in pos.items()}
    nx.draw_networkx_labels(G, label_pos, labels=label_deg, font_size=10, font_color='darkred')

    plt.title("Graf MultiGraph (1 loop + 1 sisi ganda minimal)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    buat_graf_dengan_loop_dan_sisi_ganda()
