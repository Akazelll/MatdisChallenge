import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict
import itertools

class VisualisasiGraf:
    """
    Kelas untuk membuat dan memvisualisasikan graf berdasarkan input derajat dari pengguna.
    Mendukung pembuatan graf acak dan graf dengan jumlah loop serta sisi ganda yang ditentukan.
    """

    def __init__(self):
        """Inisialisasi atribut kelas."""
        self.simpul = []
        self.derajat_awal = {}
        self.graf = nx.MultiGraph()

    def _dapatkan_input_integer(self, prompt, min_val=0):
        """Mendapatkan input integer yang valid dari pengguna."""
        while True:
            try:
                value = int(input(prompt))
                if value >= min_val:
                    return value
                else:
                    print(f"Input harus berupa bilangan bulat (>= {min_val}). Coba lagi.")
            except ValueError:
                print("Input tidak valid. Harap masukkan sebuah angka.")

    def _visualisasikan(self, judul="Visualisasi Graf"):
        """Mencetak visualisasi graf menggunakan matplotlib dan networkx."""
        print("\nMencetak visualisasi...")
        pos = nx.spring_layout(self.graf, seed=42)
        plt.figure(figsize=(12, 10))
        ax = plt.gca()
        
        nx.draw_networkx_nodes(self.graf, pos, ax=ax, node_color='skyblue', node_size=2500)
        nx.draw_networkx_labels(self.graf, pos, ax=ax, font_size=12, font_weight='bold')
        
        # Validasi akhir derajat sebelum menggambar
        print("\n--- Verifikasi Derajat Akhir ---")
        derajat_sesuai = True
        for node in self.simpul:
            derajat_target = self.derajat_awal[node]
            derajat_aktual = self.graf.degree(node)
            if derajat_target != derajat_aktual:
                print(f"Simpul {node}: Target Derajat={derajat_target}, Aktual={derajat_aktual} [TIDAK SESUAI]")
                derajat_sesuai = False
            else:
                print(f"Simpul {node}: Target Derajat={derajat_target}, Aktual={derajat_aktual} [OK]")

        if not derajat_sesuai:
            print("\n[Peringatan] Ada derajat akhir yang tidak sesuai dengan input awal!")
        else:
            print("\nSemua derajat akhir sesuai dengan input awal.")

        # Menambahkan label derajat di bawah simpul
        try:
            derajat_labels = {node: f'd={degree}' for node, degree in self.graf.degree()}
            pos_derajat = {key: (value[0], value[1] - 0.12) for key, value in pos.items()}
            nx.draw_networkx_labels(self.graf, pos_derajat, ax=ax, labels=derajat_labels, font_size=10, font_color='darkred')
        except Exception as e:
            print(f"Tidak dapat menggambar label derajat: {e}")

        # Mengelompokkan sisi untuk menggambar sisi ganda dan loop dengan benar
        edge_groups = defaultdict(list)
        for u, v in self.graf.edges():
            edge_groups[tuple(sorted((u, v)))].append((u, v))

        for key, edges in edge_groups.items():
            u, v = key
            jumlah_sisi = len(edges)
            
            if u == v: # Menggambar loop
                for i, edge in enumerate(edges):
                    rad = 0.1 + (i * 0.1)
                    nx.draw_networkx_edges(self.graf, pos, edgelist=[edge], ax=ax,
                                           connectionstyle=f'arc3,rad={rad}', arrowstyle='-')
                continue

            if jumlah_sisi == 1: # Sisi tunggal
                nx.draw_networkx_edges(self.graf, pos, edgelist=edges, ax=ax, width=1.5)
            else: # Sisi ganda
                kelengkungan_awal = -0.2 * ((jumlah_sisi - 1) / 2)
                for i, edge in enumerate(edges):
                    kelengkungan = kelengkungan_awal + i * 0.2
                    nx.draw_networkx_edges(
                        self.graf, pos, edgelist=[edge], ax=ax, edge_color='gray',
                        width=1.5, connectionstyle=f'arc3,rad={kelengkungan}'
                    )
        
        plt.title(judul, fontsize=16)
        plt.axis('off')
        plt.show()
        print("Visualisasi selesai ditampilkan.")

    def _jalur_tanpa_syarat(self):
        """Opsi 1: Membuat graf dengan Model Konfigurasi (memungkinkan loop/sisi ganda acak)."""
        print("\n--- Opsi 1: Membuat Graf Tanpa Syarat Tambahan ---")
        stubs = [node for node, deg in self.derajat_awal.items() for _ in range(deg)]
        random.shuffle(stubs)
        
        while len(stubs) > 1:
            u = stubs.pop()
            v = stubs.pop()
            self.graf.add_edge(u, v)
            
        self._visualisasikan("Graf Dibuat Tanpa Syarat (Bebas Loop/Sisi Ganda)")

    def _jalur_dengan_syarat_otomatis(self):
        """Opsi 2 (DIPERBAIKI): Membuat graf dengan jumlah loop/sisi ganda yang ditentukan."""
        print("\n--- Opsi 2: Membuat Graf Dengan Syarat (Otomatis) ---")
        
        derajat_sisa = self.derajat_awal.copy()
        
        # 1. Input Jumlah Loop dan Sisi Ganda
        target_loop = self._dapatkan_input_integer("Masukkan jumlah loop yang diinginkan: ")
        target_sisi_ganda = self._dapatkan_input_integer("Masukkan jumlah sisi ganda yang diinginkan: ")

        # 2. Proses Pembuatan Loop
        print("\nMembuat loop...")
        loop_dibuat = 0
        for _ in range(target_loop):
            # Cari simpul yang masih memiliki sisa derajat minimal 2 untuk membuat loop
            kandidat_loop = [node for node, deg in derajat_sisa.items() if deg >= 2]
            if not kandidat_loop:
                print(f"[Peringatan] Tidak dapat membuat loop ke-{loop_dibuat + 1}. Simpul dengan sisa derajat >= 2 tidak cukup.")
                break
            
            # Pilih simpul secara acak, buat loop, dan kurangi sisa derajatnya
            pilihan_simpul = random.choice(kandidat_loop)
            self.graf.add_edge(pilihan_simpul, pilihan_simpul)
            derajat_sisa[pilihan_simpul] -= 2
            loop_dibuat += 1
            print(f"Loop ke-{loop_dibuat} dibuat pada simpul {pilihan_simpul}.")

        if loop_dibuat < target_loop:
            print(f"\n[Error] Gagal membuat loop sesuai target. Target: {target_loop}, Dibuat: {loop_dibuat}.")
            return

        # 3. Proses Pembuatan Sisi Ganda
        print("\nMembuat sisi ganda...")
        sisi_ganda_dibuat = 0
        for _ in range(target_sisi_ganda):
            # Untuk membuat sisi ganda, kita butuh dua simpul berbeda yang keduanya punya sisa derajat minimal 2
            kandidat_pasangan = list(itertools.combinations([n for n, d in derajat_sisa.items() if d >= 2], 2))
            
            if not kandidat_pasangan:
                print(f"[Peringatan] Tidak bisa membuat sisi ganda ke-{sisi_ganda_dibuat + 1}. Pasangan simpul dengan sisa derajat >= 2 tidak cukup.")
                break
            
            # Pilih pasangan simpul, buat 2 sisi di antara mereka, kurangi sisa derajat
            u, v = random.choice(kandidat_pasangan)
            self.graf.add_edge(u, v)
            self.graf.add_edge(u, v)
            derajat_sisa[u] -= 2
            derajat_sisa[v] -= 2
            sisi_ganda_dibuat += 1
            print(f"Sisi ganda ke-{sisi_ganda_dibuat} dibuat antara simpul {u} dan {v}.")

        if sisi_ganda_dibuat < target_sisi_ganda:
            print(f"\n[Error] Gagal membuat sisi ganda sesuai target. Target: {target_sisi_ganda}, Dibuat: {sisi_ganda_dibuat}.")
            return
            
        # 4. Melengkapi Sisa Graf
        print("\nMelengkapi sisa graf untuk memenuhi derajat...")
        
        # Validasi akhir sebelum melengkapi
        if sum(derajat_sisa.values()) % 2 != 0:
            print("\n[Error] Sisa derajat ganjil setelah membuat syarat. Graf tidak dapat diselesaikan.")
            return
            
        # Buat 'stubs' (koneksi terbuka) dari sisa derajat
        stubs_sisa = [node for node, deg in derajat_sisa.items() for _ in range(deg)]
        random.shuffle(stubs_sisa)
        
        # Hubungkan sisa stubs secara acak untuk memenuhi sisa derajat
        while len(stubs_sisa) > 1:
            u = stubs_sisa.pop()
            v = stubs_sisa.pop()
            
            # Coba hindari membuat loop baru di tahap akhir jika memungkinkan
            max_attempts = 10
            attempt = 0
            while u == v and len(stubs_sisa) > 0 and attempt < max_attempts:
                stubs_sisa.append(v)
                random.shuffle(stubs_sisa)
                v = stubs_sisa.pop()
                attempt += 1

            self.graf.add_edge(u, v)
        
        if stubs_sisa:
            print(f"[Peringatan] Sisa satu stub yang tidak terhubung: {stubs_sisa[0]}. Derajat tidak akan terpenuhi.")
            
        self._visualisasikan("Graf Dibuat Dengan Syarat (Derajat Terpenuhi)")

    def jalankan(self):
        """Fungsi utama untuk menjalankan program."""
        print("===== Program Visualisasi Graf Berdasarkan Derajat =====")
        jumlah_simpul = self._dapatkan_input_integer("Masukkan jumlah simpul: ", min_val=1)
        self.simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        self.graf.add_nodes_from(self.simpul)
        
        print("\n--- Input Derajat Simpul ---")
        total_derajat = 0
        while True:
            derajat_sementara = {}
            for s in self.simpul:
                derajat_sementara[s] = self._dapatkan_input_integer(f"Masukkan derajat untuk Simpul {s}: ")
            
            total_derajat = sum(derajat_sementara.values())
            if total_derajat % 2 == 0:
                self.derajat_awal = derajat_sementara
                break
            else:
                print(f"\n[Error] Jumlah total derajat ganjil ({total_derajat}). Graf tidak dapat dibuat. Silakan ulangi input.")
        
        print("\nPilih metode pembuatan graf:")
        print("1. Cetak tanpa syarat (sepenuhnya acak)")
        print("2. Cetak dengan syarat (menentukan jumlah loop & sisi ganda)")
        
        choice = ""
        while choice not in ['1', '2']:
            choice = input("Masukkan pilihan Anda (1 atau 2): ")
            
        if choice == '1':
            self._jalur_tanpa_syarat()
        else:
            self._jalur_dengan_syarat_otomatis()
            
        print("\n================ Program Selesai ================")

if __name__ == '__main__':
    program_graf = VisualisasiGraf()
    program_graf.jalankan()