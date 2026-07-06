import time
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# ============================================================
# MINI PROJECT GRAPH COLORING
# Studi Kasus:
# Penjadwalan Sterilisasi Paket Alat Klinik Gigi
#
# Node  = Paket alat klinik gigi yang harus disterilkan
# Edge  = Konflik, artinya dua paket alat tidak boleh disterilkan bersamaan
# Warna = Slot / batch sterilisasi
# ============================================================


# ------------------------------------------------------------
# 1. DATA NODE
# ------------------------------------------------------------
nodes = {
    "A": "Pemeriksaan Dasar",
    "B": "Scaling",
    "C": "Tambal Gigi",
    "D": "Cabut Gigi",
    "E": "Bedah Minor",
    "F": "Jahit Luka",
    "G": "Cetak Gigi",
    "H": "Perawatan Saluran Akar",
    "I": "Pedodonti / Anak",
    "J": "Kontrol Ortodonti"
}


# ------------------------------------------------------------
# 2. DATA EDGE / KONFLIK
# ------------------------------------------------------------
edges = [
    ("A", "B"),
    ("A", "C"),
    ("A", "D"),
    ("A", "I"),
    ("A", "J"),

    ("B", "C"),
    ("B", "H"),
    ("B", "I"),

    ("C", "H"),
    ("C", "I"),
    ("C", "J"),

    ("D", "E"),
    ("D", "F"),
    ("D", "H"),
    ("D", "I"),

    ("E", "F"),
    ("E", "H"),
    ("E", "I"),

    ("F", "H"),

    ("G", "J")
]


# ------------------------------------------------------------
# 3. MEMBUAT GRAPH
# ------------------------------------------------------------
G = nx.Graph()
G.add_nodes_from(nodes.keys())
G.add_edges_from(edges)


# ------------------------------------------------------------
# 4. FUNGSI CEK PEWARNAAN VALID
# ------------------------------------------------------------
def cek_pewarnaan_valid(graph, coloring):
    """
    Mengecek apakah hasil pewarnaan sudah valid.
    Dua node yang memiliki edge tidak boleh memiliki warna yang sama.
    """
    for u, v in graph.edges():
        if coloring[u] == coloring[v]:
            return False, (u, v)
    return True, None


# ------------------------------------------------------------
# 5. FUNGSI GRAPH COLORING MINIMUM
# ------------------------------------------------------------
def cari_pewarnaan_minimum(graph):
    """
    Mencari jumlah warna minimum menggunakan backtracking.
    Metode ini cocok untuk data kecil seperti mini project ini.
    """

    # Node diurutkan dari konflik terbanyak agar proses pewarnaan lebih efisien
    urutan_node = sorted(
        graph.nodes(),
        key=lambda node: graph.degree[node],
        reverse=True
    )

    def aman_diwarnai(node, warna, coloring):
        """
        Mengecek apakah sebuah node aman diberi warna tertentu.
        """
        for tetangga in graph.neighbors(node):
            if coloring.get(tetangga) == warna:
                return False
        return True

    def backtracking(index, jumlah_warna, coloring):
        """
        Proses mencoba warna satu per satu.
        """
        if index == len(urutan_node):
            return coloring.copy()

        node = urutan_node[index]

        for warna in range(jumlah_warna):
            if aman_diwarnai(node, warna, coloring):
                coloring[node] = warna

                hasil = backtracking(index + 1, jumlah_warna, coloring)

                if hasil is not None:
                    return hasil

                del coloring[node]

        return None

    # Mencoba dari 1 warna sampai jumlah node
    for jumlah_warna in range(1, len(graph.nodes()) + 1):
        hasil = backtracking(0, jumlah_warna, {})

        if hasil is not None:
            return hasil, jumlah_warna


# ------------------------------------------------------------
# 6. PROSES PEWARNAAN GRAPH
# ------------------------------------------------------------
mulai = time.time()

coloring, jumlah_slot = cari_pewarnaan_minimum(G)

selesai = time.time()
waktu_eksekusi = selesai - mulai


# ------------------------------------------------------------
# 7. VALIDASI HASIL PEWARNAAN
# ------------------------------------------------------------
valid, konflik_salah = cek_pewarnaan_valid(G, coloring)

print("\n============================================================")
print("GRAPH COLORING PENJADWALAN STERILISASI ALAT KLINIK GIGI")
print("============================================================")

if valid:
    print("\nStatus pewarnaan : VALID")
    print("Tidak ada node bertetangga yang memiliki warna sama.")
else:
    print("\nStatus pewarnaan : TIDAK VALID")
    print("Konflik terjadi pada edge:", konflik_salah)


# ------------------------------------------------------------
# 8. MENAMPILKAN KETERANGAN NODE
# ------------------------------------------------------------
print("\n=== KETERANGAN NODE ===")
for kode, nama in nodes.items():
    print(f"{kode} = {nama}")


# ------------------------------------------------------------
# 9. MENAMPILKAN DAFTAR EDGE / KONFLIK
# ------------------------------------------------------------
print("\n=== DAFTAR EDGE / KONFLIK ===")
for u, v in edges:
    print(f"{u} - {v} : {nodes[u]} konflik dengan {nodes[v]}")


# ------------------------------------------------------------
# 10. MENAMPILKAN HASIL PEWARNAAN SETIAP NODE
# ------------------------------------------------------------
print("\n=== HASIL PEWARNAAN NODE ===")
for kode in sorted(coloring):
    nama_paket = nodes[kode]
    slot = coloring[kode] + 1
    print(f"{kode} - {nama_paket:30s} --> Slot Sterilisasi {slot}")

print("\nJumlah slot sterilisasi minimum yang digunakan:", jumlah_slot)


# ------------------------------------------------------------
# 11. FITUR PENGEMBANGAN 1:
# MENAMPILKAN DEGREE SETIAP NODE
# ------------------------------------------------------------
print("\n=== DEGREE SETIAP NODE ===")
for kode in sorted(G.nodes()):
    print(f"{kode} - {nodes[kode]:30s} : {G.degree[kode]} konflik")


# ------------------------------------------------------------
# 12. FITUR PENGEMBANGAN 2:
# MENAMPILKAN NODE DENGAN KONFLIK TERBANYAK
# ------------------------------------------------------------
degree_terbesar = max(dict(G.degree()).values())

node_terbanyak = [
    kode for kode, degree in G.degree()
    if degree == degree_terbesar
]

print("\n=== NODE DENGAN KONFLIK TERBANYAK ===")
for kode in node_terbanyak:
    print(f"{kode} - {nodes[kode]} dengan {degree_terbesar} konflik")


# ------------------------------------------------------------
# 13. FITUR PENGEMBANGAN 3:
# MENGHITUNG WAKTU EKSEKUSI
# ------------------------------------------------------------
print("\n=== WAKTU EKSEKUSI ===")
print(f"Waktu eksekusi program: {waktu_eksekusi:.6f} detik")


# ------------------------------------------------------------
# 14. MEMBANDINGKAN BEBERAPA STRATEGI GREEDY
# ------------------------------------------------------------
print("\n=== PERBANDINGAN STRATEGI GREEDY ===")

strategi_greedy = [
    "largest_first",
    "random_sequential",
    "smallest_last"
]

for strategi in strategi_greedy:
    hasil_greedy = nx.coloring.greedy_color(G, strategy=strategi)
    jumlah_warna_greedy = len(set(hasil_greedy.values()))
    print(f"Strategi {strategi:18s} menggunakan {jumlah_warna_greedy} warna/slot")


# ------------------------------------------------------------
# 15. MEMBUAT POSISI NODE AGAR VISUALISASI RAPI
# ------------------------------------------------------------
def buat_posisi_rapi(coloring):
    """
    Membuat posisi node berdasarkan slot warnanya.
    Node dengan slot yang sama diletakkan dalam satu kolom.
    """
    kelompok_slot = {}

    for node, warna in coloring.items():
        kelompok_slot.setdefault(warna, []).append(node)

    posisi = {}
    jarak_x = 2.8
    jarak_y = 1.5

    for warna in sorted(kelompok_slot):
        daftar_node = sorted(kelompok_slot[warna])
        jumlah_node = len(daftar_node)

        for index, node in enumerate(daftar_node):
            x = warna * jarak_x
            y = ((jumlah_node - 1) / 2 * jarak_y) - (index * jarak_y)
            posisi[node] = (x, y)

    return posisi


# ------------------------------------------------------------
# 16. VISUALISASI GRAPH YANG RAPI
# ------------------------------------------------------------
warna_visual = [
    "#FFB3BA",  # Slot 1
    "#BAFFC9",  # Slot 2
    "#BAE1FF",  # Slot 3
    "#FFFFBA",  # Slot 4
    "#D7BAFF",
    "#FFD6A5",
    "#C7CEEA"
]

daftar_node = sorted(G.nodes())

node_colors = [
    warna_visual[coloring[node]]
    for node in daftar_node
]

labels = {
    node: node
    for node in daftar_node
}

pos = buat_posisi_rapi(coloring)

plt.figure(figsize=(13, 7))

# Menggambar garis konflik
nx.draw_networkx_edges(
    G,
    pos,
    edge_color="gray",
    width=1.3,
    alpha=0.55
)

# Menggambar node
nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=daftar_node,
    node_color=node_colors,
    node_size=1800,
    edgecolors="black",
    linewidths=1.5
)

# Menggambar label node
nx.draw_networkx_labels(
    G,
    pos,
    labels=labels,
    font_size=14,
    font_weight="bold"
)

# Membuat legend warna
legend_slot = [
    Patch(
        facecolor=warna_visual[i],
        edgecolor="black",
        label=f"Slot Sterilisasi {i + 1}"
    )
    for i in range(jumlah_slot)
]

plt.legend(
    handles=legend_slot,
    title="Keterangan Warna",
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    fontsize=10,
    title_fontsize=11
)

plt.title(
    "Graph Coloring Penjadwalan Sterilisasi Paket Alat Klinik Gigi",
    fontsize=15,
    fontweight="bold",
    pad=20
)

plt.text(
    0.5,
    -0.08,
    "Node = paket alat | Edge = konflik | Warna = slot sterilisasi",
    transform=plt.gca().transAxes,
    ha="center",
    fontsize=10
)

plt.axis("off")
plt.tight_layout()

# Menyimpan visualisasi graph ke file gambar
nama_file = "graf_sterilisasi_klinik_gigi_rapi.png"
plt.savefig(nama_file, dpi=300, bbox_inches="tight")

plt.show()

print("\nVisualisasi graph berhasil disimpan sebagai:", nama_file)