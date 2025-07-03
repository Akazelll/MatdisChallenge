import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

def buat_graf_yang_benar():
    """
    Membuat graf dari barisan derajat, dijamin sesuai dengan input,
    dan menampilkan keterangan derajat yang akurat pada visualisasi.
    """
    
    # --- 1. Input dari Pengguna ---
    try:
        jumlah_simpul = int(input("Masukkan jumlah simpul: "))
        simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        
        derajat_awal = {}
        print("\n--- Input Derajat Simpul ---")
        for s in simpul:
            derajat_awal[s] = int(input(f"Masukkan derajat untuk Simpul {s}: "))
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return

    # --- 2. Validasi Dasar ---
    if sum(derajat_awal.values()) % 2 != 0:
        print("\n[Error] Jumlah total derajat ganjil. Graf tidak dapat dibuat.")
        return
        
    # --- 3. Proses Pembuatan Graf yang Dijamin Benar ---
    print("\n⚙️  Membuat graf dengan metode yang dijamin...")
    
    # nx.MultiGraph() penting untuk mengizinkan loop dan sisi ganda
    graf = nx.MultiGraph()
    graf.add_nodes_from(simpul)
    
    # Membuat 'stubs' (titik koneksi). Jumlah stub untuk setiap simpul
    # akan sama dengan derajat yang diinputkan.
    stubs = [node for node, deg in derajat_awal.items() for _ in range(deg)]
    random.shuffle(stubs)
    
    # Proses ini akan berjalan sampai semua stub habis,
    # memastikan setiap titik koneksi terpakai.
    while len(stubs) > 1:
        u = stubs.pop()
        v = stubs.pop()
        graf.add_edge(u, v)

    print("✅ Proses pembuatan graf selesai.")

    # --- 4. Verifikasi Derajat di Terminal (Bukti Kebenaran) ---
    print("\n--- Verifikasi Derajat Akhir (Terminal) ---")
    print("Bagian ini membandingkan input Anda dengan hasil akhir di graf:")
    for node in simpul:
        # Membandingkan input awal dengan derajat yang dihitung dari graf final
        print(f"Simpul {node}: Input Derajat={derajat_awal[node]}, Derajat Aktual Graf={graf.degree(node)} [DIJAMIN OK]")
    
    # --- 5. Visualisasi Graf dengan Keterangan Derajat yang Akurat ---
    print("\n🎨 Menampilkan visualisasi graf...")
    pos = nx.spring_layout(graf, seed=42)
    plt.figure(figsize=(12, 10))
    
    # Menggambar komponen graf
    nx.draw_networkx_nodes(graf, pos, node_color='skyblue', node_size=2500)
    # Menggambar sisi dengan sedikit transparansi untuk loop/sisi ganda
    nx.draw_networkx_edges(graf, pos, width=1.5, alpha=0.7)
    nx.draw_networkx_labels(graf, pos, font_size=12, font_weight='bold')
    
    # Membuat dan menampilkan label derajat berdasarkan graf final yang sudah benar
    derajat_labels = {node: f"d={degree}" for node, degree in graf.degree()}
    pos_derajat = {key: (value[0], value[1] - 0.15) for key, value in pos.items()}
    
    nx.draw_networkx_labels(graf, pos_derajat, labels=derajat_labels, font_size=10, font_color='darkred')
    
    plt.title("Visualisasi Graf dengan Derajat yang Akurat")
    plt.axis('off') 
    plt.show()

# Jalankan fungsi utama
buat_graf_yang_benar()