SAAT_DEGERLERİ = {
    "A": (8, 7),
    "B": (6, 5),
    "C": (3, 2),
    "D": (2, 1),
}

class OyunDurumu:
    def __init__(self, bos_saatler, max_saatleri = (), min_saatleri = (), max_sirasi = True):
        self.bos_saatler = bos_saatler
        self.max_saatleri = max_saatleri
        self.min_saatleri = min_saatleri
        self.max_sirasi = max_sirasi

    def hamle_uygula(self, saat):
        bos_saatler = tuple(bos for bos in self.bos_saatler if bos != saat)

        if self.max_sirasi:
            return OyunDurumu(
                bos_saatler, self.max_saatleri + (saat,), self.min_saatleri, False
            )

        return OyunDurumu(
            bos_saatler, self.max_saatleri, self.min_saatleri + (saat,), True
        )

def degerlendir(durum):
    max_puani = sum(SAAT_DEGERLERİ[saat][0] for saat in durum.max_saatleri)
    min_puani = sum(SAAT_DEGERLERİ[saat][1] for saat in durum.min_saatleri)
    return max_puani - min_puani

def minimax(durum, kalan_derinlik):
    ziyaret_sayisi = 1

    if kalan_derinlik <= 0 or not durum.bos_saatler:
        return None, degerlendir(durum), ziyaret_sayisi

    hamle_puanlari = []
    for saat in durum.bos_saatler:
        yeni_durum = durum.hamle_uygula(saat)
        _, puan, alt_ziyaret_sayisi = minimax(yeni_durum, kalan_derinlik - 1)
        hamle_puanlari.append((saat, puan))
        ziyaret_sayisi += alt_ziyaret_sayisi

    sec = max if durum.max_sirasi else min
    en_iyi_hamle, en_iyi_puan = sec(hamle_puanlari, key=lambda sonuc: sonuc[1])
    return en_iyi_hamle, en_iyi_puan, ziyaret_sayisi

if __name__ == "__main__":
    baslangic_durumu = OyunDurumu(tuple(SAAT_DEGERLERİ))
    hamle, puan, dugum_sayisi = minimax(baslangic_durumu, 2)

    print(f"secilen ilk hamle: {hamle}")
    print(f"kök puanı: {puan}")
    print(f"ziyaret edilen düğüm sayısı: {dugum_sayisi}")