from flask import Flask, render_template, request
from kelime_sayaci import temizle_ve_ayir, stopwords_temizle, analiz_et

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def anasayfa():
    sonuc = None
    if request.method == "POST":
        metin = request.form["metin"]
        kelimeler = temizle_ve_ayir(metin)
        kelimeler = stopwords_temizle(kelimeler)
        sonuc = analiz_et(kelimeler, metin)
    return render_template("index.html", sonuc=sonuc)

@app.route("/ara" , methods=["POST"])
def ara():
    kelime = request.form["kelime"].strip().lower()
    metin = request.form["metin"]
    kelimeler = temizle_ve_ayir(metin)
    sayac = {}
    for k in kelimeler:
        sayac[k] = sayac.get(k, 0) + 1
    sayi = sayac.get(kelime, 0)
    return render_template("index.html", arama_sonuc=sayi, aranan=kelime)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)