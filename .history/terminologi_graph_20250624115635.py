import networkx as nx
import matplotlib.pyplot as plt
import random

def get_integer_input(prompt):
    """Fungsi bantuan untuk memastikan input adalah integer positif."""
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            else:
                print("Input harus berupa bilangan non-negatif. Silakan coba lagi.")
        except ValueError:
            print("Input tidak valid. Harap masukkan sebuah angka.")

def visualisasi_graf(graph, title="Visualisasi Graf"):
    """Fungsi untuk mencetak visualisasi graf."""
    print("\nMencetak visualisasi...")
    # Menggunakan layout 'spring' agar posisi simpul tersebar secara alami
    # seed digunakan agar layout konsisten setiap kali dijalankan untuk graf yang sama
    pos = nx.spring_layout(graph, seed=42)
    
    plt.figure(figsize=(10, 8))
    
    # Menggambar simpul, sisi, dan label
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=2000, 
            edge_color='gray', width=1.5, font_size=12, font_weight='bold')

    # Menambahkan label derajat pada setiap simpul
    try:
        labels = {node: f'd={degree}' for node, degree in graph.degree()}
        # Posisikan label derajat sedikit di bawah simpul
        pos_labels = {key: (value[0], value[1] - 0.1) for key, value in pos.items()}
        nx.draw_networkx_labels(graph, pos_labels, labels=labels, font_size=10, font_color='red')
    except Exception:
        # Jika terjadi error pada penghitungan derajat (meskipun jarang)
        pass

    plt.title(title)
    plt.show()
    print("Visualisasi selesai ditampilkan.")


def havel_hakimi_construction(degree_sequence):
    """
    Konstruksi graf sederhana menggunakan algoritma Havel-Hakimi.
    Mengembalikan daftar sisi (edges) jika graf dapat dibuat, selain itu None.
    """
    # Pasangkan simpul dengan derajatnya dan urutkan
    seq = sorted([(d, n) for n, d in degree_sequence.items()], reverse=True)
    
    if not seq:
        return []

    # Jika ada derajat negatif setelah modifikasi, itu tidak mungkin
    if seq[-1][0] < 0:
        return None

    # Base case: semua derajat adalah 0
    if seq[0][0] == 0:
        return []

    # Ambil simpul dengan derajat tertinggi
    (d, v) = seq.pop(0)

    # Jika derajat yang dibutuhkan lebih besar dari jumlah simpul yang tersisa
    if d > len(seq):
        return None

    # Hubungkan v ke d simpul berikutnya
    edges = [(v, seq[i][1]) for i in range(d)]
    
    # Kurangi derajat dari simpul yang terhubung
    new_degree_sequence = {node: degree for degree, node in seq}
    for i in range(d):
        node_to_update = seq[i][1]
        new_degree_sequence[node_to_update] -= 1
        
    # Rekursi dengan urutan derajat yang baru
    remaining_edges = havel_hakimi_construction(new_degree_sequence)
    
    if remaining_edges is not None:
        return edges + remaining_edges
    else:
        return None


def main():
    """Fungsi utama yang menjalankan alur program sesuai flowchart."""
    
    # 1. Start
    print("===== Program Visualisasi Pembuatan Graf =====")
    print("Mulai")

    # 2. Input Simpul
    simpul_input = input("Masukkan nama-nama simpul (pisahkan dengan spasi, contoh: A B C D): ")
    simpul = simpul_input.strip().split()
    if not simpul:
        print("Tidak ada simpul yang dimasukkan. Program berhenti.")
        return

    # 3. Input Derajat Masing-masing Simpul
    derajat = {}
    print("\n--- Input Derajat Simpul ---")
    for s in simpul:
        derajat[s] = get_integer_input(f"Masukkan derajat untuk simpul '{s}': ")

    # Validasi dasar: Jumlah semua derajat harus genap (Handshaking Lemma)
    if sum(derajat.values()) % 2 != 0:
        print("\n[Error] Jumlah total derajat semua simpul adalah ganjil. Graf tidak dapat dibuat.")
        print("Finish")
        return
        
    G = nx.MultiGraph() # Menggunakan MultiGraph untuk mendukung sisi ganda dan loop
    G.add_nodes_from(simpul)

    # 4. Percabangan Logika
    print("\nPilih metode pembuatan graf:")
    print("1. Cetak tanpa syarat (bebas menggunakan loop atau sisi ganda)")
    print("2. Cetak menggunakan syarat (menentukan jumlah loop dan sisi ganda)")
    
    choice = ""
    while choice not in ['1', '2']:
        choice = input("Masukkan pilihan Anda (1 atau 2): ")

    if choice == '1':
        # --- PATH KIRI: Tanpa Syarat ---
        print("\n--- Opsi 1: Membuat Graf Tanpa Syarat Tambahan ---")
        
        # Logika: Membuat daftar "stubs" (ujung sisi) untuk setiap simpul
        # lalu menghubungkannya secara acak. Ini secara alami bisa menghasilkan
        # loop (jika stub dari simpul yang sama terhubung) dan sisi ganda.
        stubs = []
        for node, deg in derajat.items():
            stubs.extend([node] * deg)
        
        # Acak daftar stubs untuk membuat koneksi random
        random.shuffle(stubs)
        
        # Hubungkan stubs berpasangan untuk membentuk sisi
        while len(stubs) > 1:
            u = stubs.pop()
            v = stubs.pop()
            G.add_edge(u, v)

        # Cetak Visualisasi
        visualisasi_graf(G, "Graf Dibuat Tanpa Syarat (Bebas Loop/Sisi Ganda)")

    elif choice == '2':
        # --- PATH KANAN: Dengan Syarat ---
        print("\n--- Opsi 2: Membuat Graf Dengan Syarat ---")
        
        derajat_sisa = derajat.copy()
        
        # Input Jumlah Sisi Ganda
        jml_sisi_ganda = get_integer_input("Masukkan jumlah sisi ganda yang diinginkan: ")
        for i in range(jml_sisi_ganda):
            while True:
                try:
                    pair_input = input(f"Sisi ganda ke-{i+1}: Masukkan 2 simpul (pisahkan spasi, cth: A B): ")
                    u, v = pair_input.strip().split()
                    if u in simpul and v in simpul:
                        if u == v:
                            print("Sisi ganda harus menghubungkan dua simpul yang berbeda. Untuk sisi ke diri sendiri, gunakan opsi loop.")
                            continue
                        # Tambahkan sisi ini dan kurangi derajat yang tersisa
                        G.add_edge(u, v)
                        derajat_sisa[u] -= 1
                        derajat_sisa[v] -= 1
                        if derajat_sisa[u] < 0 or derajat_sisa[v] < 0:
                           raise ValueError("Derajat simpul menjadi negatif, input tidak valid.")
                        break
                    else:
                        print("Salah satu atau kedua simpul tidak ada. Coba lagi.")
                except ValueError as e:
                    print(f"[Error] Input tidak valid atau menyebabkan derajat negatif. {e}. Program berhenti.")
                    return

        # Input Jumlah Loop
        jml_loop = get_integer_input("Masukkan jumlah loop yang diinginkan: ")
        for i in range(jml_loop):
            while True:
                try:
                    node_input = input(f"Loop ke-{i+1}: Masukkan 1 simpul untuk loop: ").strip()
                    if node_input in simpul:
                        # Loop mengurangi derajat sebanyak 2
                        G.add_edge(node_input, node_input)
                        derajat_sisa[node_input] -= 2
                        if derajat_sisa[node_input] < 0:
                            raise ValueError("Derajat simpul menjadi negatif, input tidak valid.")
                        break
                    else:
                        print("Simpul tidak ada. Coba lagi.")
                except ValueError as e:
                    print(f"[Error] Input tidak valid atau menyebabkan derajat negatif. {e}. Program berhenti.")
                    return

        print("\nDerajat sisa yang perlu dipenuhi dengan graf sederhana:")
        print(derajat_sisa)

        # Coba buat graf sederhana dari derajat sisa menggunakan Havel-Hakimi
        sisi_sederhana = havel_hakimi_construction(derajat_sisa)
        
        if sisi_sederhana is None:
            print("\n[Error] Graf tidak dapat dibuat dengan kombinasi derajat, sisi ganda, dan loop yang diberikan.")
            print("Tidak mungkin untuk membentuk graf sederhana dari sisa derajat yang ada.")
        else:
            G.add_edges_from(sisi_sederhana)
            # Cetak Visualisasi
            visualisasi_graf(G, "Graf Dibuat Dengan Syarat Loop dan Sisi Ganda")

    # 5. Finish
    print("\nFinish")
    print("===== Program Selesai =====")

if __name__ == '__main__':
    main()