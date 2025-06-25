import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict
import itertools

class VisualisasiGraf:
    
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
            # Urutkan simpul agar (A,B) dan (B,A) dianggap sama
            edge_groups[tuple(sorted((u, v)))].append((u, v))

        for key, edges in edge_groups.items():
            u, v = key
            jumlah_sisi = len(edges)
            
            # Gambar loop (sisi ke diri sendiri)
            if u == v:
                # Menggambar beberapa loop pada simpul yang sama dengan radius berbeda
                for i, edge in enumerate(edges):
                    rad = 0.1 + (i * 0.1)
                    nx.draw_networkx_edges(self.graf, pos, edgelist=[edge], ax=ax, 
                                           connectionstyle=f'arc3,rad={rad}', arrowstyle='-')
                continue

            # Gambar sisi tunggal
            if jumlah_sisi == 1:
                nx.draw_networkx_edges(self.graf, pos, edgelist=edges, ax=ax, width=1.5)
            # Gambar sisi ganda
            else:
                # Atur kelengkungan agar sisi ganda terlihat jelas dan tidak tumpang tindih
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
        # Membuat 'stubs' (titik koneksi) untuk setiap simpul sesuai derajatnya
        stubs = [node for node, deg in self.derajat_awal.items() for _ in range(deg)]
        random.shuffle(stubs)
        
        # Menghubungkan stubs secara acak
        while len(stubs) > 1:
            u = stubs.pop()
            v = stubs.pop()
            self.graf.add_edge(u, v)
            
        self._visualisasikan("Graf Dibuat Tanpa Syarat (Bebas Loop/Sisi Ganda)")

    # === FUNGSI BARU YANG DI-IMPROVE (OTOMATIS DAN TERVALIDASI) ===
    def _jalur_dengan_syarat_otomatis(self):
        """Opsi 2 (Baru): Membuat graf dengan jumlah loop/sisi ganda yg ditentukan secara otomatis."""
        print("\n--- Opsi 2: Membuat Graf Dengan Syarat (Otomatis) ---")
        
        derajat_sisa = self.derajat_awal.copy()
        simpul_tersedia = list(self.simpul)
        
        # 1. Input jumlah loop dan sisi ganda yang diinginkan
        target_loop = self._dapatkan_input_integer("Masukkan jumlah loop yang diinginkan: ")
        target_sisi_ganda = self._dapatkan_input_integer("Masukkan jumlah sisi ganda yang diinginkan: ")

        # 2. Validasi Awal (SANGAT PENTING)
        # Cek apakah permintaan bisa dipenuhi oleh total derajat yang ada
        total_derajat_dibutuhkan = (target_loop * 2) + (target_sisi_ganda * 4)
        if sum(derajat_sisa.values()) < total_derajat_dibutuhkan:
            print(f"\n[Error] Tidak cukup derajat untuk membuat {target_loop} loop dan {target_sisi_ganda} sisi ganda.")
            print(f"Total derajat tersedia: {sum(derajat_sisa.values())}")
            print(f"Total derajat dibutuhkan untuk syarat: {total_derajat_dibutuhkan}")
            return

        # 3. Membuat Loop (Proses yang Dijamin)
        print("\nMembuat loop secara acak...")
        loop_dibuat = 0
        for i in range(target_loop):
            # Cari simpul yang bisa dibuatkan loop (sisa derajat >= 2)
            kandidat_loop = [node for node, deg in derajat_sisa.items() if deg >= 2]
            if not kandidat_loop:
                print(f"Peringatan: Berhenti pada loop ke-{i+1}. Tidak ada lagi simpul dengan sisa derajat >= 2.")
                break
            
            pilihan_simpul = random.choice(kandidat_loop)
            self.graf.add_edge(pilihan_simpul, pilihan_simpul)
            derajat_sisa[pilihan_simpul] -= 2
            loop_dibuat += 1
            print(f"Loop ke-{loop_dibuat} dibuat pada simpul {pilihan_simpul}.")

        if loop_dibuat != target_loop:
            print(f"\n[Error] Gagal membuat jumlah loop sesuai target. Target: {target_loop}, Dibuat: {loop_dibuat}.")
            return

        # 4. Membuat Sisi Ganda (Proses yang Dijamin)
        print("\nMembuat sisi ganda secara acak...")
        sisi_ganda_dibuat = 0
        for i in range(target_sisi_ganda):
            # Untuk membuat sisi ganda antara u dan v, masing-masing butuh 2 derajat.
            # Kita cari semua pasangan (u,v) yang memenuhi syarat.
            # Syarat: u != v, derajat_sisa[u] >= 1, derajat_sisa[v] >= 1
            
            # Cari semua pasang simpul yang mungkin
            kandidat_pasangan = list(itertools.combinations([n for n, d in derajat_sisa.items() if d >= 1], 2))
            
            if not kandidat_pasangan:
                print(f"Peringatan: Berhenti pada sisi ganda ke-{i+1}. Tidak ada pasangan simpul yang valid.")
                break
            
            # Pilih satu pasangan secara acak
            u, v = random.choice(kandidat_pasangan)
            
            # Tambahkan DUA sisi antara u dan v untuk membuat sisi ganda
            self.graf.add_edge(u, v)
            self.graf.add_edge(u, v)
            derajat_sisa[u] -= 2
            derajat_sisa[v] -= 2
            sisi_ganda_dibuat += 1
            print(f"Sisi ganda ke-{sisi_ganda_dibuat} dibuat antara simpul {u} dan {v}.")

        if sisi_ganda_dibuat != target_sisi_ganda:
            print(f"\n[Error] Gagal membuat jumlah sisi ganda sesuai target. Target: {target_sisi_ganda}, Dibuat: {sisi_ganda_dibuat}.")
            return
            
        # 5. Melengkapi Sisa Graf (Menghindari Loop/Sisi Ganda baru)
        print("\nMelengkapi sisa graf untuk memenuhi derajat...")
        
        # Cek apakah sisa stubs bisa dihubungkan
        if sum(derajat_sisa.values()) % 2 != 0:
            print("\n[Error] Sisa derajat ganjil setelah membuat loop/sisi ganda. Graf tidak dapat diselesaikan.")
            print("Coba kombinasi input yang berbeda.")
            return
            
        stubs_sisa = [node for node, deg in derajat_sisa.items() for _ in range(deg)]
        random.shuffle(stubs_sisa)

        while len(stubs_sisa) > 1:
            u = stubs_sisa.pop(0)
            
            # Cari pasangan v yang valid untuk u
            pasangan_ditemukan = False
            for j in range(len(stubs_sisa)):
                v = stubs_sisa[j]
                # Syarat: tidak membuat loop baru (u!=v) dan tidak membuat sisi ganda baru
                if u != v and not self.graf.has_edge(u, v):
                    stubs_sisa.pop(j) # Ambil v dari list
                    self.graf.add_edge(u, v)
                    pasangan_ditemukan = True
                    break
            
            if not pasangan_ditemukan:
                # Jika 'terjebak' (misal sisa stubs A, B, B, C dan A-C sudah ada),
                # sulit diselesaikan tanpa algoritma kompleks (edge-swapping).
                # Untuk kasus ini, kita hentikan dan beri pesan.
                print("\n[Peringatan] Tidak dapat menghubungkan sisa graf tanpa membuat loop/sisi ganda baru.")
                print("Graf mungkin tidak lengkap sesuai derajat awal. Visualisasi menunjukkan kondisi saat ini.")
                break

        self._visualisasikan("Graf Dibuat Dengan Syarat (Loop & Sisi Ganda Terkontrol)")

    def jalankan(self):
        """Fungsi utama untuk menjalankan program."""
        print("===== Program Visualisasi Graf (Versi OOP) =====")
        jumlah_simpul = self._dapatkan_input_integer("Masukkan jumlah simpul: ", min_val=1)
        self.simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        self.graf.add_nodes_from(self.simpul)
        
        print("\n--- Input Derajat Simpul ---")
        for s in self.simpul:
            self.derajat_awal[s] = self._dapatkan_input_integer(f"Masukkan derajat untuk Simpul {s}: ")
            
        # Validasi utama: Jumlah total derajat harus genap
        if sum(self.derajat_awal.values()) % 2 != 0:
            print("\n[Error] Jumlah total derajat ganjil. Graf tidak dapat dibuat.")
            print("================ Program Selesai ================")
            return
            
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