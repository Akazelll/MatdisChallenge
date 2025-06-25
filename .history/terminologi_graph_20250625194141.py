import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict

class VisualisasiGraf:
    
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

        # 2. Logika custom untuk menggambar sisi (edges)
        # Kelompokkan sisi berdasarkan pasangan simpul yang dihubungkannya
        edge_groups = defaultdict(list)
        for u, v in self.graf.edges():
            # Urutkan simpul agar (A,B) dan (B,A) dianggap sama
            edge_groups[tuple(sorted((u, v)))].append((u, v))

        for key, edges in edge_groups.items():
            u, v = key
            jumlah_sisi = len(edges)
            
            if u == v:
                # Untuk loop, biarkan networkx menggambarnya dengan sedikit lengkungan
                nx.draw_networkx_edges(self.graf, pos, edgelist=edges, ax=ax, connectionstyle='arc3,rad=0.2')
                continue

            if jumlah_sisi == 1:
                # Jika hanya ada satu sisi, gambar sebagai garis lurus biasa
                nx.draw_networkx_edges(self.graf, pos, edgelist=edges, ax=ax, width=1.5)
            else:
                # Jika ada SISI GANDA, gambar sebagai beberapa busur terpisah
                # Tentukan kelengkungan awal agar busur terpusat
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


    def _konstruksi_havel_hakimi(self, urutan_derajat):
        seq = sorted([(d, n) for n, d in urutan_derajat.items()], reverse=True)
        if not seq: return []
        if seq[-1][0] < 0: return None
        if seq[0][0] == 0: return []
        (d, v) = seq.pop(0)
        if d > len(seq): return None
        sisi = [(v, seq[i][1]) for i in range(d)]
        derajat_baru = {node: degree for degree, node in seq}
        for i in range(d):
            derajat_baru[seq[i][1]] -= 1
        sisi_sisa = self._konstruksi_havel_hakimi(derajat_baru)
        return (sisi + sisi_sisa) if sisi_sisa is not None else None

    def _jalur_tanpa_syarat(self):
        print("\n--- Opsi 1: Membuat Graf Tanpa Syarat Tambahan ---")
        stubs = [node for node, deg in self.derajat.items() for _ in range(deg)]
        random.shuffle(stubs)
        while len(stubs) > 1:
            u = stubs.pop()
            v = stubs.pop()
            self.graf.add_edge(u, v)
        self._visualisasikan("Graf Dibuat Tanpa Syarat (Bebas Loop/Sisi Ganda)")

    def _jalur_dengan_syarat(self):
        print("\n--- Opsi 2: Membuat Graf Dengan Syarat ---")
        derajat_sisa = self.derajat.copy()
        jml_sisi_ganda = self._dapatkan_input_integer("Masukkan jumlah sisi ganda: ")
        for i in range(jml_sisi_ganda):
            while True:
                pair_input = input(f"Sisi ganda ke-{i+1}: Masukkan 2 label simpul (cth: 1 2): ")
                try:
                    u, v = pair_input.strip().split()
                    if u in self.simpul and v in self.simpul and u != v:
                        self.graf.add_edge(u, v)
                        derajat_sisa[u] -= 1
                        derajat_sisa[v] -= 1
                        if derajat_sisa[u] < 0 or derajat_sisa[v] < 0: raise ValueError
                        break
                    else: print(f"Input tidak valid. Gunakan dua label berbeda dari 1-{len(self.simpul)}.")
                except ValueError: print("Input error atau derajat menjadi negatif. Coba lagi."); continue
        jml_loop = self._dapatkan_input_integer("Masukkan jumlah loop: ")
        for i in range(jml_loop):
            while True:
                node_input = input(f"Loop ke-{i+1}: Masukkan 1 label simpul: ").strip()
                try:
                    if node_input in self.simpul:
                        self.graf.add_edge(node_input, node_input)
                        derajat_sisa[node_input] -= 2
                        if derajat_sisa[node_input] < 0: raise ValueError
                        break
                    else: print(f"Label tidak valid. Gunakan angka dari 1-{len(self.simpul)}.")
                except ValueError: print("Input error atau derajat menjadi negatif. Coba lagi."); continue
        print("\nDerajat sisa yang perlu dipenuhi:", derajat_sisa)
        sisi_sederhana = self._konstruksi_havel_hakimi(derajat_sisa)
        if sisi_sederhana is None:
            print("\n[Error] Graf tidak dapat dibuat dengan kombinasi yang diberikan.")
        else:
            self.graf.add_edges_from(sisi_sederhana)
            self._visualisasikan("Graf Dibuat Dengan Syarat Loop dan Sisi Ganda")

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
        print("2. Cetak menggunakan syarat (menentukan jumlah loop dan sisi ganda)")
        choice = ""
        while choice not in ['1', '2']:
            choice = input("Masukkan pilihan Anda (1 atau 2): ")
        if choice == '1':
            self._jalur_tanpa_syarat()
        else:
            self._jalur_dengan_syarat()
        print("\nFinish")
        print("================ Program Selesai ================")

if __name__ == '__main__':
    program_graf = VisualisasiGraf()
    program_graf.jalankan()