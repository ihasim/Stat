import srt
from datetime import timedelta

# Altyazı metnini buraya ekleyin (satır başına bir cümle olacak şekilde)
text_lines = [
    "Süper Lig'de 24. haftaya girerken",
    "gol krallığı yarışı büyük bir çekişmeye sahne oluyor.",
    "Zirvede 18 golle Piatek yer alırken,",
    "onu 16 golle Simon Banza,",
    "15 golle En-Nesyri",
    "ve 14 golle Victor Osimhen takip ediyor." "Bu dörtlünün hemen arkasında ise",
    "12'şer golle Edin Džeko,",
    "Mame Thiam ve Ali Sowe bulunuyor.",
    "Barış Alper Yılmaz ise 10 golle", 
    "listeye son sıradan girmeyi başardı.", "Maç başına gol sayısına baktığımızda,",
    "Osimhen ve Banza gösterdikleri", 
    "yüksek performansla tablomuzun", 
    "yeşil bölgesinde yer alırken,", 
    "Barış Alper Yılmaz ise", 
    "23 maçta attığı 10 golle", 
    "kırmızı bölgede bulunuyor.", 
    "Ancak atılan golleri maç başına değil,", 
    "oynanan dakikaya göre değerlendirdiğimizde,", "En-Nesyri büyük bir sıçrama yaparak",
    "her 91 dakikada 1 gol ortalamasıyla", 
    "Süper Lig'in en verimli golcüsü oluyor.", 
    "Onu, 97 dakikada 1 gol atan", 
    "Piatek takip ederken,", 
    "Osimhen ve Banza da", 
    "129 dakikada 1 gol olan lig ortalamasının", 
    "üzerine çıkmayı başarıyor."
]

# Her altyazıyı 3 saniye gösterilecek şekilde zamanla
start_time = timedelta(seconds=1)
subs = []
for i, line in enumerate(text_lines):
    end_time = start_time + timedelta(seconds=3)
    subs.append(srt.Subtitle(index=i+1, start=start_time, end=end_time, content=line))
    start_time = end_time + timedelta(milliseconds=500)  # 0.5 saniye ara

# SRT formatında kaydet
with open("output.srt", "w", encoding="utf-8") as f:
    f.write(srt.compose(subs))

print("SRT dosyanız oluşturuldu: output.srt")
