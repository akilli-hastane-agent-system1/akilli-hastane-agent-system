# -*- coding: utf-8 -*-
"""
ISE 315 - Yapay Zekaya Giriş Dönem Projesi
Modül 1 & Modül 2 Temel Altyapı Dosyası
"""


class AjanTabani:
    """
    Diğer tüm modüllerin (Modül 2, 3, 4, 5) miras alacağı (Inheritance) ana sınıf.
    Matematiksel ajan fonksiyonunu f: P* -> A (Algı Geçmişi -> Eylem) simüle eder.
    """
    def __init__(self, ajan_kodu, ajan_adi, hedef_modul, peas_nesnesi):
        self.ajan_kodu = ajan_kodu          # Örn: "AJAN-01"
        self.ajan_adi = ajan_adi            # Örn: "Bulanık Triyaj Ajanı"
        self.hedef_modul = hedef_modul      # Hangi modüle ait olduğu
        self.peas = peas_nesnesi            # PEASModeli sınıfından gelen nesne
        self.algi_gecmisi = []              # P* (Percept Sequence): Ajanın o ana kadar algıladığı tüm veriler
        self.son_eylem = None               # A (Action): Ajanın ürettiği son karar/eylem

    def algila(self, yeni_algi):
        """Sensörlerden gelen anlık veriyi ajanın hafızasına (algi_gecmisi) ekler."""
        self.algi_gecmisi.append(yeni_algi)
        return yeni_algi

    def karar_uret(self, aktif_veri):
        """
        Düşünme/Karar verme aşaması.
        Diğer modülleri yazan ekip arkadaşları kendi sınıflarında bu fonksiyonu ezerek (override) dolduracaktır.
        """
        varsayilan_karar = f"{self.ajan_adi} tarafından '{aktif_veri}' verisi işlendi."
        return varsayilan_karar

    def eyleme_gec(self, secilen_eylem):
        """Karar mekanizmasından çıkan sonucu Eyleyiciler aracılığıyla ortama uygular."""
        self.son_eylem = secilen_eylem
        return f"[{self.ajan_kodu} - {self.ajan_adi}] EYLEM -> {secilen_eylem}"

    def ajan_dongusu_calistir(self, ortam_verisi):
        """Standart Yapay Zeka Ajan Döngüsü: Algıla -> Düşün -> Eyleme Geç"""
        algilanan = self.algila(ortam_verisi)
        karar = self.karar_uret(algilanan)
        sonuc = self.eyleme_gec(karar)
        return sonuc


class HastaVakasi:
    """Modüller arasında dolaşacak ortak veri paketi."""
    def __init__(self, hasta_id, ad_soyad, yas, ates, nabiz, agri_seviyesi, semptomlar, baslangic_konumu):
        self.hasta_id = hasta_id
        self.ad_soyad = ad_soyad
        self.yas = yas
        self.ates = ates
        self.nabiz = nabiz
        self.agri_seviyesi = agri_seviyesi
        self.semptomlar = semptomlar
        self.baslangic_konumu = baslangic_konumu

        # Diğer modüllerin dolduracağı alanlar
        self.fuzzy_aciliyet_skoru = None   # Modül 5 dolduracak
        self.on_tani_ve_hedef_birim = None # Modül 4 dolduracak
        self.kaynak_onayi = None           # Modül 3 dolduracak
        self.hesaplanan_rota = None        # Modül 2 dolduracak


# =====================================================================
# SUNUM VE TEST EKRANI (Modül 1 & 2 Altyapı Çıktısı)
# =====================================================================
def modul1_sunum_calistir():
    hastane = AkilliHastaneOrtami()
    hastane.tum_ajanlari_baslat()

    print("\n" + "=" * 75)
    print(" ISE 315 - AKILLI HASTANE SİSTEMİ: MODÜL 1 & 2 TEMEL ALTYAPI")
    print("=" * 75)

    # PEAS Tablosunu Yazdır
    print("\n[BÖLÜM 3] SİSTEM ALT AJANLARI VE PEAS TABLOSU")
    print("-" * 75)
    for ajan in hastane.aktif_ajanlar.values():
        print(f">> [{ajan.ajan_kodu}] {ajan.ajan_adi} ({ajan.hedef_modul})")
        for bilesen, deger in ajan.peas.sozluk_olarak_ver().items():
            deger_metni = ", ".join(deger) if isinstance(deger, list) else deger
            print(f"   * {bilesen:<22}: {deger_metni}")
        print("-" * 75)


if __name__ == "__main__":
    modul1_sunum_calistir()
