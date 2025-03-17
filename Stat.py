import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Takımlar ve kazanma yüzdeleri
teams = ["Cavaliers", "Celtics", "Thunder", "OKC", "Rockets", "Lakers", "Clippers", "Magic", "Cavaliers", "Celtics", "Thunder", "OKC", "Rockets", "Lakers", "Clippers", "Magic"]
win_percentages = np.array([0.944, 0.824, 0.750, 0.750, 0.667, -0.625,  -0.611, -0.611, 0.944, 0.824, 0.750, 0.750, 0.667, -0.625,  -0.611, -0.611])

# Başlangıçta tüm değerleri sıfır yapalım
current_values = np.zeros_like(win_percentages)

# Grafik oluşturma
fig, ax = plt.subplots(figsize=(6, 8))
fig.patch.set_facecolor("lightblue")  # Tüm figürün arka planını gri yapar

bars = ax.barh(teams, current_values, color="black", edgecolor="white")

# Eksen ayarları
ax.set_xlim(min(win_percentages) - 0.2, max(win_percentages) + 0.1)

# Başlık
ax.set_title("Winning Percentage", fontsize=25, color="black", fontweight="bold")

# X ve Y ekseni etiketleri
ax.set_xlabel("Win Percentage", fontsize=20, color="black", fontweight="bold")
ax.set_ylabel("Teams", fontsize=20, color="black", fontweight="bold")

# X ve Y eksen değerleri (tick'ler)
ax.tick_params(axis="x", labelsize=18, labelcolor="black")  # X eksenindeki yazılar
ax.tick_params(axis="y", labelsize=18, labelcolor="black")  # Y eksenindeki yazılar

# Renk değiştirme
for index, bar in enumerate(bars):
    if win_percentages[index] >= 0:
        bar.set_color("darkgreen")  # 0.8'den büyükse yeşil
    else:
        bar.set_color("red")  # Küçükse kırmızı

# Yüzde değerlerini çubukların yanında göstermek için boş bir liste oluşturuyoruz
text_labels = [ax.text(0, i, "", va='center', fontsize=12) for i in range(len(teams))]

# Animasyon fonksiyonu
def update(frame):
    progress = (frame + 1) / 50  # 50 frame'de tamamlanacak
    new_values = win_percentages * progress  # Oranlı artış

    # Çubukları güncelle
    for bar, new_value, text in zip(bars, new_values, text_labels):
        bar.set_width(new_value)
        text.set_x(new_value + 0.01)
        text.set_text(f"{new_value:.3f}")

    return bars + tuple(text_labels)  


# Animasyonu oluştur
ani = animation.FuncAnimation(fig, update, frames=50, interval=50, blit=False, repeat=False)
ani.save("Kaydedilenler/" + "file_name" + ".mp4", writer="ffmpeg", fps=50)
# Animasyonu göster
plt.gca().invert_yaxis()  # En büyük değeri en üste koymak için
plt.show()





