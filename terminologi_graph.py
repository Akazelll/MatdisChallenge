
import networkx as nx #menambah simpul dan sisi, menghitung jumlah derajat simpul yang di inisialkan nx
import matplotlib.pyplot as plt #untuk memvisualisasikan graph yang di input
import random #untuk memilih loop/sisi ganda secara acak 
from collections import defaultdict #untuk pengelompokkan sisi yang ganda dan loop untuk aksi jenis graph 
import itertools #menghasilakn simpul unik untuk graph yang bersyarat

import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict

class VisualisasiGraf:

    def __init__(self):

        #construktor default
        """Inisialisasi atribut kelas."""

        self.simpul = []
        self.derajat_awal = {}
        self.graf = nx.MultiGraph()

    def _dapatkan_input_integer(self, prompt, min_val=0):
        while True:
            try:
                value = int(input(prompt))
                if value >= min_val:
                    return value
                else:
                    print(f"Input harus >= {min_val}.")
            except ValueError:
                print("Input tidak valid. Harap masukkan angka.")

    def _visualisasikan(self, judul="Visualisasi Graf"):
        print("\nMencetak visualisasi...")

        pos = nx.spring_layout(self.graf, seed=42) #mengatur posisi setiap simpul 
        plt.figure(figsize=(12, 10)) #membuat kanvas gambar dengan ukuran tertentu lebar*tinggi
        ax = plt.gca() #mengambil sebagian kanvas untuk mengambbar
        
        nx.draw_networkx_nodes(self.graf, pos, ax=ax, node_color='skyblue', node_size=2500) # mengambar titik titik simpul 
        nx.draw_networkx_labels(self.graf, pos, ax=ax, font_size=12, font_weight='bold') #memberikan label di setiap simpulnya yg ada di tengah lingkaran
        
        # Validasi akhir derajat sebelum menggambar
        print("\n--- Verifikasi Derajat Akhir ---")
        derajat_sesuai = True
        for node in self.simpul: #loop simpul
            derajat_target = self.derajat_awal[node] #derajat yang di input
            derajat_aktual = self.graf.degree(node) #cek derajat apakah sama dengan yang di input atau tidak
            if derajat_target != derajat_aktual:
                print(f"Simpul {node}: Target Derajat={derajat_target}, Aktual={derajat_aktual} [TIDAK SESUAI]")

        pos = nx.spring_layout(self.graf, seed=42)
        plt.figure(figsize=(12, 10))
        ax = plt.gca()

        nx.draw_networkx_nodes(self.graf, pos, ax=ax, node_color='skyblue', node_size=2500)
        nx.draw_networkx_labels(self.graf, pos, ax=ax, font_size=12, font_weight='bold')

        print("\n--- Verifikasi Derajat Akhir ---")
        derajat_sesuai = True
        for node in self.simpul:
            target = self.derajat_awal[node]
            actual = self.graf.degree(node)
            if target != actual:
                print(f"Simpul {node}: Target={target}, Aktual={actual} [TIDAK SESUAI]")

                derajat_sesuai = False
            else:
                print(f"Simpul {node}: Target={target}, Aktual={actual} [OK]")

        if not derajat_sesuai:
            print("[Peringatan] Derajat akhir tidak sesuai dengan input awal!")
        else:
            print("Semua derajat akhir sesuai dengan input awal.")

        try:
            labels = {n: f'd={self.graf.degree(n)}' for n in self.graf.nodes()}
            label_pos = {k: (v[0], v[1] - 0.12) for k, v in pos.items()}
            nx.draw_networkx_labels(self.graf, label_pos, labels=labels, font_size=10, font_color='darkred')
        except Exception as e:
            print(f"Gagal menggambar label derajat: {e}")

        edge_groups = defaultdict(list)
        for u, v in self.graf.edges():
            edge_groups[tuple(sorted((u, v)))].append((u, v))

        for (u, v), edges in edge_groups.items():
            if u == v:
                for i, e in enumerate(edges):
                    rad = 0.1 + (i * 0.1)
                    nx.draw_networkx_edges(self.graf, pos, edgelist=[e], ax=ax, connectionstyle=f'arc3,rad={rad}')
            elif len(edges) <= 2:
                for i, e in enumerate(edges):
                    rad = -0.1 + i * 0.2
                    nx.draw_networkx_edges(self.graf, pos, edgelist=[e], ax=ax, connectionstyle=f'arc3,rad={rad}')

        plt.title(judul)
        plt.axis('off')
        plt.show()
        print("Visualisasi selesai ditampilkan.")

    def _jalur_tanpa_syarat(self):
        print("\n--- Membuat Graf Tanpa Syarat Tambahan (dengan batas sisi maksimal 2 per pasangan simpul) ---")
        stubs = [node for node, deg in self.derajat_awal.items() for _ in range(deg)]
        random.shuffle(stubs)
        edge_counts = defaultdict(int)

        while len(stubs) > 1:
            u = stubs.pop()
            v = stubs.pop()
            key = tuple(sorted((u, v)))


            if u == v or edge_counts[key] < 2:
                self.graf.add_edge(u, v)
                edge_counts[key] += 1
            else:
                stubs.extend([u, v])
                random.shuffle(stubs)

        self._visualisasikan("Graf Dibuat")


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
            # Untuk membuat sisi ganda antara dua simpul, keduanya harus punya sisa derajat minimal 2
            # Kita perlu membuat sebuah sisi normal (derajat -1 di tiap simpul) dan sisi kedua (derajat -1 lagi)
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
            
        # 4. Melengkapi Sisa Graf (Kunci Perbaikan)
        print("\nMelengkapi sisa graf untuk memenuhi derajat...")
        
        # Validasi akhir sebelum melengkapi
        if sum(derajat_sisa.values()) % 2 != 0:
            print("\n[Error] Sisa derajat ganjil setelah membuat syarat. Graf tidak dapat diselesaikan.")
            return
            
        # Buat 'stubs' atau 'koneksi terbuka' dari sisa derajat
        stubs_sisa = [node for node, deg in derajat_sisa.items() for _ in range(deg)]
        random.shuffle(stubs_sisa)
        
        # Hubungkan sisa stubs secara acak. Ini akan menghubungkan semua bagian graf
        # dan memastikan semua derajat terpenuhi.
        while len(stubs_sisa) > 1:
            u = stubs_sisa.pop()
            v = stubs_sisa.pop()
            
            # Cek untuk menghindari loop dan sisi ganda yang tidak diinginkan di tahap akhir
            # Jika hanya ada dua stubs tersisa dari simpul yang sama, loop tidak bisa dihindari.
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
        print("===== Program Visualisasi Graf =====")
        jumlah_simpul = self._dapatkan_input_integer("Masukkan jumlah simpul: ", min_val=1)
        self.simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        self.graf.add_nodes_from(self.simpul)

        print("\n--- Input Derajat Simpul ---")
        for s in self.simpul:
            self.derajat_awal[s] = self._dapatkan_input_integer(f"Derajat simpul {s}: ")

        if sum(self.derajat_awal.values()) % 2 != 0:
            print("[Error] Total derajat ganjil. Tidak bisa buat graf.")
            return

        self._jalur_tanpa_syarat()
        print("\n================ Program Selesai ================")

if __name__ == '__main__':
    program_graf = VisualisasiGraf()
    program_graf.jalankan()