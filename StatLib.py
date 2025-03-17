import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymysql
from requests import get
from bs4 import BeautifulSoup
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.animation as animation
from collections import defaultdict




def graph_background(min_x, max_x, min_y, max_y, line_slope, 
                      label_x, label_y, table_name,line_DC = 0, 
                      ratio_x = 12, ratio_y=8,resolution= 400, intensity_rate= 0.3):
    
    fig, ax = plt.subplots(figsize=(ratio_x, ratio_y)) # Grafik boyutlarını belirleme
    fig.patch.set_facecolor("lightblue")

    # Arka plan için meshgrid oluşturma
    x = np.linspace(min_x, max_x, resolution)
    y = np.linspace(min_y, max_y, resolution)
    X, Y = np.meshgrid(x, y)

    
    for spine in ax.spines.values():
        spine.set_linewidth(2.5)  # Kalınlık: 2.5


    # Doğruya olan mesafeyi hesaplama
    distance = Y - (line_slope * X + line_DC)  # Doğrunun üstü pozitif, altı negatif olacak


    # Yoğunluk fonksiyonunu mesafeye göre belirleme
    max_distance = np.max(np.abs(distance))
    intensity = np.abs(distance* intensity_rate) / max_distance  # Mesafe arttıkça yoğunluk artacak (0: beyaz, 1: renkli)

    # RGB bileşenlerini ayarlama (beyazdan kırmızı-yeşile geçiş)
    background = np.ones((Y.shape[0], Y.shape[1], 3))  # Başlangıçta beyaz (1,1,1)

    # Yeşil ve kırmızı bileşenlerini belirleme (mavi hiç kullanılmıyor!)
    background[..., 1] = 1 - intensity * np.where(distance > 0, 0, 1)  # Alt kısım kırmızı (G=0)
    background[..., 0] = 1 - intensity * np.where(distance < 0, 0, 1)  # Üst kısım yeşil (R=0)
    background[..., 2] = 1 - intensity * np.where((distance > 0) & (distance < 0), 0, 1) 

    # Arka planı gösterme
    ax.imshow(background, extent=[min_x, max_x, min_y, max_y], origin='lower')


    ax.annotate(
    "",
    xy=(max_x, line_slope * max_x),  # Okun uç noktası
    xytext=(min_x, min_y),  # Okun başlangıç noktası
    arrowprops=dict(
        arrowstyle="->",  # Ok ucu şekli
        linewidth=3,       # Ok çizgisinin kalınlığı
        linestyle= "--",
        color="black",   # Ok rengi
        mutation_scale=25,  # Ok ucunun büyüklüğü
        alpha=0.9          # Saydamlık (daha belirgin olması için)
    ),
    fontsize=12,          # Yazı büyüklüğü
    color="darkred",      # Yazı rengi
    fontweight="bold",    # Yazıyı kalın yap
    ha= "center",
    va= "bottom"
)
    axis_rate=  (ratio_y * (max_x - min_x))/((max_y - min_y) * ratio_x)
    # Eksenleri ayarlama
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.set_xlabel(label_x, fontsize=18, color="black", fontweight="bold")
    ax.set_ylabel(label_y, fontsize=18, color="black", fontweight="bold")
    ax.set_title(table_name, fontsize=27, color="black", fontweight="bold")
    ax.set_aspect(axis_rate)

    return fig, ax

def connect_db(dbname="Stat_Super_Lig"):
    
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="Ka-Fa1500",
        database="Stat_Super_Lig",
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = db.cursor()
    return db, cursor

def disconnect_db(db, cursor):
    # Değişiklikleri kaydet ve bağlantıyı kapat
    db.commit()
    cursor.close()
    db.close()

def update_top_scorers():

    url = "https://www.worldfootball.net/goalgetter/tur-sueperlig-2024-2025/"
    html = get(url).text
    soup = BeautifulSoup(html, "lxml")

    table_1 = soup.find_all("td", class_ = "hell")
    table_2 = soup.find_all("td", class_ = "dunkel")

    data = {"sira" : [],
        "isim" : [],
        "ulke" : [],
        "takim": [],
        "gol"  : [],
        "penalti": []}
    
    sira = {}
    for i in range(int(len(table_1) / 6)):
        k = table_1[6 * i + 5].text.split()[0]
        if k not in sira.keys():
            sira[k] = table_1[6 * i].text
        else: 
            if sira[k] == "":
                sira[k] = table_2[6 * i].text
            else:
                continue

    for i in range(int(len(table_1) / 6)):
        k = table_2[6 * i + 5].text.split()[0]
        if k not in sira.keys():
            sira[k] = table_2[6 * i].text
        else: 
            if sira[k] == "":
                sira[k] = table_2[6 * i].text
            else:
                continue

    for i in range(int(len(table_1)/6)):
        gol = int(table_1[6 * i + 5].text.split()[0])
        penalti = int(table_1[6 * i + 5].text.split()[1][1])
        sirra = sira[str(gol)]
        data["sira"].append(sirra)
        data["isim"].append(table_1[6 * i + 1].text.strip())
        data["ulke"].append(table_1[6 * i + 2].text.strip())
        data["takim"].append(table_1[6 * i + 4].text.strip())
        data["gol"].append(gol)
        data["penalti"].append(penalti)

    for i in range(int(len(table_1)/6)):
        gol = int(table_2[6 * i + 5].text.split()[0])
        penalti = int(table_2[6 * i + 5].text.split()[1][1])
        sirra = sira[str(gol)]
        data["sira"].append(sirra)
        data["isim"].append(table_2[6 * i + 1].text.strip())
        data["ulke"].append(table_2[6 * i + 2].text.strip())
        data["takim"].append(table_2[6 * i + 4].text.strip())
        data["gol"].append(gol)
        data["penalti"].append(penalti)

    # SQL komutu: Verileri ekleme
    sql = """
    INSERT INTO GolKralligi (sira, oyuncu_adi, takim, ulke, attigi_gol, penalti_gol, mac_basi_gol)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    # Verileri `data` sözlüğünden alarak MySQL'e ekleme
    for i in range(len(data["sira"])):  # Tüm verileri sırayla eklemek için döngü
        degerler = (
            data["sira"][i],
            data["isim"][i],
            data["takim"][i],
            data["ulke"][i],
            data["gol"][i],
            data["penalti"][i],
            0.0  # Ortalama gol (default 0.0)
        )
        db,cursor =connect_db()
        cursor.execute(sql, degerler)
        disconnect_db(db,cursor)

def update_players2025():
    teams = ["adana-demirspor", "alanyaspor", "antalyaspor","besiktas", "bodrum-fk", "caykur-rizespor", "eyuepspor", "fenerbahce", "galatasaray",
        "gaziantep-fk", "goeztepe", "hatayspor", "istanbul-basaksehir", "kasimpasa-sk", "kayserispor", "konyaspor", "samsunspor",
        "sivasspor", "trabzonspor"]
    data = {"isim": [],
            "dakika": [],
            "oynadigi"  : [],
            "ilk-11"  : [],
            "girdigi"  : [],
            "ciktigi"  : [],
            "gol"  : [],
            "sari"  : [],
            "ikinci-sari"  : [],
            "kirmizi"  : [],
            "takim" : []}
    
    for team in teams:
        url = "https://www.worldfootball.net/team_performance/"+ team +"/tur-sueperlig-2024-2025/"
        html = get(url).text
        soup = BeautifulSoup(html, "lxml")
        tabled = soup.find("table", class_="standard_tabelle").find_all("td")

        for i in range(int(len(tabled) / 10) - 1):
            data["isim"].append(tabled[10 * (i + 1)].text)
            data["dakika"].append("0" if tabled[10 * (i + 1) + 1].text == "-" else tabled[10 * (i + 1) + 1].text[:-1])
            data["oynadigi"].append("0" if tabled[10 * (i + 1) + 2].text.strip() == "-" else tabled[10 * (i + 1) + 2].text.strip())
            data["ilk-11"].append("0" if tabled[10 * (i + 1) + 3].text == "-" else tabled[10 * (i + 1) + 3].text)
            data["girdigi"].append("0" if tabled[10 * (i + 1) + 4].text == "-" else tabled[10 * (i + 1) + 4].text)
            data["ciktigi"].append("0" if tabled[10 * (i + 1) + 5].text == "-" else tabled[10 * (i + 1) + 5].text)
            data["gol"].append("0" if tabled[10 * (i + 1) + 6].text == "-" else tabled[10 * (i + 1) + 6].text)
            data["sari"].append("0" if tabled[10 * (i + 1) + 7].text == "-" else tabled[10 * (i + 1) + 7].text)
            data["ikinci-sari"].append("0" if tabled[10 * (i + 1) + 8].text == "-" else tabled[10 * (i + 1) + 8].text)
            data["kirmizi"].append("0" if tabled[10 * (i + 1) + 9].text == "-" else tabled[10 * (i + 1) + 9].text)
            data["takim"].append(team)

    # SQL komutu: Verileri ekleme
    sql = """
    INSERT INTO Oyuncular2025 (isim, aldigi_sure, oynadigi_mac, ilk_11_mac, sonradan_girdigi_mac, oyundan_ciktigi_mac, attigi_gol, sari_kart, ikinci_sari_kirmizi, kirmizi_kart, takim)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """


    # Verileri `data` sözlüğünden alarak MySQL'e ekleme
    for i in range(len(data["isim"])):  # Tüm verileri sırayla eklemek için döngü
        degerler = (
            data["isim"][i],
            data["dakika"][i],
            data["oynadigi"][i],
            data["ilk-11"][i],
            data["girdigi"][i],
            data["ciktigi"][i],
            data["gol"][i],
            data["sari"][i],
            data["ikinci-sari"][i],
            data["kirmizi"][i],
            data["takim"][i],
        )
        db,cursor =connect_db()
        cursor.execute(sql, degerler)
        disconnect_db(db,cursor)

    print("Oyuncular2025 Tablosu başarıyla güncellenmiştir!!!")

def plot_graph(data, fig, ax, initial_x, right_move= True, save_gif= False, save_mp4=False, ):
    df = pd.DataFrame(data)

    # Görselleri başlangıç noktasına yerleştir
    init_x = [initial_x] * len(df)  # Tüm resimler en solda başlayacak
    images = []

    for i in range(len(df)):
        img = Image.open(df["Resim Dosya"][i])
        img = img.resize((120, 120))
        im = OffsetImage(img, zoom=0.5)
        ab = AnnotationBbox(im, (initial_x, df["Gol Sayısı"][i]), frameon=False)
        ax.add_artist(ab)
        images.append(ab)

    index = 0
    # Animasyon fonksiyonu
    def update(frame):
        global index
        target_x = df["Mac"][index]
        new_x = initial_x + (target_x - initial_x) * min((frame / 50) - index , 1)
        if new_x >= target_x:
            index += 1
            frame = 0
            
        else :
            images[index].xybox = (new_x, df["Gol Sayısı"][index])
        return images

    # Animasyonu oluştur

    ani = animation.FuncAnimation(fig, update, frames=450, interval=50, blit=False, repeat= False)
    if save_gif:
        ani.save("goal_animation.gif", writer="pillow", fps=30)
    if save_mp4:
        ani.save("goal_animation.mp4", writer="ffmpeg", fps=30)

        plt.show()

def sql_table_read(query, team= False, player = False):
    db, cursor = connect_db()

    cursor.execute(query)
    data_list = cursor.fetchall()  # Sonuçları liste olarak al

    # Bağlantıyı kapat
    cursor.close()
    db.close()

    data = {}
    # Çekilen veriyi dictionarye dönüştürür
    for row in data_list:
        for key in row.keys():
            if key not in data.keys():
                data[key] = [row[key]]
            else:
                data[key].append(row[key])

    if team or player:
        data["Resim Dosya"]= []
        if player:
            for i in range(len(data["id"])):
                data["Resim Dosya"].append("Fotograflar/Super_Lig/Oyuncular/" + data["isim"][i].strip().split()[-1]+ ".png")
        elif team:
            for i in range(len(data["id"])):
                data["Resim Dosya"].append("Fotograflar/Super_Lig/Takim-Logolari/" + data["takim"][i].strip().split()[-1]+ ".png")

        

    return data

def get_table_animated(df, fig, ax, initial_x, independent_var, constant_var, picsize_hor=100, picsize_ver=100, fps= 30, save_mp4= False, save_gif= False, file_name= "Ani", block_step= 0.2):
    images = []

    # Veri tiplerini uygun hale getir
    df[constant_var] = df[constant_var].astype(float)
    df[independent_var] = df[independent_var].astype(float)

    point_counts = defaultdict(int)

    for i in range(len(df)):
        point = (df.loc[i, independent_var], df.loc[i, constant_var])
        count = point_counts[point]
        
        if count % 2 == 0:
            df.loc[i, independent_var] += block_step * count
            df.loc[i, constant_var] += block_step * count
            point_counts[point] += 1
        else:
            df.loc[i, independent_var] -= block_step * count
            df.loc[i, constant_var] -= block_step * count
        
        
    for i in range(len(df)):
        img = Image.open(df["Resim Dosya"][i])
        img = img.resize((picsize_hor, picsize_ver))
        im = OffsetImage(img, zoom=0.5)
        ab = AnnotationBbox(im, (initial_x, df[constant_var][i]), frameon=False)
        ax.add_artist(ab)
        images.append(ab)

    global index
    index = 0
    global memo
    memo = 0
    # Animasyon fonksiyonu
    def update(frame):
        global index
        global step_size
        global memo
        target_x = df[independent_var][index]
        fram= int((target_x - initial_x)// step_size)
        new_x = initial_x + (target_x - initial_x) * min(((frame - memo) / fram)  , 1)
        if new_x >= target_x:
            index += 1
            memo = frame
            
        else :
            images[index].xybox = (new_x, df[constant_var][index])
        return images

    # Animasyonu oluştur
    frames= 0
    global step_size
    step_size = (df[independent_var].max() - initial_x) / 50
    for minute in df[independent_var]:
        frames += int((minute - initial_x)// step_size)
    
    
    ani = animation.FuncAnimation(fig, update, frames= frames, interval= 1 / fps, blit=False, repeat= False)

    if save_gif:
        ani.save("goal_animation.gif", writer="pillow", fps=30)

    if save_mp4:
        writer = animation.FFMpegWriter(
            fps=50,
            bitrate=8000,  
            codec="libx264",  
            extra_args=["-vf", "scale=1920:1080", "-crf", "15", "-preset", "slow"]
        )
        ani.save("Kaydedilenler/" + file_name + ".mp4", writer=writer, dpi=300)


    if not save_gif and not save_mp4:
        plt.show()

    