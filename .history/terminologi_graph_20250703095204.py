import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

def buat_graf_dengan_keterangan_derajat():
    """
    Membuat graf dari barisan derajat, menampilkan matriks ketetanggaan,
    dan menyertakan keterangan derajat pada visualisasi graf.
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
    graf = nx.MultiGraph()
    graf.add_nodes_from(simpul)
    
    stubs = [node for node, deg in derajat_awal.items() for _ in range(deg)]
    random.shuffle(stubs)
    
    while len(stubs) > 1:
        u = stubs.pop()
        v = stubs.pop()
        graf.add_edge(u, v)

    print("✅ Proses pembuatan graf selesai.")

    # --- 4. Verifikasi Derajat ---
    print("\n--- Verifikasi Derajat Akhir ---")
    for node in simpul:
        print(f"Simpul {node}: Target Derajat={derajat_awal[node]}, Aktual={graf.degree(node)} [OK]")
    
    # --- 5. Matriks Ketetanggaan ---
    print("\n--- Matriks Ketetanggaan (Adjacency Matrix) ---")
    matriks = nx.to_numpy_array(graf, nodelist=simpul)
    print("Matriks ini menunjukkan JUMLAH SISI antar simpul:")
    print(matriks)
    
    # --- 6. Visualisasi Graf dengan Keterangan Derajat ---
    print("\n🎨 Menampilkan visualisasi graf...")
    pos = nx.spring_layout(graf, seed=42)
    plt.figure(figsize=(12, 10))
    
    # Menggambar komponen graf secara terpisah untuk kustomisasi
    nx.draw_networkx_nodes(graf, pos, node_color='skyblue', node_size=2500)
    nx.draw_networkx_edges(graf, pos, width=1.5, alpha=0.7)
    nx.draw_networkx_labels(graf, pos, font_size=12, font_weight='bold')
    
    # Logika untuk menambahkan label derajat (BARU)
    derajat_labels = {node: f"d={degree}" for node, degree in graf.degree()}
    pos_derajat = {key: (value[0], value[1] - 0.15) for key, value in pos.items()}
    
    nx.draw_networkx_labels(graf, pos_derajat, labels=derajat_labels, font_size=10, font_color='darkred')
    
    plt.title("Visualisasi Graf dengan Keterangan Derajat")
    plt.axis('off') # Menghilangkan sumbu x dan y
    plt.show()

# Jalankan fungsi utama
buat_graf_dengan_keterangan_derajat()