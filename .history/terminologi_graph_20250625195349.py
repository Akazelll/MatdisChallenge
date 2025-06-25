import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict

class VisualisasiGraf:
    # ... (bagian __init__ dan _dapatkan_input_integer tetap sama persis) ...
    def __init__(self):
        self.simpul = []
        self.derajat = {}
        self.graf = nx.MultiGraph()

    def _dapatkan_input_integer(self, prompt, min_val=0):
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
        print("\nMencetak visualisasi...")
        pos = nx.spring_layout(self.graf, seed=42)
        plt.figure(figsize=(12, 10))
        ax = plt.gca()
        
        nx.draw_networkx_nodes(self.graf, pos, ax=ax, node_color='skyblue', node_size=2500)
        nx.draw_networkx_labels(self.graf, pos, ax=ax, font_size=12, font_weight='bold')
        try:
            derajat_labels = {node: f'd={degree}' for node, degree in self.graf.degree()}
            pos_derajat = {key: (value[0], value[1] - 0.12) for key, value in pos.items()}
            nx.draw_networkx_labels(self.graf, pos_derajat, ax=ax, labels=derajat_labels, font_size=10, font_color='darkred')
        except Exception as e:
            print(f"Tidak dapat menggambar label derajat: {e}")

        edge_groups = defaultdict(list)
        for u, v in self.graf.edges():
            edge_groups[tuple(sorted((u, v)))].append((u, v))

        for key, edges in edge_groups.items():
            u, v = key
            jumlah_sisi = len(edges)
            
            if u == v:
                nx.draw_networkx_edges(self.graf, pos, edgelist=edges, ax=ax, connectionstyle='arc3,rad=0.2')
                continue

            if jumlah_sisi == 1:
                nx.draw_networkx_edges(self.graf, pos, edgelist=edges, ax=ax, width=1.5)
            else:
                kelengkungan_awal = -0.2 * ((jumlah_sisi - 1) / 2)
                for i, edge in enumerate(edges):
                    kelengkungan = kelengkungan_awal + i * 0.2
                    nx.draw_networkx_edges(
                        self.graf, pos, edgelist=[edge], ax=ax,
                        edge_color='gray', width=1.5, connectionstyle=f'arc3,rad={kelengkungan}'
                    )
        
        plt.title(judul, fontsize=16)
        plt.axis('off')
        plt.show()
        print("Visualisasi selesai ditampilkan.")
    
    # --- PERUBAHAN DI SINI ---
    def _konstruksi_havel_hakimi(self, urutan_derajat):
        """
        Versi yang disempurnakan: Mengembalikan pesan error jika gagal.
        """
        # Buat daftar pasangan (derajat, nama_simpul) untuk diurutkan
        seq = sorted([(d, n) for n, d in urutan_derajat.items() if d > 0], reverse=True)
        
        # Jika tidak ada lagi yang perlu dihubungkan, berhasil
        if not seq: 
            return []
        
        # Jika ada derajat sisa negatif, mustahil
        if seq[-1][0] < 0: 
            return "Terjadi sisa derajat negatif setelah proses acak."

        # Ambil simpul dengan sisa derajat tertinggi
        (d, v) = seq.pop(0)

        # INI ADALAH PENGECEKAN KUNCI YANG SERING GAGAL
        if d > len(seq):
            # Kembalikan pesan error yang jelas, bukan hanya None
            return f"Sisa derajat untuk Simpul '{v}' ({d}) terlalu besar. Tidak bisa dihubungkan ke {len(seq)} simpul lainnya."

        # Lanjutkan proses seperti biasa...
        sisi = [(v, seq[i][1]) for i in range(d)]
        derajat_baru = {node: degree for degree, node in seq}
        for i in range(d):
            derajat_baru[seq[i][1]] -= 1
        
        # Panggil rekursif
        hasil_rekursif = self._konstruksi_havel_hakimi(derajat_baru)
        
        # Periksa hasil dari pemanggilan rekursif
        if isinstance(hasil_rekursif, str): # Jika hasilnya adalah pesan error
            return hasil_rekursif # Teruskan pesan error ke atas
        else:
            return sisi + hasil_rekursif # Gabungkan hasilnya jika berhasil
    
    # --- PERUBAHAN DI SINI ---
    def _jalur_dengan_syarat_otomatis(self):
        print("\n--- Opsi 2: Membuat Graf Dengan Syarat (Otomatis) ---")
        print("Program akan mencoba membangun graf secara acak sesuai syarat Anda.")

        derajat_sisa = self.derajat.copy()
        
        jml_loop = self._dapatkan_input_integer("Masukkan jumlah loop yang diinginkan: ")
        jml_sisi_ganda = self._dapatkan_input_integer("Masukkan jumlah sisi ganda yang diinginkan: ")

        # Tahap 1: Tempatkan loop secara acak
        loop_ditempatkan = []
        for _ in range(jml_loop):
            simpul_layak_loop = [s for s, d in derajat_sisa.items() if d >= 2]
            if not simpul_layak_loop:
                print("\n[GAGAL] Tidak dapat menempatkan loop. Tidak ada simpul dengan sisa derajat yang cukup.")
                return
            simpul_terpilih = random.choice(simpul_layak_loop)
            derajat_sisa[simpul_terpilih] -= 2
            loop_ditempatkan.append(simpul_terpilih)

        # Tahap 2: "Pesan" tempat untuk sisi ganda secara acak
        sisi_ganda_ditempatkan = []
        for _ in range(jml_sisi_ganda):
            simpul_layak_sisi = [s for s, d in derajat_sisa.items() if d >= 1]
            if len(simpul_layak_sisi) < 2:
                print("\n[GAGAL] Tidak dapat menempatkan sisi ganda. Tidak cukup simpul dengan sisa derajat.")
                return
            u, v = random.sample(simpul_layak_sisi, 2)
            derajat_sisa[u] -= 1
            derajat_sisa[v] -= 1
            sisi_ganda_ditempatkan.append((u, v))
            
        print("\nDerajat sisa yang akan dibentuk menjadi graf sederhana:", derajat_sisa)
        
        # Tahap 3: Bangun graf dasar dan tangani pesan errornya
        hasil_konstruksi = self._konstruksi_havel_hakimi(derajat_sisa)

        # Periksa apakah hasilnya adalah pesan error (string) atau daftar sisi (list)
        if isinstance(hasil_konstruksi, str):
            print("\n[GAGAL] Kombinasi syarat yang diberikan tidak memungkinkan untuk membentuk graf.")
            print(f"Alasan Spesifik: {hasil_konstruksi}") # Cetak pesan error yang jelas
            return

        # Tahap 4: Gabungkan semua bagian jika berhasil
        self.graf.add_edges_from(hasil_konstruksi)
        for simpul_loop in loop_ditempatkan:
            self.graf.add_edge(simpul_loop, simpul_loop)
        self.graf.add_edges_from(sisi_ganda_ditempatkan)
        
        print("\n[BERHASIL] Graf berhasil dibuat secara otomatis!")
        self._visualisasikan("Graf Dibuat Dengan Syarat (Otomatis)")

    # ... (Metode jalankan dan _jalur_tanpa_syarat tetap sama) ...
    def jalankan(self):
        print("===== Program Visualisasi Graf (Versi OOP) =====")
        jumlah_simpul = self._dapatkan_input_integer("Masukkan jumlah simpul: ", min_val=1)
        self.simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        self.graf.add_nodes_from(self.simpul)
        print("\n--- Input Derajat Simpul ---")
        for s in self.simpul:
            self.derajat[s] = self._dapatkan_input_integer(f"Masukkan derajat untuk Simpul {s}: ")
        if sum(self.derajat.values()) % 2 != 0:
            print("\n[Error] Jumlah total derajat ganjil. Graf tidak dapat dibuat.")
            print("Finish")
            return
            
        print("\nPilih metode pembuatan graf:")
        print("1. Cetak tanpa syarat (bebas menggunakan loop atau sisi ganda)")
        print("2. Cetak menggunakan syarat (otomatis berdasarkan jumlah loop & sisi ganda)")
        choice = ""
        while choice not in ['1', '2']:
            choice = input("Masukkan pilihan Anda (1 atau 2): ")
            
        if choice == '1':
            self._jalur_tanpa_syarat()
        else:
            self._jalur_dengan_syarat_otomatis()
            
        print("\nFinish")
        print("================ Program Selesai ================")


if __name__ == '__main__':
    program_graf = VisualisasiGraf()
    program_graf.jalankan()