# modul 2 arama algoritmalari karsilastirma raporu
# bilgisiz : bfs, dfs, ids, ucs 
# bilgili : greedy, a*

from modul1_ajan_peas import AkilliHastaneOrtami

from modul2b_1_bilgili_ortak import BilgiliAramaAjani

import modul2b_2_a_yildiz
import modul2b_3_greedy
# astar ve greedy ortak arayuze kaydediyoruz


algoritma_listesi = [
    {"algoritma": "BFS"},
    {"algoritma": "DFS"},
    {"algoritma": "IDS"},
    {"algoritma": "UCS"},
    {"algoritma": "GREEDY", "sezgisel": "MNHTN"},
    {"algoritma": "GREEDY", "sezgisel": "SLD"},
    {"algoritma": "ASTAR", "sezgisel": "MNHTN"},
    {"algoritma": "ASTAR", "sezgisel": "SLD"}
]
# 4 bilgisiz + 2 bilgili x 2 sezgisel = 8 farkli algoritma

senaryolar = [
    ("Acil_Giris", "Ameliyathane_Kat2"),
    ("Asansor", "Yogun_Bakim")
]

TEKRAR = 50
# sure cok kucuk ciktigi icin her olcumu 50 kere yapip ortalamasini aliyorum

GENISLIK = 96


def baslik(metin):
    print("." * GENISLIK)
    print(f" {metin}")
    print("." * GENISLIK)


def kisa_rota(rota):
    if not rota:
        return "Rota Yok"
    return " > ".join(dugum.split("_")[0] for dugum in rota)
    # acil giris ' i acil olarak aliyoruz tablo duzeni icin


def calistir(ajan, baslangic, hedef, ayar):

    istek = {"baslangic": baslangic, "hedef": hedef}
    istek.update(ayar)

    toplam_sure = 0
    for _ in range(TEKRAR):
        sonuc = ajan.karar_uret(istek)
        toplam_sure += sonuc["islem_suresi_ms"]

    sonuc["ortalama_sure_ms"] = round(toplam_sure / TEKRAR, 4)
    return sonuc


def optimal_maliyet(ajan, baslangic, hedef):
    return ajan.karar_uret({"baslangic": baslangic, "hedef": hedef, "algoritma": "UCS"})["toplam_maliyet"]
    # ucs her zaman optimal oldugundan referans olarak aliyoruz


def graf_bilgisi(hastane):

    baslik("[1] DURUM UZAYI G=(V,E)")

    dugum_sayisi = len(hastane.hastane_grafi)
    kenar_sayisi = sum(len(komsular) for komsular in hastane.hastane_grafi.values()) // 2
    # graf yonsuz
    # dolayisiyla her kenar iki kere yazildigi icin 2 ye boluyoruz

    print(f" Dugum sayisi |V| : {dugum_sayisi}")
    print(f" Kenar sayisi |E| : {kenar_sayisi}")
    print(f" Algoritma sayisi : {len(algoritma_listesi)} (4 bilgisiz + 2 bilgili x 2 sezgisel)")


def sezgisel_tablosu(ajan, hastane, hedef):

    baslik(f"[2] SEZGISEL DEGERLER h(n)  (hedef: {hedef})")
    print(f" {'Dugum':<20} | {'Manhattan':>9} | {'SLD':>7} | {'Gercek (h*)':>11}")
    print(" " + "." * 56)

    for dugum in hastane.hastane_grafi:
        h_m = ajan.h_sezgisel(dugum, hedef, "MNHTN")
        h_s = round(ajan.h_sezgisel(dugum, hedef, "SLD"), 2)
        h_gercek = optimal_maliyet(ajan, dugum, hedef)
        print(f" {dugum:<20} | {h_m:>9} | {h_s:>7} | {h_gercek:>11}")

    print("\n Her satirda Manhattan ve SLD <= gercek maliyet -> iki sezgisel de kabul edilebilir.")


def senaryo_tablosu(ajan, numara, baslangic, hedef):

    optimal = optimal_maliyet(ajan, baslangic, hedef)

    baslik(f"[{numara}] SENARYO: {baslangic} -> {hedef}  (optimal maliyet: {optimal})")
    print(f" {'Algoritma':<14} | {'Maliyet':>7} | {'Genis.':>6} | {'Sure(ms)':>8} | {'Opt.':<5} | Rota")
    print(" " + "." * (GENISLIK - 1))

    for ayar in algoritma_listesi:
        sonuc = calistir(ajan, baslangic, hedef, ayar)
        optimal_mi = "EVET" if sonuc["toplam_maliyet"] == optimal else "HAYIR"

        print(f" {sonuc['algoritma']:<14} | {sonuc['toplam_maliyet']:>7} | "
              f"{sonuc['genisletilen_dugum_sayisi']:>6} | {sonuc['ortalama_sure_ms']:>8} | "
              f"{optimal_mi:<5} | {kisa_rota(sonuc['rota'])}")


if __name__ == "__main__":

    hastane = AkilliHastaneOrtami()
    ajan = BilgiliAramaAjani(hastane)

    print("." * GENISLIK)
    print(" ISE 315 - AKILLI HASTANE | MODUL 2: ARAMA ALGORITMALARI KARSILASTIRMA RAPORU")
    print("." * GENISLIK)

    graf_bilgisi(hastane)
    sezgisel_tablosu(ajan, hastane, senaryolar[0][1])

    numara = 3
    for baslangic, hedef in senaryolar:
        senaryo_tablosu(ajan, numara, baslangic, hedef)
        numara += 1