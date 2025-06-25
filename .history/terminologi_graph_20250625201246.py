import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict

class VisualisasiGraf:
    
    # __init__, _dapatkan_input_integer, _visualisasikan, _jalur_tanpa_syarat
    # tetap sama persis seperti kode sebelumnya.
    # Saya akan menyertakannya di sini agar kode lengkap.

    def __init__(self):
        """Inisialisasi atribut kelas."""
        self.simpul = []
        self.derajat = {}
        self.graf = nx.MultiGraph()

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
                nx.draw_networkx_edges(self.graf, pos, edgelist=edges, ax=ax, connectionstyle='arc3,rad=0.2', arrowstyle='-')
                continue

            if jumlah_sisi == 1:
                nx.draw_networkx_edges(self.graf, pos, edgelist=edges, ax=ax, width=1.5)
            else:
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
        """Opsi 1: Membuat graf dengan Model Konfigurasi (sepenuhnya acak)."""
        print("\n--- Opsi 1: Membuat Graf Tanpa Syarat Tambahan ---")
        stubs = [node for node, deg in self.derajat.items() for _ in range(deg)]
        random.shuffle(stubs)
        while len(stubs) > 1:
            u = stubs.pop()
            v = stubs.pop()
            self.graf.add_edge(u, v)
        self._visualisasikan("Graf Dibuat Tanpa Syarat (Bebas Loop/Sisi Ganda)")
    
    # === FUNGSI BARU UNTUK OPSI 2 (VERSI PRESISI) ===
    def _jalur_dengan_syarat_tepat(self):
        """Opsi 2 (Presisi): Membuat graf dengan JUMLAH TEPAT loop/sisi ganda."""
        print("\n--- Opsi 2: Membuat Graf Dengan Syarat Tepat ---")
        derajat_sisa = self.derajat.copy()

        # 1. Input jumlah yang diinginkan
        jml_loop = self._dapatkan_input_integer("Masukkan jumlah TEPAT loop yang diinginkan: ")
        jml_sisi_ganda = self._dapatkan_input_integer("Masukkan jumlah TEPAT sisi ganda yang diinginkan: ")
        
        # 2. Membuat loop secara acak (sama seperti sebelumnya)
        print("\nMembuat loop yang disyaratkan...")
        for i in range(jml_loop):
            kandidat_loop = [node for node, deg in derajat_sisa.items() if deg >= 2]
            if not kandidat_loop:
                print(f"[Error] Tidak dapat membuat graf. Gagal saat membuat loop ke-{i+1} karena tidak ada simpul dengan sisa derajat >= 2.")
                return
            pilihan_simpul = random.choice(kandidat_loop)
            self.graf.add_edge(pilihan_simpul, pilihan_simpul)
            derajat_sisa[pilihan_simpul] -= 2
            print(f"Loop ke-{i+1} dibuat pada simpul {pilihan_simpul}.")

        # 3. Membuat sisi ganda secara acak (sama seperti sebelumnya)
        print("\nMembuat sisi ganda yang disyaratkan...")
        for i in range(jml_sisi_ganda):
            kandidat_sisi = [node for node, deg in derajat_sisa.items() if deg >= 1]
            if len(kandidat_sisi) < 2:
                print(f"[Error] Tidak dapat membuat graf. Gagal saat membuat sisi ganda ke-{i+1} karena kurang dari 2 simpul dengan sisa derajat.")
                return
            u, v = random.sample(kandidat_sisi, 2)
            self.graf.add_edge(u, v)
            derajat_sisa[u] -= 1
            derajat_sisa[v] -= 1
            print(f"Sisi ganda ke-{i+1} dibuat antara simpul {u} dan {v}.")

        # 4. Melengkapi sisa graf menjadi GRAF SEDERHANA (TIDAK ADA LOOP/SISI GANDA BARU)
        print("\nMelengkapi sisa graf (tanpa membuat loop/sisi ganda baru)...")
        stubs_sisa = [node for node, deg in derajat_sisa.items() for _ in range(deg)]
        
        # Panggil helper function dengan metode "Coba dan Uji"
        if self._lengkapi_graf_sederhana(stubs_sisa):
            self._visualisasikan("Graf Dibuat Dengan Syarat Tepat")
        else:
            print("\n[ERROR FATAL] Gagal membuat graf.")
            print("Setelah banyak percobaan, tidak ditemukan cara untuk menghubungkan sisa derajat")
            print("tanpa membuat loop atau sisi ganda baru yang tidak diinginkan.")
            print("Coba lagi dengan kombinasi derajat atau syarat yang berbeda.")

    def _lengkapi_graf_sederhana(self, stubs_sisa):
        """
        Helper function untuk menghubungkan sisa stubs menjadi graf sederhana.
        Menggunakan metode "Coba dan Uji" dengan batas percobaan.
        """
        # Batas percobaan untuk mencegah program mogok
        MAKS_PERCOBAAN = 2000 
        
        for percobaan in range(MAKS_PERCOBAAN):
            pasangan_valid = True
            sisi_baru = []
            
            # Selalu bekerja dengan salinan agar daftar asli tidak rusak
            stubs_sementara = list(stubs_sisa)
            random.shuffle(stubs_sementara)
            
            # Cek apakah pairing saat ini valid
            if len(stubs_sementara) % 2 != 0: # Seharusnya tidak pernah terjadi, tapi untuk keamanan
                return False 

            temp_graf = self.graf.copy()
            while len(stubs_sementara) > 1:
                u = stubs_sementara.pop()
                v = stubs_sementara.pop()
                
                # Kondisi GAGAL:
                # 1. Jika membentuk loop baru
                # 2. Jika membentuk sisi ganda baru (sudah ada di graf)
                if u == v or temp_graf.has_edge(u, v):
                    pasangan_valid = False
                    break # Hentikan pengecekan untuk percobaan ini, coba lagi dari awal
                
                # Jika valid, tambahkan ke graf sementara untuk pengecekan selanjutnya
                temp_graf.add_edge(u,v)
                sisi_baru.append((u, v))

            # Jika seluruh pasangan dalam percobaan ini valid
            if pasangan_valid:
                print(f"Berhasil menemukan kombinasi valid setelah {percobaan + 1} percobaan.")
                self.graf.add_edges_from(sisi_baru)
                return True # Sukses!

        # Jika loop selesai tanpa menemukan solusi
        return False # Gagal

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
        print("1. Cetak tanpa syarat (sepenuhnya acak)")
        print("2. Cetak dengan syarat TEPAT (jumlah loop & sisi ganda ditentukan)")
        
        choice = ""
        while choice not in ['1', '2']:
            choice = input("Masukkan pilihan Anda (1 atau 2): ")
            
        if choice == '1':
            self._jalur_tanpa_syarat()
        else:
            self._jalur_dengan_syarat_tepat() # Panggil fungsi presisi yang baru
            
        print("\n================ Program Selesai ================")

if __name__ == '__main__':
    program_graf = VisualisasiGraf()
    program_graf.jalankan()