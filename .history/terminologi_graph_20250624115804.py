import networkx as nx
import matplotlib.pyplot as plt
import random

def get_integer_input(prompt, min_val=0):
    """Fungsi bantuan untuk memastikan input adalah integer yang valid."""
    while True:
        try:
            value = int(input(prompt))
            if value >= min_val:
                return value
            else:
                print(f"Input harus berupa bilangan non-negatif (>= {min_val}). Silakan coba lagi.")
        except ValueError:
            print("Input tidak valid. Harap masukkan sebuah angka.")

def visualisasi_graf(graph, title="Visualisasi Graf"):
    """Fungsi untuk mencetak visualisasi graf."""
    print("\nMencetak visualisasi...")
    pos = nx.spring_layout(graph, seed=42)
    
    plt.figure(figsize=(10, 8))
    
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=2000, 
            edge_color='gray', width=1.5, font_size=12, font_weight='bold')

    try:
        labels = {node: f'd={degree}' for node, degree in graph.degree()}
        pos_labels = {key: (value[0], value[1] - 0.1) for key, value in pos.items()}
        nx.draw_networkx_labels(graph, pos_labels, labels=labels, font_size=10, font_color='red')
    except Exception:
        pass

    plt.title(title)
    plt.show()
    print("Visualisasi selesai ditampilkan.")


def havel_hakimi_construction(degree_sequence):
    """
    Konstruksi graf sederhana menggunakan algoritma Havel-Hakimi.
    Mengembalikan daftar sisi (edges) jika graf dapat dibuat, selain itu None.
    """
    seq = sorted([(d, n) for n, d in degree_sequence.items()], reverse=True)
    
    if not seq:
        return []

    if seq[-1][0] < 0:
        return None

    if seq[0][0] == 0:
        return []

    (d, v) = seq.pop(0)

    if d > len(seq):
        return None

    edges = [(v, seq[i][1]) for i in range(d)]
    
    new_degree_sequence = {node: degree for degree, node in seq}
    for i in range(d):
        node_to_update = seq[i][1]
        new_degree_sequence[node_to_update] -= 1
        
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

    # 2. Input Simpul (Jumlah)
    jumlah_simpul = get_integer_input("Masukkan jumlah simpul: ", min_val=1)
    # Membuat label simpul secara otomatis dari '1' sampai 'jumlah_simpul'
    simpul = [str(i) for i in range(1, jumlah_simpul + 1)]

    # 3. Input Derajat Masing-masing Simpul
    derajat = {}
    print("\n--- Input Derajat Simpul ---")
    for s in simpul:
        derajat[s] = get_integer_input(f"Masukkan derajat untuk Simpul {s}: ")

    if sum(derajat.values()) % 2 != 0:
        print("\n[Error] Jumlah total derajat semua simpul adalah ganjil. Graf tidak dapat dibuat.")
        print("Finish")
        return
        
    G = nx.MultiGraph()
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
        
        stubs = []
        for node, deg in derajat.items():
            stubs.extend([node] * deg)
        
        random.shuffle(stubs)
        
        while len(stubs) > 1:
            u = stubs.pop()
            v = stubs.pop()
            G.add_edge(u, v)

        visualisasi_graf(G, "Graf Dibuat Tanpa Syarat (Bebas Loop/Sisi Ganda)")

    elif choice == '2':
        # --- PATH KANAN: Dengan Syarat ---
        print("\n--- Opsi 2: Membuat Graf Dengan Syarat ---")
        
        derajat_sisa = derajat.copy()
        
        jml_sisi_ganda = get_integer_input("Masukkan jumlah sisi ganda yang diinginkan: ")
        for i in range(jml_sisi_ganda):
            while True:
                try:
                    pair_input = input(f"Sisi ganda ke-{i+1}: Masukkan 2 label simpul (pisahkan spasi, cth: 1 2): ")
                    u, v = pair_input.strip().split()
                    if u in simpul and v in simpul:
                        if u == v:
                            print("Sisi ganda harus menghubungkan dua simpul berbeda. Gunakan opsi loop.")
                            continue
                        G.add_edge(u, v)
                        derajat_sisa[u] -= 1
                        derajat_sisa[v] -= 1
                        if derajat_sisa[u] < 0 or derajat_sisa[v] < 0:
                           raise ValueError("Derajat simpul menjadi negatif.")
                        break
                    else:
                        print(f"Label simpul tidak valid. Gunakan angka dari 1 hingga {jumlah_simpul}.")
                except ValueError:
                    print(f"[Error] Input tidak valid. Harap masukkan dua angka atau periksa kembali derajat.")
                    # Mengembalikan derajat yang sudah dikurangi jika error
                    if 'u' in locals() and 'v' in locals() and u in G and v in G:
                        derajat_sisa[u] += 1
                        derajat_sisa[v] += 1
                        G.remove_edge(u,v)


        jml_loop = get_integer_input("Masukkan jumlah loop yang diinginkan: ")
        for i in range(jml_loop):
            while True:
                try:
                    node_input = input(f"Loop ke-{i+1}: Masukkan 1 label simpul untuk loop: ").strip()
                    if node_input in simpul:
                        G.add_edge(node_input, node_input)
                        derajat_sisa[node_input] -= 2
                        if derajat_sisa[node_input] < 0:
                            raise ValueError("Derajat simpul menjadi negatif.")
                        break
                    else:
                        print(f"Label simpul tidak valid. Gunakan angka dari 1 hingga {jumlah_simpul}.")
                except ValueError:
                    print(f"[Error] Input tidak valid atau menyebabkan derajat negatif.")
                    if 'node_input' in locals() and node_input in G:
                        derajat_sisa[node_input] += 2
                        G.remove_edge(node_input, node_input)


        print("\nDerajat sisa yang perlu dipenuhi dengan graf sederhana:")
        print(derajat_sisa)

        sisi_sederhana = havel_hakimi_construction(derajat_sisa)
        
        if sisi_sederhana is None:
            print("\n[Error] Graf tidak dapat dibuat dengan kombinasi derajat, sisi ganda, dan loop yang diberikan.")
        else:
            G.add_edges_from(sisi_sederhana)
            visualisasi_graf(G, "Graf Dibuat Dengan Syarat Loop dan Sisi Ganda")

    # 5. Finish
    print("\nFinish")
    print("===== Program Selesai =====")

if __name__ == '__main__':
    main()