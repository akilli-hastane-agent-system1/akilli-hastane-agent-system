import time

from modul3_minimax_algoritmasi import OyunDurumu,SAAT_DEGERLERİ,minimax
from modul3_alfa_beta import alfa_beta

TEKRAR=50

def algoritma_calistir(algoritma,derinlik):

    toplam_sure = 0

    for _ in range (TEKRAR):

        baslangic_durumu = OyunDurumu(tuple(SAAT_DEGERLERİ))

        baslangic_zamani = time.perf_counter()

        hamle,puan,dugum_sayisi = algoritma(baslangic_durumu,derinlik)

        toplam_sure += (time.perf_counter()-baslangic_zamani)*1000


    return{
            "hamle":hamle,
            "puan":puan,
            "dugum_sayisi": dugum_sayisi,
            "ortalama_sure_ms":round(toplam_sure/ TEKRAR,4)
        }
def karsilastir(derinlik):

    minimax_sonuc=algoritma_calistir(minimax,derinlik)
    alfa_beta_sonuc= algoritma_calistir(alfa_beta,derinlik)

    minimax_dugum = minimax_sonuc["dugum_sayisi"]
    alfa_beta_dugum= alfa_beta_sonuc["dugum_sayisi"]

    budanan_dugum = minimax_dugum - alfa_beta_dugum

    tasarruf = (budanan_dugum/minimax_dugum)*100

    ayni_puan = minimax_sonuc["puan"]== alfa_beta_sonuc["puan"]
    ayni_hamle = minimax_sonuc["hamle"] == alfa_beta_sonuc["hamle"]

    print("\n"+"."*80)
    print(f"DERİNLİK:{derinlik}")
    print("."*80)

    print(f"{'Algoritma':<15} | {'Hamle':<8} | {'Puan':<8} | "
          f"{'Dugum':<8} | {'Sure (ms)':<10}")

    print("-" * 80)


    for ad, sonuc in [
      ("Minimax",minimax_sonuc),
      ("Alfa-Beta",alfa_beta_sonuc)

    ]:

        print(f"{ad:<15} | {str(sonuc['hamle']):<8} | "
              f"{sonuc['puan']:<8} | "
              f"{sonuc['dugum_sayisi']:<8} | "
              f"{sonuc['ortalama_sure_ms']:<10}")

    print(f"\nBudanan dugum sayisi : {budanan_dugum}")
    print(f"Arama tasarrufu      : %{tasarruf:.2f}")
    print(f"Ayni karar puani     : {'EVET' if ayni_puan else 'HAYIR'}")
    print(f"Ayni ilk hamle       : {'EVET' if ayni_hamle else 'HAYIR'}")


if __name__ == "__main__":
    print("=" * 80)
    print(" ISE 315 - AKILLI HASTANE")
    print(" MODUL 3: MINIMAX VE ALFA-BETA KARSILASTIRMA RAPORU")
    print("=" * 80)

    for derinlik in [1, 2, 3, 4]:
        karsilastir(derinlik)



        
