from modul3_minimax_algoritmasi import OyunDurumu,SAAT_DEGERLERİ,degerlendir


def alfa_beta(durum,kalan_derinlik,alfa=float("-inf"),beta=float("inf")):
    ziyaret_sayisi=1

    if kalan_derinlik <= 0 or not durum.bos_saatler:
        return None, degerlendir(durum), ziyaret_sayisi


    en_iyi_hamle = None

    if durum.max_sirasi:
        en_iyi_puan = float("-inf")
    else:
        en_iyi_puan = float("inf")

    for saat in durum.bos_saatler:

        yeni_durum= durum.hamle_uygula(saat)

        _,puan,alt_ziyaret_sayisi=alfa_beta(yeni_durum,kalan_derinlik -1,alfa,beta)

        ziyaret_sayisi += alt_ziyaret_sayisi

        if durum.max_sirasi:

            if puan > en_iyi_puan:
                en_iyi_puan=puan
                en_iyi_hamle=saat


            alfa=max(alfa,en_iyi_puan)

        else:
            if puan < en_iyi_puan:
                en_iyi_puan=puan
                en_iyi_hamle=saat

            beta=min(beta,en_iyi_puan)

        if alfa >= beta:
            break

    return en_iyi_hamle,en_iyi_puan,ziyaret_sayisi

if __name__ == "__main__":

    baslangic_durumu = OyunDurumu(tuple(SAAT_DEGERLERİ))

    hamle, puan, dugum_sayisi = alfa_beta(baslangic_durumu, 2)

    print(f"Secilen ilk hamle: {hamle}")
    print(f"Kok puani: {puan}")
    print(f"Ziyaret edilen dugum sayisi: {dugum_sayisi}")

 