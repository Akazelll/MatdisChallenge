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

    total_deg = sum(derajat.values())
    if total_deg % 2 != 0:
        print("Jumlah total derajat harus genap.")
        return

    G = nx.MultiGraph()
    G.add_nodes_from(simpul)
    sisa_derajat = derajat.copy()
    loop_digunakan = set()

    # 1. Tambahkan setidaknya 1 loop
    loop_candidates = [v for v in simpul if sisa_derajat[v] >= 2]
    if loop_candidates:
        node = random.choice(loop_candidates)
        G.add_edge(node, node)
        sisa_derajat[node] -= 2
        loop_digunakan.add(node)
    else:
        print("❌ Tidak ada simpul dengan derajat ≥ 2 untuk loop.")
        return

    # 2. Tambahkan setidaknya 1 sisi ganda antar simpul berbeda
    ganda_candidates = [
        (u, v)
        for i, u in enumerate(simpul)
        for v in simpul[i+1:]
        if sisa_derajat[u] >= 2 and sisa_derajat[v] >= 2
    ]
    if ganda_candidates:
        u, v = random.choice(ganda_candidates)
        G.add_edge(u, v)
        G.add_edge(u, v)
        sisa_derajat[u] -= 2
        sisa_derajat[v] -= 2
    else:
        print("❌ Tidak ada pasangan simpul dengan derajat ≥ 2 untuk sisi ganda.")
        return

    # 3. Bangun daftar stub untuk sisa derajat
    stubs = []
    for node, deg in sisa_derajat.items():
        stubs.extend([node] * deg)
    random.shuffle(stubs)

    # 4. Pasangkan stubs
    while len(stubs) >= 2:
        u = stubs.pop()
        v = stubs.pop()
        # Jika ingin menghindari loop tambahan, batasi di sini:
        if u == v and u in loop_digunakan:
            # Cari pasangan lain yang bukan loop
            found = False
            for i in range(len(stubs)):
                if stubs[i] != u:
                    v_alt = stubs.pop(i)
                    G.add_edge(u, v_alt)
                    found = True
                    break
            if not found:
                G.add_edge(u, v)
        else:
            G.add_edge(u, v)
            if u == v:
                loop_digunakan.add(u)

    # 5. Verifikasi akhir
    print("\n--- Verifikasi Derajat ---")
    valid = True
    for node in simpul:
        d_expected = derajat[node]
        d_actual = G.degree(node)
        print(f"Simpul {node}: Derajat input = {d_expected}, Derajat aktual = {d_actual}")
        if d_actual != d_expected:
            valid = False
    if not valid:
        print("❌ Derajat tidak sesuai.")
        return

    # 6. Matriks ketetanggaan
    print("\n--- Matriks Ketetanggaan (jumlah sisi antar simpul) ---")
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
    nx.draw_networkx_nodes(G, pos, node_color='lightgreen', node_size=2000)
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    label_derajat = {n: f"d={G.degree(n)}" for n in G.nodes()}
    pos_label = {k: (v[0], v[1] - 0.1) for k, v in pos.items()}
    nx.draw_networkx_labels(G, pos_label, labels=label_derajat, font_size=10, font_color='darkred')

    plt.title("Graf Tak Sederhana (Wajib Loop & Sisi Ganda)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    buat_multigraf_terstandar()
