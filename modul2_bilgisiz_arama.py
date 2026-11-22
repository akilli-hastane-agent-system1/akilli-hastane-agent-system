# -*- coding: utf-8 -*-
"""
ISE 315 - Yapay Zekaya Giriş Dönem Projesi
Modül 2: Bilgisiz Arama Algoritmaları (BFS, DFS, IDS, UCS)
Sorumlu: Rol 3 - Bilgisiz Arama Algoritmaları Sorumlusu
"""

import heapq
import time
from modul1_ajan_peas import AkilliHastaneOrtami, AjanTabani, PEASModeli


# =====================================================================
# 1. TEMEL VERİ YAPILARI (Sıfırdan Implementasyon)
# =====================================================================

class Kuyruk:
    """BFS için FIFO (İlk Giren İlk Çıkar) veri yapısı."""
    def __init__(self):
        self.elemanlar = []

    def ekle(self, veri):
        self.elemanlar.append(veri)

    def cikar(self):
        if not self.bos_mu():
            return self.elemanlar.pop(0)
        return None

    def bos_mu(self):
        return len(self.elemanlar) == 0


class Yigin:
    """DFS ve IDS için LIFO (Son Giren İlk Çıkar) veri yapısı."""
    def __init__(self):
        self.elemanlar = []

    def ekle(self, veri):
        self.elemanlar.append(veri)

    def cikar(self):
        if not self.bos_mu():
            return self.elemanlar.pop()
        return None

    def bos_mu(self):
        return len(self.elemanlar) == 0


class OncelikliKuyruk:
    """UCS için toplam yol maliyeti g(n) en düşük düğümü öne alan Min-Heap yapısı."""
    def __init__(self):
        self.elemanlar = []
        self._sayac = 0  # Maliyetler eşitse eklenme sırasını korumak için sayaç ekledim

    def ekle(self, maliyet, veri):
        heapq.heappush(self.elemanlar, (maliyet, self._sayac, veri))
        self._sayac += 1

    def cikar(self):
        if not self.bos_mu():
            maliyet, _, veri = heapq.heappop(self.elemanlar)
            return maliyet, veri
        return None, None

    def bos_mu(self):
        return len(self.elemanlar) == 0


# =====================================================================
# 2. BİLİGİSİZ ARAMA MOTORU VE AJAN SINIFI
# =====================================================================

class BilgisizAramaAjani(AjanTabani):
    """
    Modül 1'deki AjanTabani sınıfından miras alır.
    Hastane durum uzayı grafı G=(V,E) üzerinde BFS, DFS, IDS ve UCS çalıştırır.
    """
    def __init__(self, hastane_ortami):
        peas = PEASModeli(
            performans_olcutleri=[
                "En az adım sayısı (BFS/IDS) veya en düşük yol maliyeti (UCS)",
                "Genişletilen düğüm sayısının raporlanması",
                "Minimum hesaplama süresi (ms)"
            ],
            ortam_tanimi="Hastane yerleşkesi durum uzayı grafı G=(V,E)",
            eyleyiciler=["Otonom sedye/ilaç robotu rota yönlendirmesi"],
            algilayicilar=["Konum düğüm sensörü", "Koridor maliyet haritası"]
        )
        super().__init__("AJAN-02A", "Bilgisiz Arama Navigasyon Ajanı", "Modül 2 (Bilgisiz Arama)", peas)

        #Modül 1 'deki hastane ortamı grafı
        self.graf = hastane_ortami.hastane_grafi

    def _sonuc_paketle(self, algoritma_adi, rota, toplam_maliyet, baslangic_zamani, open_list, closed_list):
        """Tüm arama algoritmaları için karşılaştırılabilir standart metrik çıktısı üretir."""
        gecen_sure_ms = (time.perf_counter() - baslangic_zamani) * 1000
        return {
            "algoritma": algoritma_adi,
            "rota": rota,
            "toplam_maliyet": toplam_maliyet,
            "genisletilen_dugum_sayisi": len(closed_list),
            "islem_suresi_ms": round(gecen_sure_ms, 4),
            "open_list": open_list,
            "closed_list": closed_list
        }

    # -----------------------------------------------------------------
    # ALGORİTMA 1: GENİŞLİK ÖNCELİKLİ ARAMA (BFS - Breadth-First Search)
    # -----------------------------------------------------------------
    def bfs(self, baslangic, hedef):
        """
        Kenar maliyetlerini dikkate almadan düğüm (adım) sayısı en az olan rotayı bulur.
        OPEN listesi FIFO Kuyruk ile yönetilir.
        """
        baslangic_zamani = time.perf_counter()

        if baslangic not in self.graf or hedef not in self.graf:
            return self._sonuc_paketle("BFS", None, float("inf"), baslangic_zamani, [], [])

        open_kuyruk = Kuyruk()
        open_kuyruk.ekle((baslangic, [baslangic], 0))  # (mevcut_dugum, yol, toplam_maliyet)
        open_kumesi = {baslangic}  # OPEN listesinde bekleyen düğümler
        closed_list = []           # CLOSED listesi: Genişletilen düğümler

        while not open_kuyruk.bos_mu():
            mevcut_dugum, yol, maliyet = open_kuyruk.cikar()
            open_kumesi.discard(mevcut_dugum)

            if mevcut_dugum == hedef:
                kalan_open = [eleman[0] for eleman in open_kuyruk.elemanlar]
                return self._sonuc_paketle("BFS", yol, maliyet, baslangic_zamani, kalan_open, closed_list)

            closed_list.append(mevcut_dugum)

            for komsu, kenar_maliyeti in self.graf[mevcut_dugum].items():
                if komsu not in closed_list and komsu not in open_kumesi:
                    open_kuyruk.ekle((komsu, yol + [komsu], maliyet + kenar_maliyeti))
                    open_kumesi.add(komsu)

        return self._sonuc_paketle("BFS", None, float("inf"), baslangic_zamani, [], closed_list)