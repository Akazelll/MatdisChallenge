import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import Counter

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
        print("\n🎨 Mencetak visualisasi...")
        pos = nx.spring_layout(self.graf, seed=42)
        plt.figure(figsize=(12, 10))
        ax = plt.gca()
        
        nx.draw_networkx_nodes(self.graf, pos, ax=ax, node_color='skyblue', node_size=2500)
        nx.draw_networkx_labels(self.graf, pos, ax=ax, font_size=12, font_weight='bold')
        
        print("\n--- Verifikasi Derajat Akhir ---")
        derajat_sesuai = all(self.derajat_awal[n] == self.graf.degree(n) for n in self.simpul)

        if derajat_sesuai:
            print("✅ Semua derajat akhir DIJAMIN sesuai dengan input awal.")
        else:
            # Blok ini seharusnya tidak pernah tercapai dengan logika baru
            print("❌ PERINGATAN: Ada derajat yang tidak sesuai. Ini adalah bug.")

        try:
            derajat_labels = {node: f'd={degree}' for node, degree in self.graf.degree()}
            pos_derajat = {key: (value[0], value[1] - 0.12) for key, value in pos.items()}
            nx.draw_networkx_labels(self.graf, pos_derajat, ax=ax, labels=derajat_labels, font_size=10, font_color='darkred')
        except Exception as e:
            print(f"Tidak dapat menggambar label derajat: {e}")

        # Visualisasi sisi ganda dan loop yang lebih rapi
        for u, v, data in self.graf.edges(data=True):
            # Cek duplikat agar tidak digambar dua kali
            if u > v: continue
            
            edges = self.graf.get_edge_data(u, v)
            if u == v: # Loop
                for i in range(len(edges)):
                    rad = 0.1 + (i * 0.1)
                    nx.draw_networkx_edges(self.graf, pos, edgelist=[(u, v)], ax=ax,
                                           connectionstyle=f'arc3,rad={rad}', arrowstyle='-')
            elif len(edges) == 1: # Sisi tunggal
                nx.draw_networkx_edges(self.graf, pos, edgelist=[(u,v)], ax=ax, width=1.5)
            else: # Sisi ganda
                rad = 0.15
                nx.draw_networkx_edges(self.graf, pos, edgelist=[(u,v)], ax=ax, width=1.5,
                                       connectionstyle=f'arc3,rad={rad}')
                nx.draw_networkx_edges(self.graf, pos, edgelist=[(u,v)], ax=ax, width=1.5,
                                       connectionstyle=f'arc3,rad={-rad}')

        plt.title(judul, fontsize=16)
        plt.axis('off')
        plt.show()
        print("Visualisasi selesai ditampilkan.")

    def _buat_dan_visualisasikan_graf(self):
        """
        Membuat graf dari barisan derajat dengan metode Havel-Hakimi yang dimodifikasi.
        Metode ini menjamin derajat terpenuhi dan meminimalkan sisi ganda > 2.
        """
        print("\n⚙️ Memulai pembuatan graf dengan metode Havel-Hakimi yang dimodifikasi...")
        
        # 1. Inisialisasi: Gunakan Counter untuk melacak sisa derajat
        sisa_derajat = Counter(self.derajat_awal)
        
        # Urutkan simpul dari derajat tertinggi ke terendah
        simpul_urut = sorted(sisa_derajat, key=sisa_derajat.get, reverse=True)
        
        # 2. Proses Pairing Terkontrol (Havel-Hakimi)
        for u in simpul_urut:
            # Hubungkan simpul 'u' ke simpul lain dengan derajat tertinggi
            while sisa_derajat[u] > 0:
                sisa_derajat[u] -= 1
                
                # Cari partner 'v' terbaik: derajat tertinggi, bukan diri sendiri, dan belum punya 2 sisi
                kandidat_v = sorted(
                    (v for v in sisa_derajat if sisa_derajat[v] > 0 and u != v),
                    key=lambda v: (self.graf.number_of_edges(u, v), -sisa_derajat.get(v, 0))
                )
                
                # Jika ada kandidat yang belum punya 2 sisi, pilih itu
                partner_ditemukan = False
                for v in kandidat_v:
                    if self.graf.number_of_edges(u, v) < 2:
                        self.graf.add_edge(u, v)
                        sisa_derajat[v] -= 1
                        partner_ditemukan = True
                        break
                
                if not partner_ditemukan:
                    # Jika semua kandidat sudah punya 2 sisi, terpaksa hubungkan ke salah satunya
                    # Ini jarang terjadi, tapi penting untuk menjamin derajat
                    if kandidat_v:
                        v = kandidat_v[0] # Ambil yang derajatnya paling tinggi
                        self.graf.add_edge(u, v)
                        sisa_derajat[v] -= 1
                    else:
                        # Jika tidak ada kandidat sama sekali (misal sisa derajat u=1, lainnya 0),
                        # kita pasangkan sebagai loop (jika memungkinkan)
                        if sisa_derajat[u] >= 1 and self.graf.number_of_edges(u,u) < 2:
                             self.graf.add_edge(u, u)
                             sisa_derajat[u] -= 1
                        else:
                             # Stub yang tidak bisa dipasangkan, akan ditangani di langkah 3
                             sisa_derajat[u] += 1 # Kembalikan derajat yang gagal dipasangkan
                             break
        
        # 3. Finalisasi: Hubungkan sisa stub (jika ada) untuk menjamin derajat
        stubs_sisa = [n for n, d in sisa_derajat.items() for _ in range(d)]
        if stubs_sisa:
            print(f"🔗 Menghubungkan {len(stubs_sisa)} sisa 'stub' untuk memastikan semua derajat sesuai...")
            random.shuffle(stubs_sisa)
            while len(stubs_sisa) > 1:
                u = stubs_sisa.pop()
                v = stubs_sisa.pop()
                self.graf.add_edge(u, v)
        
        self._visualisasikan("Graf Final (Derajat Dijamin Sesuai)")

    def jalankan(self):
        """Fungsi utama untuk menjalankan program."""
        print("===== Program Visualisasi Graf (Versi Final) =====")
        jumlah_simpul = self._dapatkan_input_integer("Masukkan jumlah simpul: ", min_val=1)
        self.simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        
        print("\n--- Input Derajat Simpul ---")
        for s in self.simpul:
            self.derajat_awal[s] = self._dapatkan_input_integer(f"Masukkan derajat untuk Simpul {s}: ")
            
        if sum(self.derajat_awal.values()) % 2 != 0:
            print("\n[Error] Jumlah total derajat ganjil. Graf tidak dapat dibuat.")
            print("================ Program Selesai ================")
            return
            
        self._buat_dan_visualisasikan_graf()
            
        print("\n================ Program Selesai ================")

if __name__ == '__main__':
    program_graf = VisualisasiGraf()
    program_graf.jalankan()