import networkx as nx
import matplotlib.pyplot as plt
import random

def buat_graf_dari_flowchart():
    """
    Fungsi utama untuk membuat dan memvisualisasikan graf berdasarkan
    langkah-langkah pada flowchart.
    """
    print("==============================================")
    print(" Selamat Datang di Program Pembuat Graf ")
    print("==============================================")

    # Langkah 1: Input Simpul
    try:
        input_simpul = input("Masukkan nama simpul (pisahkan dengan spasi): ").strip().split()
        if not input_simpul:
            print("Error: Tidak ada simpul yang dimasukkan. Program berhenti.")
            return
        # Menghilangkan duplikat jika ada
        simpul = sorted(list(set(input_simpul))) 
        print(f"Simpul yang akan dibuat: {', '.join(simpul)}")
        print("-" * 30)
    except Exception as e:
        print(f"Terjadi error saat input simpul: {e}")
        return

    # Langkah 2: Input Derajat Masing-Masing Simpul
    derajat = {}
    for s in simpul:
        while True:
            try:
                d = int(input(f"Masukkan derajat untuk simpul '{s}': "))
                if d < 0:
                    print("Derajat tidak boleh negatif. Silakan coba lagi.")
                    continue
                derajat[s] = d
                break
            except ValueError:
                print("Input tidak valid. Harap masukkan angka bulat.")
    
    # Validasi berdasarkan Handshaking Lemma
    total_derajat = sum(derajat.values())
    print("-" * 30)
    print(f"Total jumlah derajat semua simpul: {total_derajat}")
    if total_derajat % 2 != 0:
        print("\nError: Jumlah total derajat adalah ganjil.")
        print("Berdasarkan Handshaking Lemma, graf dengan urutan derajat ini tidak mungkin ada.")
        print("Program berhenti.")
        return

    # Langkah 3: Percabangan (Dengan atau Tanpa Syarat)
    print("\nGraf yang akan dibuat bisa berupa:")
    print("1. Graf Sederhana (Tanpa sisi ganda atau loop)")
    print("2. Graf Umum (Boleh memiliki sisi ganda atau loop)")
    
    pilihan = ''
    while pilihan not in ['1', '2']:
        pilihan = input("Pilih tipe graf yang ingin dibuat (1/2): ")
        if pilihan not in ['1', '2']:
            print("Pilihan tidak valid. Harap masukkan '1' atau '2'.")

    # Membuat list derajat sesuai urutan simpul
    urutan_derajat = [derajat[s] for s in simpul]
    G = None # Inisialisasi variabel graf

    # Membuat pemetaan dari node integer (hasil library) ke nama simpul
    pemetaan_label = {i: simpul[i] for i in range(len(simpul))}

    if pilihan == '1':
        # --- JALUR TANPA SYARAT (GRAF SEDERHANA) ---
        print("\nMembuat Graf Sederhana (tanpa sisi ganda/loop)...")
        
        # Cek apakah urutan derajat bisa membentuk graf sederhana
        if not nx.is_graphical(urutan_derajat):
            print("\nError: Urutan derajat yang diberikan TIDAK BISA membentuk graf sederhana.")
            print("Silakan coba lagi dengan urutan derajat yang berbeda atau pilih opsi graf umum.")
            return
            
        # Membuat graf menggunakan algoritma Havel-Hakimi
        G_temp = nx.havel_hakimi_graph(urutan_derajat)
        # Mengganti label integer dengan nama simpul yang diinginkan
        G = nx.relabel_nodes(G_temp, pemetaan_label)
        print("Graf sederhana berhasil dibuat.")

    else:
        # --- JALUR DENGAN SYARAT (GRAF UMUM/PSEUDOGRAPH) ---
        print("\nMembuat Graf Umum (mengizinkan sisi ganda/loop)...")
        
        # Membuat graf menggunakan configuration model
        # Model ini membuat graf yang memenuhi derajat, bisa menghasilkan MultiGraph
        G_temp = nx.configuration_model(urutan_derajat)
        # Mengganti label dan memastikan tipe graf adalah MultiGraph
        G = nx.MultiGraph(nx.relabel_nodes(G_temp, pemetaan_label))
        
        # Menghitung jumlah loop dan sisi ganda sesuai flowchart
        jumlah_loop = G.number_of_selfloops()
        
        # Sisi ganda adalah sisi yang muncul lebih dari satu kali antara dua simpul yang sama
        sisi_ganda = 0
        edges = list(G.edges())
        unique_edges = set(map(frozenset, edges))
        if len(edges) > len(unique_edges):
             sisi_ganda = len(edges) - len(unique_edges) - jumlah_loop
        
        print("Graf umum berhasil dibuat.")
        print(f"-> Jumlah sisi ganda yang dihasilkan: {sisi_ganda}")
        print(f"-> Jumlah loop yang dihasilkan: {jumlah_loop}")


    # Langkah terakhir: Cetak Visualisasi
    if G is not None:
        print("\nMenyiapkan visualisasi graf...")
        plt.figure(figsize=(10, 8))
        
        # Menentukan posisi node agar tidak tumpang tindih
        pos = nx.spring_layout(G, seed=42) 
        
        # Menggambar node, sisi, dan label
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='skyblue')
        nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.8, edge_color='gray', connectionstyle='arc3,rad=0.1')
        nx.draw_networkx_labels(G, pos, font_size=16, font_family='sans-serif')
        
        # Memberi judul pada plot
        plt.title("Visualisasi Graf", size=20)
        
        # Menampilkan plot
        print("Visualisasi akan ditampilkan di jendela baru.")
        plt.show()

    print("\n==============================================")
    print("Program Selesai.")
    print("==============================================")


if __name__ == '__main__':
    buat_graf_dari_flowchart()