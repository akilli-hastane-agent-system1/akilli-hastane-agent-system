# suanlik modul 2 bilgili aramada tek rolde 2 kisi bulundan dolayi
# bu kisim ortak bir arayuz olmasi adina kurulmustur
# buradan ilerlenecektir


import math 

from modul2_bilgisiz_arama import BilgisizAramaAjani 
# rol 3 seymanurun bilgisiz ajani


# once manhattan ardindan da kus ucusu sezgisel yontemi kullanacagiz
# manhattan: var olan satir ve sutundan hedef satir sutunu cikartarak bulunur
def manhattan(koordinatlar, dugum, hedef):

    x1,y1 = koordinatlar[dugum]

    x2,y2 = koordinatlar[hedef]

    return abs(x1-x2)+abs(y1-y2)
    # mutlak deger

# burada kus ucusu yani oklid bulunur
def kus_ucusu(koordinatlar, dugum, hedef):

    x1,y1 = koordinatlar[dugum]

    x2,y2 = koordinatlar[hedef]

    return math.sqrt((x1-x2)**2+(y1-y2)**2)
    # karesi


sezgiseller = {"MNHTN" : manhattan, "SLD" : kus_ucusu} 
# dictionary, extra algoritma eklersek buradan devam edebiliriz


bilgili_algoritmalar = {}
# algoritmalari ekleyecegiz

def algoritmalari_otomatik_kaydet(ad, fonksiyon):

    bilgili_algoritmalar[ad.upper()] = fonksiyon
    # kafa karisikligi olmasin diye algoritmalari buyuk harfe ceviriyoruz, SLD MNHTN gibi


# -----

# ajan tabanindan bilgisiz arama ajanina oradan da bilgili arama ajanlarina 
class BilgiliAramaAjani(BilgisizAramaAjani):

    def __init__(self, hastane_ortami):
        super().__init__(hastane_ortami) # bilgisiz arama constructoru

        self.ajan_kodu = "AJAN-02B"
        self.ajan_adi = "Bilgili arama Ajanı"
        self.hedef_modul = "Modul 2 bilgili arama"
        self.koordinatlar = hastane_ortami.dugum_koordinatlari # koordinatlar , x y

    def h_sezgisel(self, dugum, hedef, sezgisel_adi="MNHTN"):

        return sezgiseller[sezgisel_adi.upper()](self.koordinatlar, dugum, hedef)

        # bilgili arama algoritmalari icin ortak tanimlama
        # sezgiseller["SLD"] gibi direkt kullanim icin


    def karar_uret(self, aktif_veri):

        algoritma = aktif_veri.get("algoritma", "UCS").upper()
        # algoritma yoksa rol 3 seymanur vasrayılan ucs algoritmasi

        if algoritma in bilgili_algoritmalar:
            sezgisel_adi = aktif_veri.get("sezgisel", "MNHTN")
            return bilgili_algoritmalar[algoritma](
                self, aktif_veri["baslangic"], aktif_veri["hedef"], sezgisel_adi
            )


        return super().karar_uret(aktif_veri)
        # kayit yoksa onceki modul yani seymanurun karar uretimine fırlatıyoruz



# -----

# gecici test alani
# python modul2_1_rol4_ortak_arayuz.py

if __name__ == "__main__":

    from modul1_ajan_peas import AkilliHastaneOrtami

    hastane = AkilliHastaneOrtami()
    ajan = BilgiliAramaAjani(hastane) 
    hedef = "Ameliyathane_Kat2"
 
    print(f" MODUL 2 SEZGISEL DEGER TABLOSU (Hedef: {hedef})")
    print("." * 60)
    print(f"{'Düğüm':<20} | {'Manhattan':<10} | {'SLD':<10}")
    

    for dugum in hastane.hastane_grafi:
        manhattan_degeri = ajan.h_sezgisel(dugum, hedef, "MNHTN")
        sld_degeri = round(ajan.h_sezgisel(dugum, hedef, "SLD"), 2)
        print(f"{dugum:<20} | {manhattan_degeri:<10} | {sld_degeri:<10}")


    print("\nVar olan bilgili algoritmalar:", list(bilgili_algoritmalar.keys()))
    # suan bostur, ekledikce cikacak

    ucs_sonuc = ajan.karar_uret({"baslangic": "Acil_Giris", "hedef": hedef, "algoritma": "UCS"})
    print("Yonlendirme testi (UCS -> Rol 3):", ucs_sonuc["toplam_maliyet"])



