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



