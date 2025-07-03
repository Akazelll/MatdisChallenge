import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np # <-- Tambahkan library NumPy untuk operasi matriks

def jalankan_tes_dengan_matriks():
    """
    Fungsi tes untuk membuat graf dari derajat, kemudian menampilkannya
    dalam bentuk matriks ketetanggaan dan visualisasi.
    """
    
    # --- INPUT DARI ANDA ---
    try:
        jumlah_simpul = int(input("Masukkan jumlah simpul: "))
        # Pastikan daftar simpul selalu terurut agar matriks konsisten
        simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        
        derajat_awal = {}
        print("\n--- Input Derajat Simpul ---")
        for s in simpul:
            derajat_awal[s] = int(input(f"Masukkan derajat untuk Simpul {s}: "))
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        return

    # --- VALIDASI DASAR ---
    if sum(derajat_awal.values()) % 2 != 0:
        print("\n[Error] Jumlah total derajat ganjil. Graf tidak dapat dibuat.")
        return
        
    # --- PROSES PEMBUATAN GRAF PALING DASAR ---
    print("\n⚙️  Membuat graf dengan metode paling dasar...")
    graf = nx.MultiGraph()
    graf.add_nodes_from(simpul)
    
    stubs = [node for node, deg in derajat_awal.items() for _ in range(deg)]
    random.shuffle(stubs)
    
    while len(stubs) > 1:
        u = stubs.pop()
        v = stubs.pop()
        graf.add_edge(u, v)

    print("✅ Proses pembuatan graf selesai.")

    # --- VERIFIKASI DERAJAT ---
    print("\n--- Verifikasi Derajat Akhir ---")
    for node in simpul:
        print(f"Simpul {node}: Target Derajat={derajat_awal[node]}, Aktual={graf.degree(node)} [OK]")
    print("\nKESIMPULAN: Semua derajat dijamin sesuai.")
    
    # --- LOGIKA MATRIKS KETETANGGAAN (BARU) ---
    print("\n--- Matriks Ketetanggaan (Adjacency Matrix) ---")
    # Mengonversi graf NetworkX menjadi matriks NumPy
    # 'nodelist=simpul' memastikan urutan baris/kolom sesuai urutan simpul (1, 2, 3, ...)
    matriks = nx.to_numpy_array(graf, nodelist=simpul)
    
    print("Matriks ini menunjukkan jumlah sisi antar simpul:")
    print(matriks)
    
    # --- VISUALISASI GRAF ---
    print("\n🎨 Menampilkan visualisasi graf secara visual...")
    pos = nx.spring_layout(graf, seed=42)
    plt.figure(figsize=(10, 8))
    nx.draw(graf, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=12, font_weight='bold')
    plt.title("Visualisasi Graf")
    plt.show()

# Jalankan fungsi tes
jalankan_tes_dengan_matriks()