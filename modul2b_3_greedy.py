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
            return ajan._sonuc_paketle(algoritma_adi, yol, g_mevcut, baslangic_zamani, kalan_open, closed_list)

        closed_list.append(mevcut_dugum)

        for komsu, kenar_maliyeti in ajan.graf[mevcut_dugum].items():

            if komsu in closed_list or komsu in open_kumesi:
                continue
            # greedy daha ucuz yol aramaz en hızlı yoldan gider

            h_komsu = ajan.h_sezgisel(komsu, hedef, sezgisel_adi)
            open_kuyruk.ekle(h_komsu, (komsu, yol + [komsu], g_mevcut + kenar_maliyeti))
            open_kumesi.add(komsu)
            # kuyruga h ile giriyor, g sadece tasiniyor

    return ajan._sonuc_paketle(algoritma_adi, None, float("inf"), baslangic_zamani, [], closed_list)
    # hedefe ulasamama durumu

algoritmalari_otomatik_kaydet("GREEDY", greedy)
# greedy'yi de ortak arayuze atiyorum