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

def buat_graf_dengan_pengkondisian():
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
    derajat_simpul = []
    for node in simpul_list:
        derajat = get_input_angka(f"Masukkan derajat untuk simpul {node}: ")
        derajat_simpul.append((node, derajat))
    print("Derajat masing-masing simpul telah ditentukan.")
    print("-" * 30)

    # Menambahkan sisi ganda jika diinginkan
    opsi_sisi_ganda = get_input_angka("Apakah Anda ingin menambahkan sisi ganda? (1: Ya, 0: Tidak): ")
    if opsi_sisi_ganda == 1:
        jumlah_sisi_ganda = get_input_angka("Masukkan jumlah sisi ganda yang ingin Anda tambahkan: ")
        for i in range(jumlah_sisi_ganda):
            while True:
                try:
                    prompt_ganda = f"Sisi Ganda ke-{i+1}: Masukkan 2 simpul (contoh: 3 4): "
                    u, v = map(int, input(prompt_ganda).split())
                    if u in simpul_list and v in simpul_list:
                        G.add_edge(u, v)
                        print(f"   -> Sisi ganda ({u}, {v}) berhasil ditambahkan.")
                        break
                    else:
                        print(f"   -> Simpul tidak valid. Harap masukkan angka antara 1 dan {jumlah_simpul}.")
                except ValueError:
                    print("   -> Format input salah. Harap masukkan dua angka yang dipisahkan spasi.")

    # Menambahkan loop jika diinginkan
    opsi_loop = get_input_angka("Apakah Anda ingin menambahkan loop? (1: Ya, 0: Tidak): ")
    if opsi_loop == 1:
        jumlah_loop = get_input_angka("Masukkan jumlah loop yang ingin Anda tambahkan: ")
        for i in range(jumlah_loop):
            while True:
                try:
                    prompt_loop = f"Loop ke-{i+1}: Masukkan 1 simpul untuk diberi loop (contoh: 5): "
                    node = int(input(prompt_loop))
                    if node in simpul_list:
                        G.add_edge(node, node)  # Loop adalah sisi dari simpul ke dirinya sendiri
                        print(f"   -> Loop pada simpul ({node}) berhasil ditambahkan.")
                        break
                    else:
                        print(f"   -> Simpul tidak valid. Harap masukkan angka antara 1 dan {jumlah_simpul}.")
                except ValueError:
                    print("   -> Format input salah. Harap masukkan satu angka.")
    print("-" * 30)

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

if __name__ == "__main__":
    graf_kustom = buat_graf_dengan_pengkondisian()
    gambar_graf_dan_tampilkan_matriks(graf_kustom)
