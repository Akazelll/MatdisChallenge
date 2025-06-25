import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict

class VisualisasiGraf:
    
    def __init__(self):
        """Inisialisasi atribut kelas."""
        self.simpul = []
        self.derajat = {}
        self.graf = nx.MultiGraph() # Menggunakan MultiGraph untuk sisi ganda dan loop

    def _dapatkan_input_integer(self, prompt, min_val=0):
        """Mendapatkan input integer yang valid dari pengguna."""
        while True:
            try:
                value = int(input(prompt))
                if value >= min_val:
                    return value
                else:
                    print(f"Input harus berupa bilangan (>= {min_val}). Coba lagi.")
            except ValueError:
                print("Input tidak valid. Harap masukkan sebuah angka.")

    def _visualisasikan(self, judul="Visualisasi Graf"):
        """Mencetak visualisasi graf menggunakan matplotlib dan networkx."""
        
        print("\nMencetak visualisasi...")
        # Pengaturan posisi simpul agar konsisten
        pos = nx.spring_layout(self.graf, seed=42)
        plt.figure(figsize=(12, 10))
        ax = plt.gca()
        
        # Gambar simpul dan labelnya
        nx.draw_networkx_nodes(self.graf, pos, ax=ax, node_color='skyblue', node_size=2500)
        nx.draw_networkx_labels(self.graf, pos, ax=ax, font_size=12, font_weight='bold')
        
        # Tambahkan label derajat di bawah setiap simpul
        try:
            derajat_labels = {node: f'd={degree}' for node, degree in self.graf.degree()}
            pos_derajat = {key: (value[0], value[1] - 0.12) for key, value in pos.items()}
            nx.draw_networkx_labels(self.graf, pos_derajat, ax=ax, labels=derajat_labels, font_size=10, font_color='darkred')
        except Exception as e:
            print(f"Tidak dapat menggambar label derajat: {e}")

        # Logika canggih untuk menggambar sisi ganda dan loop dengan rapi
        edge_groups = defaultdict(list)
        for u, v in self.graf.edges():
            # Urutkan simpul untuk mengelompokkan sisi (1,2) dan (2,1) bersama
            edge_groups[tuple(sorted((u, v)))].append((u, v))

        for key, edges in edge_groups.items():
            u, v = key
            jumlah_sisi = len(edges)
            
            # Gambar loop
            if u == v:
                # Menggambar loop membutuhkan penanganan khusus
                nx.draw_networkx_edges(self.graf, pos, edgelist=edges, ax=ax, connectionstyle='arc3,rad=0.2', arrowstyle='-')
                continue

            # Gambar sisi tunggal (garis lurus)
            if jumlah_sisi == 1:
                nx.draw_networkx_edges(self.graf, pos, edgelist=edges, ax=ax, width=1.5)
            # Gambar sisi ganda (garis melengkung)
            else:
                kelengkungan_awal = -0.2 * ((jumlah_sisi - 1) / 2)
                for i, edge in enumerate(edges):
                    kelengkungan = kelengkungan_awal + i * 0.2
                    nx.draw_networkx_edges(
                        self.graf,
                        pos,
                        edgelist=[edge],
                        ax=ax,
                        edge_color='gray',
                        width=1.5,
                        connectionstyle=f'arc3,rad={kelengkungan}'
                    )
        
        plt.title(judul, fontsize=16)
        plt.axis('off')
        plt.show()
        print("Visualisasi selesai ditampilkan.")

    # --- FUNGSI HAVEL-HAKIMI DIHAPUS ---
    # Fungsi ini tidak cocok untuk kasus multigraf dan menyebabkan error.
    # def _konstruksi_havel_hakimi(self, urutan_derajat):
    #     ...
    
    def _jalur_tanpa_syarat(self):
        """Opsi 1: Membuat graf dengan Model Konfigurasi (memungkinkan loop/sisi ganda)."""
        print("\n--- Opsi 1: Membuat Graf Tanpa Syarat Tambahan ---")
        
        # Buat 'stub' atau 'setengah-sisi' untuk setiap simpul sesuai derajatnya
        stubs = [node for node, deg in self.derajat.items() for _ in range(deg)]
        random.shuffle(stubs)
        
        # Pasangkan stub secara acak untuk membentuk sisi
        while len(stubs) > 1:
            u = stubs.pop()
            v = stubs.pop()
            self.graf.add_edge(u, v)
            
        self._visualisasikan("Graf Dibuat Tanpa Syarat (Bebas Loop/Sisi Ganda)")

    def _jalur_dengan_syarat(self):
        """Opsi 2: Membuat graf dengan syarat sisi ganda dan loop yang ditentukan."""
        print("\n--- Opsi 2: Membuat Graf Dengan Syarat ---")
        derajat_sisa = self.derajat.copy()
        
        # Input Sisi Ganda
        jml_sisi_ganda = self._dapatkan_input_integer("Masukkan jumlah sisi ganda yang ingin ditambahkan: ")
        for i in range(jml_sisi_ganda):
            while True:
                try:
                    pair_input = input(f"Sisi ganda ke-{i+1}: Masukkan 2 label simpul (cth: 1 2): ")
                    u, v = pair_input.strip().split()
                    if u in self.simpul and v in self.simpul and u != v:
                        # Periksa apakah derajat sisa mencukupi
                        if derajat_sisa[u] < 1 or derajat_sisa[v] < 1:
                            print("Derajat sisa tidak mencukupi untuk simpul ini. Coba lagi.")
                            continue
                        
                        self.graf.add_edge(u, v)
                        derajat_sisa[u] -= 1
                        derajat_sisa[v] -= 1
                        print(f"Sisi ganda ({u},{v}) ditambahkan. Sisa derajat {u}={derajat_sisa[u]}, {v}={derajat_sisa[v]}")
                        break
                    else:
                        print(f"Input tidak valid. Gunakan dua label simpul yang ada dan berbeda. (Simpul tersedia: 1 sampai {len(self.simpul)})")
                except ValueError:
                    print("Input error. Harap masukkan dua angka yang dipisahkan spasi. Coba lagi.")
        
        # Input Loop
        jml_loop = self._dapatkan_input_integer("Masukkan jumlah loop yang ingin ditambahkan: ")
        for i in range(jml_loop):
            while True:
                try:
                    node_input = input(f"Loop ke-{i+1}: Masukkan 1 label simpul: ").strip()
                    if node_input in self.simpul:
                        # Sebuah loop membutuhkan 2 derajat
                        if derajat_sisa[node_input] < 2:
                            print("Derajat sisa tidak mencukupi (butuh 2). Coba lagi.")
                            continue

                        self.graf.add_edge(node_input, node_input)
                        derajat_sisa[node_input] -= 2
                        print(f"Loop pada simpul {node_input} ditambahkan. Sisa derajat {node_input}={derajat_sisa[node_input]}")
                        break
                    else:
                        print(f"Label tidak valid. Gunakan angka dari 1 sampai {len(self.simpul)}.")
                except ValueError:
                    print("Input error. Harap masukkan satu angka. Coba lagi.")

        # === BAGIAN YANG DIPERBAIKI ===
        print("\nDerajat sisa yang perlu dipenuhi:", derajat_sisa)
        print("Melengkapi sisa graf menggunakan Model Konfigurasi...")

        # Gunakan Model Konfigurasi (seperti di Opsi 1) untuk sisa derajat
        # Ini adalah metode yang benar untuk multigraf
        stubs_sisa = [node for node, deg in derajat_sisa.items() for _ in range(deg)]
        random.shuffle(stubs_sisa)

        sisi_tambahan = []
        while len(stubs_sisa) > 1:
            u = stubs_sisa.pop()
            v = stubs_sisa.pop()
            sisi_tambahan.append((u,v))

        self.graf.add_edges_from(sisi_tambahan)
        print(f"{len(sisi_tambahan)} sisi tambahan berhasil dibuat untuk memenuhi sisa derajat.")
        
        self._visualisasikan("Graf Dibuat Dengan Syarat Loop dan Sisi Ganda")

    def jalankan(self):
        """Fungsi utama untuk menjalankan program."""
        print("===== Program Visualisasi Graf (Versi OOP) =====")
        jumlah_simpul = self._dapatkan_input_integer("Masukkan jumlah simpul: ", min_val=1)
        self.simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        self.graf.add_nodes_from(self.simpul)
        
        print("\n--- Input Derajat Simpul ---")
        for s in self.simpul:
            self.derajat[s] = self._dapatkan_input_integer(f"Masukkan derajat untuk Simpul {s}: ")
            
        if sum(self.derajat.values()) % 2 != 0:
            print("\n[Error] Jumlah total derajat ganjil. Graf tidak dapat dibuat.")
            print("================ Program Selesai ================")
            return
            
        print("\nPilih metode pembuatan graf:")
        print("1. Cetak tanpa syarat (bebas menggunakan loop atau sisi ganda)")
        print("2. Cetak menggunakan syarat (menentukan jumlah loop dan sisi ganda)")
        
        choice = ""
        while choice not in ['1', '2']:
            choice = input("Masukkan pilihan Anda (1 atau 2): ")
            
        if choice == '1':
            self._jalur_tanpa_syarat()
        else:
            self._jalur_dengan_syarat()
            
        print("\n================ Program Selesai ================")

if __name__ == '__main__':
    program_graf = VisualisasiGraf()
    program_graf.jalankan()