import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def get_input_angka(prompt):
    """Fungsi untuk memastikan input adalah angka integer positif."""
    while True:
        try:
            nilai = int(input(prompt))
            if nilai >= 0:
                return nilai
            else:
                print("Input tidak boleh negatif. Silakan coba lagi.")
        except ValueError:
            print("Input tidak valid. Harap masukkan sebuah angka.")


def buat_graf_otomatis():
    G = nx.MultiGraph()

    # Meminta jumlah simpul
    jumlah_simpul = get_input_angka("Masukkan jumlah total simpul (nodes) yang Anda inginkan: ")
    if jumlah_simpul == 0:
        print("Tidak ada simpul yang dibuat. Program selesai.")
        return None

    simpul_list = range(1, jumlah_simpul + 1)
    G.add_nodes_from(simpul_list)
    print(f"Berhasil membuat {jumlah_simpul} simpul, yaitu: {list(simpul_list)}")
    print("-" * 30)

    # Meminta derajat dari masing-masing simpul
    derajat = {}
    for simpul in simpul_list:
        derajat[simpul] = get_input_angka(f"Masukkan derajat untuk simpul {simpul}: ")

    # Validasi jumlah derajat (harus genap)
    if sum(derajat.values()) % 2 != 0:
        print("Total derajat tidak genap, graf tidak bisa dibuat. Program selesai.")
        return None

    # Membuat sisi berdasarkan derajat
    sisi_tersisa = {node: derajat[node] for node in simpul_list}
    while any(sisi_tersisa.values()):
        nodes = [node for node in simpul_list if sisi_tersisa[node] > 0]
        if len(nodes) > 1:
            u, v = np.random.choice(nodes, size=2, replace=False)
            G.add_edge(u, v)
            sisi_tersisa[u] -= 1
            sisi_tersisa[v] -= 1
        elif len(nodes) == 1:  # Menghindari infinite loop jika hanya ada satu simpul dengan derajat tersisa
            break

    print("-" * 30)

    # Menambahkan sisi ganda jika diinginkan
    opsi_sisi_ganda = get_input_angka("Apakah Anda ingin menambahkan sisi ganda? (1: Ya, 0: Tidak): ")
    if opsi_sisi_ganda == 1:
        jumlah_sisi_ganda = get_input_angka("Masukkan jumlah sisi ganda yang ingin Anda tambahkan: ")
        for _ in range(jumlah_sisi_ganda):
            u, v = np.random.choice(list(G.nodes), size=2)
            G.add_edge(u, v)

    # Menambahkan loop jika diinginkan
    opsi_loop = get_input_angka("Apakah Anda ingin menambahkan loop? (1: Ya, 0: Tidak): ")
    if opsi_loop == 1:
        jumlah_loop = get_input_angka("Masukkan jumlah loop yang ingin Anda tambahkan: ")
        for _ in range(jumlah_loop):
            node = np.random.choice(list(G.nodes))
            G.add_edge(node, node)

    print(f"Graf berhasil dibuat dengan {G.number_of_edges()} sisi.")
    return G


def gambar_graf_dan_tampilkan_matriks(G):
    if G is None or not G.nodes():
        print("Graf kosong, tidak ada yang bisa digambar.")
        return

    # Visualisasi graf
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=14, font_weight='bold', edge_color='black', width=1.5)
    plt.title("Visualisasi Graf Berdasarkan Input Anda", size=18)
    plt.show()

    # Matriks ketetanggaan
    adjacency_matrix = nx.adjacency_matrix(G).toarray()
    print("Matriks Ketetanggaan:")
    print(adjacency_matrix)

    # Derajat simpul
    derajat = dict(G.degree())
    print("\nDerajat setiap simpul:")
    for simpul, nilai_derajat in derajat.items():
        print(f"  Simpul {simpul}: {nilai_derajat}")


if __name__ == "__main__":
    graf_kustom = buat_graf_otomatis()
    gambar_graf_dan_tampilkan_matriks(graf_kustom)
