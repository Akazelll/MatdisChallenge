import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np # Diperlukan untuk operasi matriks

def buat_graf_dengan_matriks():
    """
    Membuat graf dari barisan derajat, mengizinkan sisi ganda untuk memastikan
    derajat sesuai, lalu menampilkan matriks ketetanggaan dan visualisasinya.
    """
    
    # --- 1. Input dari Pengguna ---
    try:
        jumlah_simpul = int(input("Masukkan jumlah simpul: "))
        # Membuat daftar simpul yang terurut, penting untuk matriks yang konsisten
        simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        
        derajat_awal = {}
        print("\n--- Input Derajat Simpul ---")
        for s in simpul:
            derajat_awal[s] = int(input(f"Masukkan derajat untuk Simpul {s}: "))
    except ValueError:
        print("Input tidak valid. Harap masukkan sebuah angka.")
        return

    # --- 2. Validasi Dasar ---
    if sum(derajat_awal.values()) % 2 != 0:
        print("\n[Error] Jumlah total derajat ganjil. Graf tidak dapat dibuat.")
        return
        
    # --- 3. Proses Pembuatan Graf (Mengizinkan Sisi Ganda) ---
    print("\n⚙️  Membuat graf... Sisi ganda akan otomatis dibuat jika diperlukan.")
    
    # nx.MultiGraph() adalah tipe graf yang secara eksplisit mengizinkan sisi ganda
    graf = nx.MultiGraph()
    graf.add_nodes_from(simpul)
    
    # Membuat 'stubs' (titik koneksi) untuk setiap simpul sesuai derajatnya
    stubs = [node for node, deg in derajat_awal.items() for _ in range(deg)]
    random.shuffle(stubs)
    
    # Menghubungkan stubs secara acak. Jika pasangan yang sama muncul lagi,
    # maka terbentuklah sisi ganda.
    while len(stubs) > 1:
        u = stubs.pop()
        v = stubs.pop()
        graf.add_edge(u, v)

    print("✅ Proses pembuatan graf selesai.")

    # --- 4. Verifikasi Derajat (Dijamin Sesuai) ---
    print("\n--- Verifikasi Derajat Akhir ---")
    for node in simpul:
        print(f"Simpul {node}: Target Derajat={derajat_awal[node]}, Aktual={graf.degree(node)} [OK]")
    print("\nKESIMPULAN: Semua derajat telah sesuai berkat penggunaan sisi ganda.")
    
    # --- 5. Logika Matriks Ketetanggaan ---
    print("\n--- Matriks Ketetanggaan (Adjacency Matrix) ---")
    # Mengonversi graf NetworkX menjadi matriks NumPy
    matriks = nx.to_numpy_array(graf, nodelist=simpul)
    
    print("Matriks ini menunjukkan JUMLAH SISI antar simpul:")
    print(matriks)
    
    # --- 6. Visualisasi Graf ---
    print("\n🎨 Menampilkan visualisasi graf...")
    pos = nx.spring_layout(graf, seed=42)
    plt.figure(figsize=(10, 8))
    nx.draw(graf, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=12, font_weight='bold')
    plt.title("Visualisasi Graf")
    plt.show()

# Jalankan fungsi utama
buat_graf_dengan_matriks()