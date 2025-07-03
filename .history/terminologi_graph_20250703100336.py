import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

def buat_multigraf_dengan_ketetanggaan_eksak():
    """
    Membuat graf MultiGraph dengan loop dan sisi ganda sehingga
    derajat setiap simpul sesuai input, dan matriks ketetanggaan
    mencerminkan hubungan aktual (jumlah sisi antara simpul).
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

    print("\nℹ️ MultiGraph dengan sisi ganda dan loop akan dibuat.")
    print("✅ Derajat akan dipenuhi, dan ketetanggaan merepresentasikan jumlah sisi.")

    # --- 3. Inisialisasi Graf ---
    G = nx.MultiGraph()
    G.add_nodes_from(simpul)

    # Daftar stubs (ujung sisi)
    stubs = [node for node, deg in derajat_awal.items() for _ in range(deg)]
    random.shuffle(stubs)

    # --- 4. Bangun Edge dari Pasangan Stubs ---
    while len(stubs) >= 2:
        u = stubs.pop()
        v = stubs.pop()
        G.add_edge(u, v)  # izinkan loop dan sisi ganda

    print("✅ Graf berhasil dibuat.")

    # --- 5. Verifikasi Derajat Akhir ---
    print("\n--- Verifikasi Derajat ---")
    sukses = True
    for node in simpul:
        derajat = G.degree(node)
        if derajat != derajat_awal[node]:
            print(f"❌ Simpul {node}: Derajat Input = {derajat_awal[node]}, Derajat Aktual = {derajat} ❌")
            sukses = False
        else:
            print(f"✅ Simpul {node}: Derajat = {derajat}")

    if not sukses:
        print("\n⚠️ Terdapat simpul dengan derajat tidak sesuai. Proses pairing stubs bisa dipengaruhi oleh acakan.")
        print("   Jalankan ulang atau gunakan strategi pairing deterministik.")

    # --- 6. Matriks Ketetanggaan (jumlah sisi antar simpul) ---
    print("\n--- Matriks Ketetanggaan (jumlah sisi antar simpul) ---")
    matriks = np.zeros((jumlah_simpul, jumlah_simpul), dtype=int)
    indeks = {simpul[i]: i for i in range(jumlah_simpul)}

    for u, v in G.edges():
        i = indeks[u]
        j = indeks[v]
        matriks[i][j] += 1
        if i != j:
            matriks[j][i] += 1  # untuk loop, hanya sekali ditambahkan

    print(matriks)

    # --- 7. Visualisasi Graf ---
    print("\n🎨 Menampilkan Visualisasi Graf...")
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 9))

    nx.draw_networkx_nodes(G, pos, node_color='lightcyan', node_size=2000)
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.8)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    # Tampilkan label derajat
    label_derajat = {n: f"d={G.degree(n)}" for n in G.nodes()}
    pos_label = {k: (v[0], v[1] - 0.15) for k, v in pos.items()}
    nx.draw_networkx_labels(G, pos_label, labels=label_derajat, font_size=10, font_color='darkgreen')

    plt.title("Graf MultiGraph (Loop dan Sisi Ganda Diizinkan)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Jalankan
if __name__ == "__main__":
    buat_multigraf_dengan_ketetanggaan_eksak()
