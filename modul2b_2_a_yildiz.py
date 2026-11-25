# burada a* algoritmasini kullanacagiz
# fn = hn + gn
# ucs'ye hn eklenmis hali

import time

from modul2_bilgisiz_arama import OncelikliKuyruk

from modul2b_1_bilgili_ortak import algoritmalari_otomatik_kaydet, open_dugumleri




def a_yildiz(ajan, baslangic, hedef, sezgisel_adi="MNHTN"):

    baslangic_zamani = time.perf_counter()
    algoritma_adi = f"A*({sezgisel_adi.upper()})"


    if baslangic not in ajan.graf or hedef not in ajan.graf:

        return ajan._sonuc_paketle(algoritma_adi, None, float("inf"), baslangic_zamani, [],[])


    open_kuyruk = OncelikliKuyruk()
    g_degerleri = {baslangic: 0} # anlik 0

    closed_list=[]
    adim_izi = []
    # kayıt

    h_baslangic = ajan.h_sezgisel(baslangic, hedef, sezgisel_adi)
    open_kuyruk.ekle(0 + h_baslangic, (baslangic, [baslangic], 0))
    # baslangicta dugum yol ve g yi aliyoruz

    while not open_kuyruk.bos_mu():
        f_degeri, veri = open_kuyruk.cikar()
        # min f degerli cikar

        mevcut_dugum, yol, g_mevcut = veri

        if mevcut_dugum in closed_list:
            continue
        # dugum eger closed'da ise zaten daha ucuz yoldan genisletilmistir


        if mevcut_dugum == hedef:
            kalan_open = open_dugumleri(open_kuyruk, closed_list)
            sonuc = ajan._sonuc_paketle(algoritma_adi, yol, g_mevcut, baslangic_zamani, kalan_open, closed_list)
            sonuc["adim_izi"] = adim_izi
            # adim izi degiskeninde bekletiyoruz

            return sonuc

        # hedef testini kuyruktan cikarken yapiyoruz
        # eklerken yaparsak opt. saglanmayabilir
        # ardindan closed'a atiyoruz

        closed_list.append(mevcut_dugum)

        for komsu, kenar_maliyeti in ajan.graf[mevcut_dugum].items():
            if komsu in closed_list:
                continue

            # kapali komsulara tekrar bakmiyoruz

            # komsuya ilk kez ulasiyorsak ( yani sonsuz ) veya daha ucuz yol varsa;
            yeni_g = g_mevcut + kenar_maliyeti

            if yeni_g < g_degerleri.get(komsu, float("inf")):

                g_degerleri[komsu] = yeni_g
                f_komsu = yeni_g + ajan.h_sezgisel(komsu, hedef, sezgisel_adi) # f = g + h
                open_kuyruk.ekle(f_komsu, (komsu, yol + [komsu], yeni_g))

        adim_izi.append({
            "adim": len(closed_list),
            "genisletilen": mevcut_dugum,
            "g": g_mevcut,
            "h": round(f_degeri - g_mevcut, 2),
            "f": round(f_degeri, 2),
            "open": open_dugumleri(open_kuyruk, closed_list),
            "closed": list(closed_list)
        })

    sonuc = ajan._sonuc_paketle(algoritma_adi, None, float("inf"), baslangic_zamani, [], closed_list)
    sonuc["adim_izi"] = adim_izi
    return sonuc
    # hedefe ulasamama durumu

algoritmalari_otomatik_kaydet("ASTAR", a_yildiz)
# astar adiyla ortak'a atiyoruz
# ajan.karar_uret ile kullananabiliriz



# test alani
# python modul2b_2_a_yildiz.py 

if __name__ == "__main__":

    from modul1_ajan_peas import AkilliHastaneOrtami
    from modul2b_1_bilgili_ortak import BilgiliAramaAjani

    hastane = AkilliHastaneOrtami()
    ajan = BilgiliAramaAjani(hastane)
    baslangic = "Acil_Giris"
    hedef = "Ameliyathane_Kat2"
    # ana senaryo acilden ameliyathaneye

    # ucs ile a* ayni maliyeti buluyor mu kac dugum aciyorlar ona bakiyoruz

    
    print(f" modul 2: A* karsilastirmasi ({baslangic} -> {hedef})")
    print("." * 30)
    print(f"{'Algoritma':<12} | {'Maliyet':<8} | {'Genisletilen':<13} | {'Sure (ms)':<10} | {'Bulunan Rota'}")
    

    testler = [
        {"algoritma": "UCS"},
        {"algoritma": "ASTAR", "sezgisel": "MNHTN"},
        {"algoritma": "ASTAR", "sezgisel": "SLD"}
    ]
    # ucs kiyas icin

    for test in testler:
        istek = {"baslangic": baslangic, "hedef": hedef}
        istek.update(test)

        sonuc = ajan.karar_uret(istek)

        rota_metni = " -> ".join(sonuc["rota"]) if sonuc["rota"] else "Rota Yok"

        print(f"{sonuc['algoritma']:<12} | {sonuc['toplam_maliyet']:<8} | "
              f"{sonuc['genisletilen_dugum_sayisi']:<13} | {sonuc['islem_suresi_ms']:<10} | {rota_metni}")

    # her adimda acilan dugum, g h f degerleri ve open listesi

    print("\nA* (MNHTN) ADIM ADIM IZ:")
    print(f"{'Adim':<5} | {'Genisletilen':<18} | {'g':<5} | {'h':<6} | {'f':<6} | OPEN")
    print("-" * 90)

    iz_sonucu = ajan.karar_uret({"baslangic": baslangic, "hedef": hedef,
                                 "algoritma": "ASTAR", "sezgisel": "MNHTN"})

    for adim in iz_sonucu["adim_izi"]:
        print(f"{adim['adim']:<5} | {adim['genisletilen']:<18} | {adim['g']:<5} | "
              f"{adim['h']:<6} | {adim['f']:<6} | {adim['open']}")


    # optimallik, optimal mi

    print("\nOPTIMALLIK TESTI: Tum dugum ciftlerinde A* maliyeti == UCS maliyeti mi?")
    hatali = 0
    toplam = 0

    for bas in hastane.hastane_grafi:
        for hed in hastane.hastane_grafi:

            ucs_maliyet = ajan.karar_uret({"baslangic": bas, "hedef": hed,
                                           "algoritma": "UCS"})["toplam_maliyet"]

            for sezgisel in ["MNHTN", "SLD"]:
                a_maliyet = ajan.karar_uret({"baslangic": bas, "hedef": hed,
                                             "algoritma": "ASTAR", "sezgisel": sezgisel})["toplam_maliyet"]
                toplam += 1

                if a_maliyet != ucs_maliyet:
                    hatali += 1
                    print(f"  HATA: {bas} -> {hed} ({sezgisel}) A*={a_maliyet}, UCS={ucs_maliyet}")

    print(f"  {toplam} testten {toplam - hatali} tanesi basarili.")


# a* her komsu icin ayrica hn hesapliyor
# bizim graf 8 dugum oldugu icin sure farki anlamsiz, asil olcut genisletilen dugum sayisi 