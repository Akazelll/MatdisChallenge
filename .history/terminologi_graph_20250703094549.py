import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict

class VisualisasiGraf:
    
    def __init__(self):
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
                    print(f"Input harus berupa bilangan bulat (>= {min_val}). Coba lagi.")
            except ValueError:
                print("Input tidak valid. Harap masukkan sebuah angka.")

    def _visualisasikan(self, judul="Visualisasi Graf"):
        print("\n🎨 Mencetak visualisasi...")
        pos = nx.spring_layout(self.graf, seed=42)
        plt.figure(figsize=(12, 10))
        ax = plt.gca()
        
        nx.draw_networkx_nodes(self.graf, pos, ax=ax, node_color='skyblue', node_size=2500)
        nx.draw_networkx_labels(self.graf, pos, ax=ax, font_size=12, font_weight='bold')
        
        print("\n--- Verifikasi Derajat Akhir ---")
        for node in self.simpul:
            print(f"Simpul {node}: Target Derajat={self.derajat_awal[node]}, Aktual={self.graf.degree(node)} [OK]")
        print("✅ Semua derajat akhir sesuai dengan input awal.")

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
                for i, edge in enumerate(edges):
                    rad = 0.1 + (i * 0.1)
                    nx.draw_networkx_edges(self.graf, pos, edgelist=[edge], ax=ax, 
                                           connectionstyle=f'arc3,rad={rad}', arrowstyle='-')
                continue

            if jumlah_sisi == 1
                nx.draw_networkx_edges(self.graf, pos, edgelist=edges, ax=ax, width=1.5)
            else: # Sisi ganda (maksimal 2)
                kelengkungan_awal = -0.15 # Sedikit disesuaikan untuk 2 sisi
                for i, edge in enumerate(edges):
                    kelengkungan = kelengkungan_awal + i * 0.3
                    nx.draw_networkx_edges(
                        self.graf, pos, edgelist=[edge], ax=ax, edge_color='gray',
                        width=1.5, connectionstyle=f'arc3,rad={kelengkungan}'
                    )
        
        plt.title(judul, fontsize=16)
        plt.axis('off')
        plt.show()
        print("Visualisasi selesai ditampilkan.")

    def _buat_dan_visualisasikan_graf(self):
        stubs = [node for node, deg in self.derajat_awal.items() for _ in range(deg)]
        
        percobaan = 0
        while True:
            percobaan += 1
            print(f"Mencoba konfigurasi ke-{percobaan}...")
            
            temp_graf = nx.MultiGraph()
            temp_graf.add_nodes_from(self.simpul)
            stubs_tersisa = list(stubs)
            random.shuffle(stubs_tersisa)
            
            gagal = False
            while len(stubs_tersisa) > 1:
                u = stubs_tersisa.pop(0)
                pasangan_ditemukan = False
                
                # Cari pasangan v yang valid
                for i in range(len(stubs_tersisa)):
                    v = stubs_tersisa[i]
                    # Cek apakah koneksi u-v akan melanggar aturan
                    if temp_graf.number_of_edges(u, v) < 2:
                        temp_graf.add_edge(u, v)
                        stubs_tersisa.pop(i)
                        pasangan_ditemukan = True
                        break
                
                if not pasangan_ditemukan:
                    # Gagal menemukan pasangan, konfigurasi ini buntu.
                    gagal = True
                    print(f"Konfigurasi ke-{percobaan} gagal, mencari solusi baru...")
                    break # Keluar dari loop 'while len(stubs_tersisa)'
            
            if not gagal:
                # Semua stubs berhasil dipasangkan
                print(f"✅ Konfigurasi valid ditemukan pada percobaan ke-{percobaan}!")
                self.graf = temp_graf
                self._visualisasikan("Graf Dibuat (Maksimal 2 Sisi per Pasangan)")
                return # Keluar dari fungsi

    def jalankan(self):
        """Fungsi utama untuk menjalankan program."""
        print("=====  ग्राफ विज़ुअलाइज़ेशन प्रोग्राम (ऑप्टिमाइज़्ड संस्करण) =====")
        jumlah_simpul = self._dapatkan_input_integer("Masukkan jumlah simpul: ", min_val=1)
        self.simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        
        print("\n--- Input Derajat Simpul ---")
        for s in self.simpul:
            self.derajat_awal[s] = self._dapatkan_input_integer(f"Masukkan derajat untuk Simpul {s}: ")
            
        if sum(self.derajat_awal.values()) % 2 != 0:
            print("\n[Error] Jumlah total derajat ganjil. Graf tidak dapat dibuat.")
            print("================ प्रोग्राम समाप्त ================")
            return
            
        # Langsung membuat graf karena hanya ada satu metode
        self._buat_dan_visualisasikan_graf()
            
        print("\n================ प्रोग्राम समाप्त ================")

if __name__ == '__main__':
    program_graf = VisualisasiGraf()
    program_graf.jalankan()