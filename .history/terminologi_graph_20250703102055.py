import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def buat_multigraf_terstandar():
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

    if sum(derajat.values()) % 2 != 0:
        print("Jumlah total derajat harus genap.")
        return

    G = nx.MultiGraph()
    G.add_nodes_from(simpul)
    sisa = derajat.copy()
    loop_digunakan = set()

    # Paksa 1 loop (maks 1 per simpul)
    loop_kandidat = [v for v in simpul if sisa[v] >= 2]
    if not loop_kandidat:
        print("❌ Tidak ada simpul cukup derajat untuk loop.")
        return
    node_loop = random.choice(loop_kandidat)
    G.add_edge(node_loop, node_loop)
    sisa[node_loop] -= 2
    loop_digunakan.add(node_loop)

    # Paksa 1 sisi ganda
    ganda_kandidat = [
        (u, v) for i, u in enumerate(simpul)
        for v in simpul[i+1:] if sisa[u] >= 2 and sisa[v] >= 2
    ]
    if not ganda_kandidat:
        print("❌ Tidak ada cukup pasangan simpul untuk sisi ganda.")
        return
    u, v = random.choice(ganda_kandidat)
    G.add_edge(u, v)
    G.add_edge(u, v)
    sisa[u] -= 2
    sisa[v] -= 2

    # Bangun stub SESUDAH pemotongan dari loop & sisi ganda
    stubs = []
    for node, deg in sisa.items():
        stubs.extend([node] * deg)
    random.shuffle(stubs)

    # Pairing sisa stub
    while len(stubs) >= 2:
        a, b = stubs.pop(), stubs.pop()
        if a == b and a in loop_digunakan:
            # Hindari loop kedua
            found = False
            for i in range(len(stubs)):
                if stubs[i] != a:
                    b = stubs.pop(i)
                    G.add_edge(a, b)
                    found = True
                    break
            if not found:
                G.add_edge(a, b)
        else:
            G.add_edge(a, b)
            if a == b:
                loop_digunakan.add(a)

    # Verifikasi derajat
    print("\n--- Verifikasi Derajat ---")
    valid = True
    for node in simpul:
        expected = derajat[node]
        actual = G.degree(node)
        print(f"Simpul {node}: Derajat input = {expected}, Derajat aktual = {actual}")
        if expected != actual:
            valid = False
    if not valid:
        print("❌ Derajat tidak sesuai.")
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

    label_deg = {n: f"d={G.degree(n)}" for n in G.nodes()}
    label_pos = {k: (v[0], v[1] - 0.1) for k, v in pos.items()}
    nx.draw_networkx_labels(G, label_pos, labels=label_deg, font_size=10, font_color='darkred')

    plt.title("Graf MultiGraph dengan Loop dan Sisi Ganda (Final Fix)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    buat_multigraf_terstandar()
