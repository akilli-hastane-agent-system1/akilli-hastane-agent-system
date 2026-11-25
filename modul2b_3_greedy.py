# burada greedy best first search algoritmasini kullanacagiz
# fn = hn
# a*'dan farki g'yi hesaba katmamasi sadece hedefe yakinliga bakar
# hizli ama optimal degil


import time

from modul2_bilgisiz_arama import OncelikliKuyruk

from modul2b_1_bilgili_ortak import algoritmalari_otomatik_kaydet, open_dugumleri



def greedy(ajan, baslangic, hedef, sezgisel_adi="MNHTN"):

    baslangic_zamani = time.perf_counter()
    algoritma_adi = f"GREEDY({sezgisel_adi.upper()})"


    if baslangic not in ajan.graf or hedef not in ajan.graf:

        return ajan._sonuc_paketle(algoritma_adi, None, float("inf"), baslangic_zamani, [], [])


    open_kuyruk = OncelikliKuyruk()
    open_kumesi = {baslangic}

    closed_list = []
    adim_izi = []
    # her adimin kaydi

    h_baslangic = ajan.h_sezgisel(baslangic, hedef, sezgisel_adi)
    open_kuyruk.ekle(h_baslangic, (baslangic, [baslangic], 0))
    # oncelik sadece h, g'yi sadece maliyeti raporlamak icin tutuyoruz

    while not open_kuyruk.bos_mu():
        h_degeri, veri = open_kuyruk.cikar()
        # en kucuk h degerli yani en yakin cikar

        mevcut_dugum, yol, g_mevcut = veri
        open_kumesi.discard(mevcut_dugum)

        if mevcut_dugum == hedef:
            kalan_open = open_dugumleri(open_kuyruk, closed_list)
            sonuc = ajan._sonuc_paketle(algoritma_adi, yol, g_mevcut, baslangic_zamani, kalan_open, closed_list)
            sonuc["adim_izi"] = adim_izi
            return sonuc

        closed_list.append(mevcut_dugum)

        for komsu, kenar_maliyeti in ajan.graf[mevcut_dugum].items():

            if komsu in closed_list or komsu in open_kumesi:
                continue
            # greedy daha ucuz yol aramaz, her dugumu bir kere ekler

            h_komsu = ajan.h_sezgisel(komsu, hedef, sezgisel_adi)
            open_kuyruk.ekle(h_komsu, (komsu, yol + [komsu], g_mevcut + kenar_maliyeti))
            open_kumesi.add(komsu)
            # kuyruga h ile giriyor, g sadece tasiniyor

        adim_izi.append({
            "adim": len(closed_list),
            "genisletilen": mevcut_dugum,
            "g": g_mevcut,
            "h": round(h_degeri, 2),
            "f": round(h_degeri, 2),
            "open": open_dugumleri(open_kuyruk, closed_list),
            "closed": list(closed_list)
        })
        # greedy'de f = h, a* ile ayni anahtarlar olsun diye f'yi de yaziyoruz

    sonuc = ajan._sonuc_paketle(algoritma_adi, None, float("inf"), baslangic_zamani, [], closed_list)
    sonuc["adim_izi"] = adim_izi
    return sonuc
    # hedefe ulasamama durumu

algoritmalari_otomatik_kaydet("GREEDY", greedy)
# greedy'yi de ortak arayuze atiyoruz






# test alani
# python modul2b_3_greedy.py

if __name__ == "__main__":

    from modul1_ajan_peas import AkilliHastaneOrtami
    from modul2b_1_bilgili_ortak import BilgiliAramaAjani
    import modul2b_2_a_yildiz
    # a* ile kiyaslamak icin sadece testte import ediyoruz, greedy a*'a bagli degil

    hastane = AkilliHastaneOrtami()
    ajan = BilgiliAramaAjani(hastane)
    baslangic = "Acil_Giris"
    hedef = "Ameliyathane_Kat2"

    print(f" modul 2: greedy karsilastirmasi ({baslangic} -> {hedef})")
    print("." * 30)
    print(f"{'Algoritma':<14} | {'Maliyet':<8} | {'Genisletilen':<13} | {'Sure (ms)':<10} | {'Bulunan Rota'}")

    testler = [
        {"algoritma": "UCS"},
        {"algoritma": "ASTAR", "sezgisel": "MNHTN"},
        {"algoritma": "GREEDY", "sezgisel": "MNHTN"},
        {"algoritma": "ASTAR", "sezgisel": "SLD"},
        {"algoritma": "GREEDY", "sezgisel": "SLD"}
    ]
    # ayni sezgisel ile a* ve greedy yan yana

    for test in testler:
        istek = {"baslangic": baslangic, "hedef": hedef}
        istek.update(test)

        sonuc = ajan.karar_uret(istek)

        rota_metni = " -> ".join(sonuc["rota"]) if sonuc["rota"] else "Rota Yok"

        print(f"{sonuc['algoritma']:<14} | {sonuc['toplam_maliyet']:<8} | "
              f"{sonuc['genisletilen_dugum_sayisi']:<13} | {sonuc['islem_suresi_ms']:<10} | {rota_metni}")

    # her adimda acilan dugum, g ve h degerleri

    print("\nGREEDY (MNHTN) ADIM ADIM IZ:")
    print(f"{'Adim':<5} | {'Genisletilen':<18} | {'g':<5} | {'h':<6} | OPEN")
    print("-" * 90)

    iz_sonucu = ajan.karar_uret({"baslangic": baslangic, "hedef": hedef,
                                 "algoritma": "GREEDY", "sezgisel": "MNHTN"})

    for adim in iz_sonucu["adim_izi"]:
        print(f"{adim['adim']:<5} | {adim['genisletilen']:<18} | {adim['g']:<5} | "
              f"{adim['h']:<6} | {adim['open']}")

    # optimallik, greedy kac ciftte optimal yolu kaciriyor

    print("\nOPTIMALLIK TESTI: Greedy maliyeti UCS ile ayni mi?")

    for sezgisel in ["MNHTN", "SLD"]:
        optimal_olmayan = 0
        toplam = 0

        for bas in hastane.hastane_grafi:
            for hed in hastane.hastane_grafi:

                ucs_maliyet = ajan.karar_uret({"baslangic": bas, "hedef": hed,
                                               "algoritma": "UCS"})["toplam_maliyet"]
                g_maliyet = ajan.karar_uret({"baslangic": bas, "hedef": hed,
                                             "algoritma": "GREEDY", "sezgisel": sezgisel})["toplam_maliyet"]
                toplam += 1

                if g_maliyet != ucs_maliyet:
                    optimal_olmayan += 1
                    print(f"  {sezgisel}: {bas} -> {hed}  greedy={g_maliyet}, optimal={ucs_maliyet}")

        print(f"  {sezgisel}: {toplam} ciftin {optimal_olmayan} tanesinde greedy optimal degil.")


    # a*'da bu sayi 0 idi
    # greedy'de 0 dan buyuk cikmasi greedy'nin optimal olmadigini gosterir