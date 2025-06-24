import networkx as nx
import matplotlib.pyplot as plt
import random

def buat_graf_acak(jumlah_simpul, prob_sisi, prob_loop):
    """
    Membuat sebuah graf acak (tak berarah) dengan kemungkinan adanya
    sisi ganda dan loop.

    Args:
        jumlah_simpul (int): Jumlah simpul (node) dalam graf.
        prob_sisi (float): Probabilitas (antara 0.0 dan 1.0) untuk membuat sisi antara sepasang simpul.
        prob_loop (float): Probabilitas (antara 0.0 dan 1.0) untuk sebuah simpul memiliki loop.

    Returns:
        networkx.MultiGraph: Objek graf yang telah dibuat.
    """
    # Menggunakan MultiGraph untuk memperbolehkan adanya sisi ganda dan loop.
    # Sesuai dengan materi, ini adalah tipe "Graf tak-sederhana".
    G = nx.MultiGraph()

    # 1. Menambahkan Simpul (Nodes)
    # Simpul diberi nama dari 1 hingga jumlah_simpul
    simpul = range(1, jumlah_simpul + 1)
    G.add_nodes_from(simpul)

    # 2. Menambahkan Sisi Acak (Random Edges)
    # Iterasi melalui setiap kemungkinan pasangan simpul untuk membuat sisi.
    for i in range(1, jumlah_simpul + 1):
        for j in range(i + 1, jumlah_simpul + 1):
            # Membuat sisi berdasarkan probabilitas
            if random.random() < prob_sisi:
                G.add_edge(i, j)
                # Kemungkinan adanya sisi ganda (multiple edges)
                if random.random() < prob_sisi / 2: # Probabilitas sisi ganda dibuat lebih kecil
                    G.add_edge(i, j)

    # 3. Menambahkan Loop Acak (Random Self-loops)
    # Iterasi melalui setiap simpul untuk kemungkinan membuat loop.
    for node in G.nodes():
        if random.random() < prob_loop:
            G.add_edge(node, node) # Menambahkan sisi dari simpul ke dirinya sendiri

    return G

def gambar_graf(G):
    """
    Menggambar dan menampilkan objek graf menggunakan matplotlib.

    Args:
        G (networkx.Graph): Graf yang akan digambar.
    """
    # Menentukan posisi simpul agar tidak tumpang tindih
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(10, 8))

    # Menggambar simpul, sisi, dan label
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=12, font_weight='bold', edge_color='gray')

    # Menampilkan informasi derajat simpul
    derajat = dict(G.degree())
    print("Derajat setiap simpul:", derajat)

    # Menampilkan informasi graf
    plt.title("Visualisasi Graf Acak", size=16)
    print(f"Jumlah Simpul: {G.number_of_nodes()}")
    print(f"Jumlah Sisi (termasuk ganda & loop): {G.number_of_edges()}")
    
    plt.show()


# --- PENGATURAN UTAMA ---
if __name__ == "__main__":
    # Anda bisa mengubah parameter di bawah ini untuk menghasilkan graf yang berbeda
    
    # Jumlah simpul yang diinginkan
    JUMLAH_SIMPUL_ACAK = 8

    # Probabilitas adanya sisi antar simpul (0.0 - 1.0)
    # Semakin tinggi nilainya, semakin banyak sisi yang terbentuk.
    PROBABILITAS_SISI = 0.4

    # Probabilitas sebuah simpul memiliki loop (0.0 - 1.0)
    PROBABILITAS_LOOP = 0.25

    # 1. Membuat graf dengan ketentuan acak
    graf_hasil = buat_graf_acak(JUMLAH_SIMPUL_ACAK, PROBABILITAS_SISI, PROBABILITAS_LOOP)

    # 2. Menggambar graf yang sudah dibuat
    gambar_graf(graf_hasil)