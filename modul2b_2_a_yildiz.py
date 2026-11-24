# burada a* algoritmasini kullanacagiz
# fn = hn + gn
# ucs'ye hn eklenmis hali

import time

from modul2_bilgisiz_arama import OncelikliKuyruk

from modul2b_1_bilgili_ortak import algoritmalari_otomatik_kaydet



def open_dugumleri(open_kuyruk, closed_list):
    # opendaki dugumleri tekrarsiz aliriz

    dugumler = []

    for eleman in open_kuyruk.elemanlar:

        dugum = eleman[2][0]
        # dugum,yol,g ve dugum adı

        if dugum not in closed_list and dugum not in dugumler:
            
            dugumler.append(dugum)

    return dugumler


def a_yildiz(ajan, baslangic, hedef, sezgisel_adi="MNHTN"):

    baslangic_zamani = time.perf_counter()
    algoritma_adi = f"A*({sezgisel_adi.upper()})"


    if baslangic not in ajan.graf or hedef not in ajan.graf:

        return ajan._sonuc_paketle(algoritma_adi, None, float("inf"), baslangic_zamani, [],[])


    open_kuyruk = OncelikliKuyruk()
    g_degerleri = {baslangic: 0} # anlik 0

    closed_list=[]

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
            return ajan._sonuc_paketle(algoritma_adi, yol, g_mevcut, baslangic_zamani, kalan_open, closed_list)

        # kuyruktan cikarken ekleme yapiyoruz
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

    return ajan._sonuc_paketle(algoritma_adi, None, float("inf"), baslangic_zamani, [], closed_list)
    # hedefe ulasamama durumu

algoritmalari_otomatik_kaydet("ASTAR", a_yildiz)
# astar adiyla ortak'a atiyoruz
# ajan.karar_uret ile kullananabiliriz