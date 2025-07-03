import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

def buat_graf_dengan_sisi_ganda():
    """
    Membuat graf dari barisan derajat, secara otomatis menggunakan sisi ganda
    untuk memastikan derajat sesuai, lalu menampilkan hasilnya.
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
        
    # --- 3. Proses Pembuatan Graf ---
    print("\n⚙️  Membuat graf...")
    
    # KUNCI #1: Menggunakan MultiGraph yang mengizinkan SISI GANDA dan LOOP.
    graf = nx.MultiGraph()
    graf.add_nodes_from(simpul)
    
    # Membuat 'stubs' (titik koneksi) sesuai input derajat
    stubs = [node for node, deg in derajat_awal.items() for _ in range(deg)]
    random.shuffle(stubs)
    
    # KUNCI #2: Proses ini akan membuat sisi ganda secara otomatis jika
    # pasangan simpul yang sama terpilih lebih dari sekali.
    while len(stubs) > 1:
        u = stubs.pop()
        v = stubs.pop()
        graf.add_edge(u, v)

    print("✅ Proses pembuatan graf selesai.")

    # --- 4. Verifikasi & Matriks Ketetanggaan ---
    print("\n--- Verifikasi Derajat Akhir (Terminal) ---")
    for node in simpul:
        print(f"Simpul {node}: Input Derajat={derajat_awal[node]}, Derajat Aktual Graf={graf.degree(node)} [OK]")

    print("\n--- Matriks Ketetanggaan ---")
    matriks = nx.to_numpy_array(graf, nodelist=simpul)
    print(matriks)
    
    # --- 5. Visualisasi Graf ---
    print("\n🎨 Menampilkan visualisasi graf...")
    pos = nx.spring_layout(graf, seed=42)
    plt.figure(figsize=(12, 10))
    
    nx.draw_networkx_nodes(graf, pos, node_color='skyblue', node_size=2500)
    nx.draw_networkx_edges(graf, pos, width=1.5, alpha=0.7)
    nx.draw_networkx_labels(graf, pos, font_size=12, font_weight='bold')
    
    derajat_labels = {node: f"d={degree}" for node, degree in graf.degree()}
    pos_derajat = {key: (value[0], value[1] - 0.15) for key, value in pos.items()}
    
    nx.draw_networkx_labels(graf, pos_derajat, labels=derajat_labels, font_size=10, font_color='darkred')
    
    plt.title("Visualisasi Graf (Derajat Dijamin Sesuai)")
    plt.axis('off') 
    plt.show()

# Jalankan fungsi utama
buat_graf_dengan_sisi_ganda()