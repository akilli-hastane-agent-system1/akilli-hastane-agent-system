# -*- coding: utf-8 -*-
"""
ISE 315 - Yapay Zekaya Giriş Dönem Projesi
Modül 1 & Modül 2 Temel Altyapı Dosyası
"""


class PEASModeli:
    """
    Bir yapay zeka ajanının Görev Ortamını (Task Environment) tanımlayan
    PEAS (Performance, Environment, Actuators, Sensors) veri sınıfı.
    """
    def __init__(self, performans_olcutleri, ortam_tanimi, eyleyiciler, algilayicilar):
        self.performans = performans_olcutleri  # Ajanın başarısını ölçen kriterler (Liste)
        self.ortam = ortam_tanimi               # Ajanın içinde çalıştığı fiziksel/dijital çevre (Metin)
        self.eyleyiciler = eyleyiciler          # Ortama etki etme araçları - Actuators (Liste)
        self.algilayicilar = algilayicilar      # Ortamdan veri toplama araçları - Sensors (Liste)

    def sozluk_olarak_ver(self):
        """Arayüz (GUI) modülünün tabloya kolayca basabilmesi için veriyi dict olarak döndürür."""
        return {
            "Performans Ölçütü (P)": self.performans,
            "Ortam (E)": self.ortam,
            "Eyleyiciler (A)": self.eyleyiciler,
            "Algılayıcılar (S)": self.algilayicilar
        }


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


class AkilliHastaneOrtami:
    """
    Sistemin çalıştığı görev ortamının akademik karakterizasyonunu,
    alt ajan kayıtlarını ve hastane yerleşkesi graf modelini tutan sınıf.
    """
    def __init__(self):
        # 1. Ortam Karakterizasyonu (Modül 1 İsterleri)
        self.ortam_karakteristigi = {
            "1. Gözlemlenebilirlik": {
                "Secim": "Kısmi Gözlemlenebilir (Partially Observable)",
                "Aciklama": "Hastanın iç fizyolojik durumu ve koridorlardaki anlık hareketlilik tamamen bilinemez; arama/minimax anında yerel kesit tam gözlemlenebilir kabul edilir."
            },
            "2. Determinizm": {
                "Secim": "Stokastik (Stochastic / Belirsiz)",
                "Aciklama": "Yeni acil vaka gelişleri ve fizyolojik parametreler belirsizlik içerir; bu nedenle Modül 5'te Bulanık Mantık kullanılır."
            },
            "3. Epizodiklik": {
                "Secim": "Ardışık (Sequential)",
                "Aciklama": "Triyaj ve ön tanı kararları, sonraki kaynak tahsisini ve navigasyon rotasını doğrudan belirler."
            },
            "4. Dinamiklik": {
                "Secim": "Dinamik (Dynamic)",
                "Aciklama": "Ajanlar karar üretirken hastanın hayati bulguları ve koridor yoğunlukları değişmeye devam eder."
            },
            "5. Ajan Yapısı": {
                "Secim": "Çoklu Ajan (Multi-Agent: İşbirlikçi ve Rekabetçi)",
                "Aciklama": "Modüller arası akış işbirlikçidir; ancak Modül 3'te acil servis ile planlı operasyonlar sınırlı kaynaklar için rekabetçidir."
            }
        }

        # 2. Hastane Durum Uzayı Graf Modeli G=(V,E) [Modül 2 için Altyapı]
        # Kenar ağırlıkları hem Manhattan hem Kuş Uçuşu (SLD) sezgisel tutarlılığını sağlayacak şekilde belirlenmiştir.
        self.hastane_grafi = {
            "Acil_Giris": {"Kurye_Koridoru": 10, "Triyaj_Alani": 8},
            "Triyaj_Alani": {"Acil_Giris": 8, "Muayene_Kat_1": 15, "Asansor": 8},
            "Kurye_Koridoru": {"Acil_Giris": 10, "Eczane_Depo": 12},
            "Muayene_Kat_1": {"Triyaj_Alani": 15, "Yogun_Bakim": 20, "Ameliyathane_Kat2": 25},
            "Asansor": {"Triyaj_Alani": 8, "Ameliyathane_Kat2": 12},
            "Yogun_Bakim": {"Muayene_Kat_1": 20},
            "Ameliyathane_Kat2": {"Muayene_Kat_1": 25, "Asansor": 12},
            "Eczane_Depo": {"Kurye_Koridoru": 12}
        }

        # Sezgisel arama (A* / Greedy) için düğümlerin (x, y) koordinatları
        self.dugum_koordinatlari = {
            "Acil_Giris": (0, 0),
            "Triyaj_Alani": (3, 4),
            "Kurye_Koridoru": (6, 0),
            "Muayene_Kat_1": (3, 10),
            "Asansor": (8, 4),
            "Yogun_Bakim": (3, 20),
            "Ameliyathane_Kat2": (12, 10),
            "Eczane_Depo": (12, 0)
        }

        self.aktif_ajanlar = {}

    def ajan_kaydet(self, ajan_nesnesi):
        """Alt ajanları merkeze kaydeder."""
        self.aktif_ajanlar[ajan_nesnesi.ajan_kodu] = ajan_nesnesi

    def tum_ajanlari_baslat(self):
        """Projedeki 5 temel ajanın detaylı PEAS tanımlamalarını yükler."""
        self.ajan_kaydet(AjanTabani(
            "AJAN-01", "Acil Müdahale Koordinatörü", "Modül 1 (Merkez)",
            PEASModeli(
                ["Toplam müdahale süresini minimize etme", "Modüller arası senkronizasyon başarısı"],
                "Akıllı hastane bilgi yönetim ağı ve tüm alt birimler",
                ["Alt ajan tetikleyicileri", "Merkezi GUI kontrol ekranı", "Acil durum alarm sistemi"],
                ["Alt ajan durum raporları", "Acil çağrı kayıtları"]
            )
        ))
        self.ajan_kaydet(AjanTabani(
            "AJAN-02", "Otonom Sedye ve Navigasyon Ajanı", "Modül 2 (Arama Motoru)",
            PEASModeli(
                ["En düşük yol maliyeti g(n)", "En az genişletilen düğüm sayısı", "Minimum ulaşım süresi"],
                "Hastane yerleşkesi durum uzayı grafı G=(V,E), katlar, koridorlar ve asansörler",
                ["Otonom sedye/ilaç robotu motorları", "Rota yönlendirme ekranı"],
                ["Konum düğüm okuyucuları (RFID/UWB)", "Koridor yoğunluk ve maliyet sensörleri"]
            )
        ))
        self.ajan_kaydet(AjanTabani(
            "AJAN-03", "Kritik Kaynak Dağıtım Ajanı", "Modül 3 (Minimax & Alfa-Beta)",
            PEASModeli(
                ["Kritik hasta sağkalım faydasını maksimize etme", "Alfa-Beta budama verimliliği", "Sıfır kaynak çatışması"],
                "Sınırlı hastane kaynakları (Yoğun Bakım Yatağı, Ameliyathane, Cerrahi Ekip)",
                ["Ameliyathane/yatak tahsis kilidi", "Planlı operasyon erteleme/onaylama komutu"],
                ["Yatak doluluk izleyicileri", "Acil vaka ve planlı operasyon talep kuyruğu"]
            )
        ))
        self.ajan_kaydet(AjanTabani(
            "AJAN-04", "Tıbbi Karar Destek Ajanı", "Modül 4 (Çıkarım Motoru)",
            PEASModeli(
                ["Doğru ön tanı ve sevk isabeti", "Çakışma çözümü başarısı", "Adım adım açıklanabilirlik (Explanation)"],
                "Tıbbi bilgi tabanı (Knowledge Base) ve hasta klinik bulguları (Facts)",
                ["Ön tanı ve sevk raporu üreteci", "Kural açıklama ekranı"],
                ["Hasta yaş, tansiyon ve semptom girişleri", "Kan tahlili veri okuyucusu"]
            )
        ))
        self.ajan_kaydet(AjanTabani(
            "AJAN-05", "Bulanık Triyaj Denetim Ajanı", "Modül 5 (Fuzzy Logic)",
            PEASModeli(
                ["Hassas aciliyet katsayısı (0-100)", "Sıfır kritik vaka kaçırma", "Belirsizlik altında kararlılık"],
                "Acil servis triyaj alanı ve kesin sınırı olmayan fizyolojik hasta sinyalleri",
                ["Triyaj öncelik/renk kodu atayıcı", "Acil müdahale alarmı"],
                ["Dijital ateş ölçer", "Nabız/oksimetre sensörü", "Görsel Ağrı Ölçeği (VAS) girişi"]
            )
        ))


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

    # 1. Ortam Karakterizasyonunu Yazdır
    print("\n[BÖLÜM 1] ORTAM KARAKTERİZASYONU")
    print("-" * 75)
    for ozellik, detay in hastane.ortam_karakteristigi.items():
        print(f"* {ozellik} -> {detay['Secim']}")
        print(f"  Gerekçe: {detay['Aciklama']}\n")

    # 2. Durum Uzayı Graf Modelini ve Koordinatları Yazdır
    print("[BÖLÜM 2] DURUM UZAYI GRAF MODELİ G=(V,E)")
    print("-" * 75)
    print(f"Toplam Düğüm Sayısı (V) : {len(hastane.hastane_grafi)}")
    print("Komşuluklar ve Kenar Maliyetleri (E):")
    for dugum, komsular in hastane.hastane_grafi.items():
        print(f"  - {dugum:<20} -> {komsular}")
    print("\nSezgisel Arama (h(n)) Düğüm Koordinatları (x, y):")
    for dugum, koord in hastane.dugum_koordinatlari.items():
        print(f"  - {dugum:<20} : {koord}")

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
