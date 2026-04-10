import re
from collections import Counter


STOPWORDS = {
    "ve", "bir", "bu", "da", "de", "ile", "için", "ama", "çok", "daha",
    "gibi", "ben", "sen", "o", "biz", "siz", "onlar", "mi", "mı", "mu",
    "mü", "ki", "ne", "en", "ya", "şu", "her", "hem", "ise", "bile",
    "ancak", "fakat", "lakin", "yani", "kadar", "sonra", "önce", "ya da"
}


def baslik_yazdir(metin):
    print("\n" + "=" * 50)
    print(f" {metin}")
    print("=" * 50)


def bolum_yazdir(metin):
    print(f"\n--- {metin} ---")


def temizle_ve_ayir(metin, kucuk_harf=True):
    if kucuk_harf:
        metin = metin.lower()
    metin = re.sub(r"[^\wçğışöüÇĞİŞÖÜ\s]", "", metin)
    return [k for k in metin.split() if k]


def stopwords_temizle(kelimeler):
    return [k for k in kelimeler if k not in STOPWORDS]


def analiz_et(kelimeler, metin_ham, top_n=10):
    if not kelimeler:
        return None
    
    sayac = Counter(kelimeler)
    toplam = len(kelimeler)
    benzersiz = len(set(kelimeler))
    cumle_sayisi = len(re.findall(r"[.!?]+", metin_ham)) or 1
    ort_uzunluk = sum(len(k) for k in kelimeler) / toplam
    en_cok = sayac.most_common(top_n)
    en_uzun = sorted(set(kelimeler), key=len, reverse=True)[:5]
    karakter_bosluksuz = len(metin_ham.replace("", "").replace("\n", ""))
    karakter_bosluklu = len(metin_ham)
    
    return {
        "toplam": toplam,
        "benzersiz": benzersiz,
        "cumle": cumle_sayisi,
        "ort_uzunluk": ort_uzunluk,
        "en_cok": en_uzun,
        "karakter_bosluklu": karakter_bosluklu,
        "sayac": sayac,
    }




def sonuclari_yazdir(sonuc, top_n):
    bolum_yazdir("Genel Istatistikler")
    print(f" Toplam kelime   : {sonuc['toplam']}")
    print(f" Benzersiz kelime    : {sonuc['benzersiz']}")
    print(f"  Cumle sayisi    : {sonuc['cumle']}")
    print(f"Ort. kelime uzunluğu : {sonuc['ort_uzunluk']:.2f} karakter")
    print(f" Karakter (bosluksuz) : {sonuc['karakter_bosluksuz']}")
    print(f"  Karakter (bosluklu)  : {sonuc['karakter_bosluklu']}")

    bolum_yazdir(f"En Cok Kullanilan {top_n} Kelime")
    en_fazla = sonuc["en_cok"][0][1] if sonuc["en_cok"] else 1
    for i, (kelime, adet) in enumerate(sonuc["en_cok"], 1):
        bar_uzunluk = int((adet / en_fazla) * 20)
        bar = "#" * bar_uzunluk + "." * (20 - bar_uzunluk)
        print(f" {i:>2}. {kelime:<20} [{bar}] {adet}")

        bolum_yazdir("En uzun 5 kelime")
        for kelime in sonuc["en_uzun"]:
            print(f"  {kelime} ({len(kelime)} harf)")


def kelime_ara(sayac):
    bolum_yazdir("Kelime Arama")
    while True:
        aranan = input(" Aramak istediğin kelime (cikmak icin 'q'): ").strip().lower()
        if aranan == "q":
            break
        if not aranan:
            continue
        adet = sayac.get(aranan, 0)
        if adet > 0:
            print(f"  BULUNDU:  '{aranan}' kelimesi metinde {adet} kez geciyor. ")
        else:
            print(f"  BULUNAMADI: '{aranan}' kelimesi metinde yok. ")


def menu():
    baslik_yazdir("KELİME SAYACI")
    print("  1 - Metin gir ve analiz et")
    print("  2 - Cikis")
    print()


def main():
    while True:
        menu()
        secim = input("  Seciminiz: ").strip()

        if secim == "1":
            print("\nMetni girin (bitirmek icin bos satırda 2 kez ENTER'e basin):")
            satirlar = []
            bos_sayisi = 0
            while bos_sayisi < 2:
                satir = input()
                if satir == "":
                    bos_sayisi += 1
                else:
                    bos_sayisi = 0
                    satirlar.append(satir)

            metin_ham = "\n".join(satirlar).strip()

            if not metin_ham:
                print("\n Hata: Metin bos olmaz. ")
                continue

            kucuk = input("\n Kucuk harfe cevirilsin mi? (e/h): ").strip().lower() == "e"
            sw_temizle = input(" Stopwords temizlensin mi? (e/h): ").strip().lower() == "e"
            top_n_girdi = input(" Kac kelime listelensin? (varsayılan 10): ").strip()
            top_n = int(top_n_girdi) if top_n_girdi.isdigit() else 10

            kelimeler = temizle_ve_ayir(metin_ham, kucuk)

            if sw_temizle:
                kelimeler = stopwords_temizle(kelimeler)

            sonuc = analiz_et(kelimeler, metin_ham, top_n)

            if sonuc:
                baslik_yazdir("ANALIZ SONUCLARI")
                sonuclari_yazdir(sonuc, top_n)

                devam = input("\n Kelime aramak ister misiniz? (e/h): ").strip().lower()
                if devam == "e":
                    kelime_ara(sonuc["sayac"])
            else:
                print("\n Analiz edilecek kelime bulunamadi. ")

        elif secim == "2":
            print("\n Cikis yapiliyor. Gorusmek uzere!\n")
            break

        else:
            print("\n Hatali secim. Lutfen 1 veya 2 girin. ")


if __name__ == "__main__":
    main()       