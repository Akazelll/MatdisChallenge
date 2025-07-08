import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict

class VisualisasiGraf:

    def __init__(self):
        self.simpul = []
        self.derajat_awal = {}
        self.graf = nx.MultiGraph()

    def _input_int(self, prompt, min_val=0):
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
        pos = nx.spring_layout(self.graf, seed=42)
        plt.figure(figsize=(12, 10))
        ax = plt.gca()

        nx.draw_networkx_nodes(self.graf, pos, ax=ax, node_color='crimson', node_size=2500)
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

    def _graph_bebas(self):
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

    def run(self):
        print("===== Program Visualisasi Graf =====")
        jumlah_simpul = self._input_int("Masukkan jumlah simpul: ", min_val=1)
        self.simpul = [str(i) for i in range(1, jumlah_simpul + 1)]
        self.graf.add_nodes_from(self.simpul)

        print("\n--- Input Derajat Simpul ---")
        for s in self.simpul:
            self.derajat_awal[s] = self._input_int(f"Derajat simpul {s}: ")

        if sum(self.derajat_awal.values()) % 2 != 0:
            print("[Error] Total derajat ganjil. Tidak bisa buat graf.")
            return

        self._jalur_tanpa_syarat()
        print("\n================ Program Selesai ================")

if __name__ == '__main__':
    program_graf = VisualisasiGraf()
    program_graf.run()