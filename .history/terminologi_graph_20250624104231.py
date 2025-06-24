import networkx as nx
import matplotlib.pyplot as plt

def get_input_angka(prompt):
    """Fungsi bantuan untuk memastikan input adalah angka integer positif."""
    while True:
        try:
            nilai = int(input(prompt))
            if nilai >= 0:
                return nilai
            else:
                print("Input tidak boleh negatif. Silakan coba lagi.")
        except ValueError:
            print("Input tidak valid. Harap masukkan sebuah angka.")

def buat_graf_manual():
    G = nx.MultiGraph()

    jumlah_simpul = get_input_angka("Masukkan jumlah total simpul (nodes) yang Anda inginkan: ")
    if jumlah_simpul == 0:
        print("Tidak ada simpul yang dibuat. Program selesai.")
        return None
    
    simpul_list = range(1, jumlah_simpul + 1)
    G.add_nodes_from(simpul_list)
    print(f"Berhasil membuat {jumlah_simpul} simpul, yaitu: {list(simpul_list)}")
    print("-" * 30)

    jumlah_sisi = get_input_angka("Masukkan jumlah sisi (edges) yang ingin Anda tambahkan: ")
    for i in range(jumlah_sisi):
        while True:
            try:
                prompt_sisi = f"Sisi ke-{i+1}: Masukkan 2 simpul yang terhubung (contoh: 1 2): "
                u, v = map(int, input(prompt_sisi).split())
                if u in simpul_list and v in simpul_list:
                    G.add_edge(u, v)
                    print(f"   -> Sisi ({u}, {v}) berhasil ditambahkan.")
                    break
                else:
                    print(f"   -> Simpul tidak valid. Harap masukkan angka antara 1 dan {jumlah_simpul}.")
            except ValueError:
                print("   -> Format input salah. Harap masukkan dua angka yang dipisahkan spasi.")
    print("-" * 30)

    jumlah_sisi_ganda = get_input_angka("Masukkan jumlah sisi ganda (multiple edges) yang ingin Anda tambahkan: ")
    for i in range(jumlah_sisi_ganda):
        while True:
            try:
                prompt_ganda = f"Sisi Ganda ke-{i+1}: Masukkan 2 simpul yang sama (contoh: 3 4): "
                u, v = map(int, input(prompt_ganda).split())
                if u in simpul_list and v in simpul_list:
                    G.add_edge(u, v)
                    print(f"   -> Sisi ganda antara ({u}, {v}) berhasil ditambahkan.")
                    break
                else:
                    print(f"   -> Simpul tidak valid. Harap masukkan angka antara 1 dan {jumlah_simpul}.")
            except ValueError:
                print("   -> Format input salah. Harap masukkan dua angka yang dipisahkan spasi.")
    print("-" * 30)
    
    jumlah_loop = get_input_angka("Masukkan jumlah loop (gelang) yang ingin Anda tambahkan: ")
    for i in range(jumlah_loop):
        while True:
            try:
                prompt_loop = f"Loop ke-{i+1}: Masukkan 1 simpul untuk diberi loop (contoh: 5): "
                node = int(input(prompt_loop))
                if node in simpul_list:
                    G.add_edge(node, node) # Loop adalah sisi dari simpul ke dirinya sendiri 
                    print(f"   -> Loop pada simpul ({node}) berhasil ditambahkan.")
                    break
                else:
                    print(f"   -> Simpul tidak valid. Harap masukkan angka antara 1 dan {jumlah_simpul}.")
            except ValueError:
                print("   -> Format input salah. Harap masukkan satu angka.")
    print("-" * 30)
    
    return G

def gambar_graf(G):
    if G is None or not G.nodes():
        print("Graf kosong, tidak ada yang bisa digambar.")
        return
    
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(12, 10))

    # Menggambar komponen graf
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=2000, font_size=14, font_weight='bold', edge_color='black', width=1.5)

    # Menampilkan informasi derajat di konsol
    try:
        # Derajat adalah jumlah sisi yang bersisian dengan simpul 
        derajat = dict(G.degree())
        print("Analisis Graf Hasil Input:")
        print(f"  - Derajat setiap simpul: {derajat}")
        # Lemma Jabat Tangan: Jumlah derajat = 2 * jumlah sisi 
        print(f"  - Jumlah semua derajat (verifikasi Lemma Jabat Tangan): {sum(derajat.values())} == 2 * {G.number_of_edges()}")
    except Exception as e:
        print(f"Tidak dapat menghitung derajat: {e}")

    # Menampilkan judul dan informasi pada gambar
    plt.title("Visualisasi Graf Berdasarkan Input Anda", size=18)
    print("\nMenampilkan graf...")
    plt.show()

# --- BLOK EKSEKUSI UTAMA ---
if __name__ == "__main__":
    # 1. Membuat graf berdasarkan input interaktif dari pengguna
    graf_kustom = buat_graf_manual()

    # 2. Menggambar graf yang sudah dibuat
    gambar_graf(graf_kustom)