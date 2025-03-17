import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from StatLib import graph_background, sql_table_read, get_table_animated

#denemeasdasdasdasdsdf
query = """
SELECT * FROM Oyuncular2025
ORDER BY attigi_gol DESC
LIMIT 8
"""
data = sql_table_read(query,player=True)
data["Ortalama_Gol"] = []
data["eksik"] = []
data["fazla"] = []
kort = int(sum(data["aldigi_sure"]) / sum(data["attigi_gol"]))
for player in range(len(data["attigi_gol"])):
    ort = int(data["aldigi_sure"][player] / data["attigi_gol"][player])
    if ort > kort :
        data["Ortalama_Gol"].append(kort)
        data["eksik"].append(0)
        data["fazla"].append(ort - kort)
    else:
        data["Ortalama_Gol"].append(ort)
        data["eksik"].append(kort - ort)
        data["fazla"].append(0)
df = pd.DataFrame(data)


# Ortalama eğilim çizgisini hesapla
ortalama_gol = df["attigi_gol"].sum() / df["oynadigi_mac"].sum()
ortalama_gol_dk = df["attigi_gol"].sum() / df["aldigi_sure"].sum()

df[["isim", "Ortalama_Gol", "eksik", "fazla"]].to_excel("golcüler.xlsx", index=False)



fig, ax = graph_background(1000, 2000, 8, 20, ortalama_gol_dk, "Aldığı Süre (Dakika)", "Gol Sayısı", "Süper Lig Gol Krallığı", ratio_x= 10, ratio_y=6)

get_table_animated(df, fig, ax, 1000, "aldigi_sure", "attigi_gol", picsize_hor=120, picsize_ver=120)

"""fig, ax = graph_background(15, 25, 8, 20, ortalama_gol, "Oynadığı Maç Sayısı", "Gol Sayısı", "Süper Lig Gol Krallığı", ratio_x= 10, ratio_y=6)

get_table_animated(df, fig, ax, 15, "oynadigi_mac", "attigi_gol", picsize_hor=120, picsize_ver=120, save_mp4=True, file_name="abc")"""