import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def get_integer_input(prompt):
    """Fungsi bantuan untuk memastikan input adalah integer non-negatif."""
    while True:
        try:
            val = int(input(prompt))
            if val < 0:
                print("Input tidak boleh negatif. Silakan coba lagi.")
                continue
            return val
        except ValueError:
            print("Input tidak valid. Harap masukkan sebuah angka.")

def get_node_input(prompt, node_list):
    """Fungsi bantuan untuk mendapatkan input simpul yang valid."""
    while True:
        val = input(prompt).strip()
        if val not in node_list:
            print(f"Error: Simpul '{val}' tidak ada. Simpul yang tersedia: {', '.join(node_list)}")
        else:
            return val

def buat_graf_sesuai_flowchart():
    """
    Fungsi utama yang direvisi untuk membuat graf presis sesuai flowchart.
    """
    print("==============================================")
    print(" Selamat Datang di Program Pembuat Graf ")
    print("==============================================")

    # 1. Input Simpul
    input_simpul = input("Masukkan nama simpul (pisahkan dengan spasi): ").strip().split()
    if not input_simpul:
        print("Error: Tidak ada simpul yang dimasukkan. Program berhenti.")
        return
    simpul = sorted(list(set(input_simpul)))
    print(f"Simpul yang akan dibuat: {', '.join(simpul)}")
    print("-" * 30)

    # 2. Input Derajat Masing-Masing Simpul
    target_derajat = {}
    for s in simpul:
        target_derajat[s] = get_integer_input(f"Masukkan target derajat untuk simpul '{s}': ")

    total_derajat = sum(target_derajat.values())
    print("-" * 30)
    print(f"Total target derajat semua simpul: {total_derajat}")
    if total_derajat % 2 != 0:
        print("\nError: Jumlah total derajat adalah ganjil. Graf tidak mungkin ada.")
        return

    # 3. Percabangan (Syarat)
    print("\nPilih alur flowchart:")
    print("1. Cetak tanpa syarat (Graf Sederhana)")
    print("2. Gunakan syarat (Input sisi ganda dan loop)")
    pilihan = ''
    while pilihan not in ['1', '2']:
        pilihan = input("Pilih alur yang ingin dieksekusi (1/2): ")

    G = None

    if pilihan == '1':
        # --- JALUR KIRI: TANPA SYARAT ---
        print("\nAlur 'Tanpa Syarat' dipilih.")
        urutan_derajat = [target_derajat[s] for s in simpul]
        if not nx.is_graphical(urutan_derajat):
            print("\nError: Urutan derajat ini TIDAK BISA membentuk graf sederhana.")
            return
        
        print("Membuat graf sederhana...")
        G_temp = nx.havel_hakimi_graph(urutan_derajat)
        pemetaan = {i: simpul[i] for i in range(len(simpul))}
        G = nx.relabel_nodes(G_temp, pemetaan)
        print("Graf sederhana berhasil dibuat.")

    else:
        # --- JALUR KANAN: DENGAN SYARAT ---
        print("\nAlur 'Dengan Syarat' dipilih.")
        G = nx.MultiGraph()
        G.add_nodes_from(simpul)
        
        # 4. Input Jumlah Sisi Ganda
        jml_sisi_ganda = get_integer_input("Input jumlah sisi ganda: ")
        for i in range(jml_sisi_ganda):
            print(f"--- Sisi Ganda ke-{i+1}/{jml_sisi_ganda} ---")
            while True:
                s1 = get_node_input(f"Masukkan simpul pertama: ", simpul)
                s2 = get_node_input(f"Masukkan simpul kedua: ", simpul)
                if s1 == s2:
                    print("Sisi ganda harus menghubungkan dua simpul yang berbeda.")
                else:
                    G.add_edge(s1, s2)
                    print(f"Sisi ganda antara '{s1}' dan '{s2}' ditambahkan.")
                    break
        
        # 5. Input Jumlah Loop
        jml_loop = get_integer_input("\nInput jumlah loop: ")
        for i in range(jml_loop):
            s = get_node_input(f"--- Masukkan simpul untuk loop ke-{i+1}/{jml_loop}: ", simpul)
            G.add_edge(s, s)
            print(f"Loop pada simpul '{s}' ditambahkan.")

        # Menghitung sisa derajat yang perlu dipenuhi
        derajat_sisa = defaultdict(int)
        
        # Derajat saat ini dari graf (loop dihitung 2)
        derajat_sekarang = dict(G.degree())

        valid = True
        for s in simpul:
            sisa = target_derajat[s] - derajat_sekarang[s]
            if sisa < 0:
                print(f"\nError: Derajat simpul '{s}' ({derajat_sekarang[s]}) sudah melebihi target ({target_derajat[s]}).")
                print("Kombinasi ini tidak mungkin. Program berhenti.")
                valid = False
                break
            derajat_sisa[s] = sisa
        
        if not valid:
            return

        # Membuat 'stubs' (koneksi terbuka) dari sisa derajat
        stub_list = []
        for s, d in derajat_sisa.items():
            stub_list.extend([s] * d)

        if sum(derajat_sisa.values()) % 2 != 0:
             print("\nError: Sisa derajat yang perlu dipenuhi ganjil. Tidak bisa diselesaikan.")
             return
             
        # Menambahkan sisi sederhana untuk memenuhi sisa derajat
        print("\nMenambahkan sisa sisi untuk memenuhi target derajat...")
        random.shuffle(stub_list)
        if len(stub_list) > 0:
            for i in range(0, len(stub_list), 2):
                s1 = stub_list[i]
                s2 = stub_list[i+1]
                # Menghindari loop yang tidak disengaja jika memungkinkan
                if s1 == s2 and len(set(stub_list)) > 1:
                    print(f"Kombinasi sisa derajat sulit dipenuhi tanpa membuat loop baru. Mencoba tetap menghubungkan {s1}-{s2}")
                G.add_edge(s1, s2)
                print(f"Menambahkan sisi: {s1}-{s2}")

        # Verifikasi akhir
        print("\nVerifikasi Derajat Akhir:")
        final_degrees = dict(G.degree())
        for s in simpul:
            print(f"Simpul '{s}': Target={target_derajat[s]}, Hasil={final_degrees[s]}")
        
    # 6. Cetak Visualisasi
    if G is not None:
        print("\nMenyiapkan visualisasi graf...")
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, seed=42, k=0.9)
        nx.draw(G, pos, with_labels=True, node_size=2500, node_color='skyblue', font_size=14, width=1.5, connectionstyle='arc3,rad=0.1')
        plt.title("Visualisasi Graf Sesuai Flowchart", size=20)
        plt.show()

    print("\n==============================================")
    print("Program Selesai.")
    print("==============================================")

if __name__ == '__main__':
    buat_graf_sesuai_flowchart()