import networkx as nx
import matplotlib.pyplot as plt
import random

def jalankan_tes_sederhana():
    """Fungsi tes yang paling sederhana untuk membuat graf dari derajat."""
    
    # --- INPUT DARI ANDA ---
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

    # --- VALIDASI DASAR ---
    if sum(derajat_awal.values()) % 2 != 0:
        print("\n[Error] Jumlah total derajat ganjil. Graf tidak dapat dibuat.")
        return
        
    # --- PROSES PEMBUATAN GRAF PALING DASAR (Configuration Model) ---
    print("\n⚙️ Membuat graf dengan metode paling dasar...")
    graf = nx.MultiGraph()
    graf.add_nodes_from(simpul)
    
    # Buat 'stubs' (titik koneksi) berdasarkan derajat
    stubs = [node for node, deg in derajat_awal.items() for _ in range(deg)]
    random.shuffle(stubs)
    
    # Hubungkan stubs secara acak
    while len(stubs) > 1:
        u = stubs.pop()
        v = stubs.pop()
        graf.add_edge(u, v)

    print("✅ Proses pembuatan graf selesai.")

    # --- VERIFIKASI DAN VISUALISASI ---
    print("\n--- Verifikasi Derajat Akhir ---")
    derajat_sesuai = True
    for node in simpul:
        derajat_target = derajat_awal[node]
        derajat_aktual = graf.degree(node)
        status = "[OK]"
        if derajat_target != derajat_aktual:
            status = "[GAGAL!]"
            derajat_sesuai = False
        print(f"Simpul {node}: Target Derajat={derajat_target}, Aktual={derajat_aktual} {status}")
    
    if not derajat_sesuai:
        print("\nKESIMPULAN: Ada derajat yang TIDAK SESUAI. Ini indikasi masalah.")
    else:
        print("\nKESIMPULAN: Semua derajat SUDAH SESUAI.")

    # Visualisasi
    print("\n🎨 Menampilkan visualisasi...")
    pos = nx.spring_layout(graf, seed=42)
    plt.figure(figsize=(10, 8))
    nx.draw(graf, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=12, font_weight='bold')
    plt.show()

# Jalankan fungsi tes
jalankan_tes_sederhana()