from xml.dom import minidom

class Faktura():
    def __init__(self, nr_faktury, data_wystawienia=False, data_sprzedazy=False, termin_platnosci=False, id_sprzedawcy=False, korekta=False, wartosc_netto=False, wartosc_brutto=False):
        self.nr_faktury = nr_faktury
        self.data_wystawienia = data_wystawienia
        self.data_sprzedazy = data_sprzedazy
        self.termin_platnosci = termin_platnosci
        self.id_sprzedawcy = id_sprzedawcy
        self.korekta = korekta
        self.wartosc_netto = wartosc_netto
        self.wartosc_brutto =wartosc_brutto



class Lek():
    def __init__(self,id_towaru, nazwa=False, BLOZ=False, jednostka=False, seria=False, data_waznosci=False, cena_netto=False, cena_brutto=False, PKWiU=False, kod_kreskowy=False, faktura=False):
        self.id_towaru = id_towaru
        self.nazwa = nazwa
        self.BLOZ = BLOZ
        self.jednostka = jednostka
        self.seria = seria
        self.data_waznosci = data_waznosci
        self.cena_netto = cena_netto
        self.cena_brutto = cena_brutto
        self.PKWiU = PKWiU
        self.kod_kreskowy = kod_kreskowy
        self.faktura = faktura




f = open('FV749746.XML')
tree = minidom.parse(f)

towary = tree.getElementsByTagName('towar')
faktura = tree.getElementsByTagName('faktura')[0]
naglowek =  faktura.getElementsByTagName('naglowek')[0]
pozycje = faktura.getElementsByTagName('pozycja')

id_list = []
lek_list =[]
faktura_list =[]

def create_faktura(naglowek):
    nr_faktury = naglowek.getElementsByTagName('nr_faktury')[0].firstChild.data
    try:
        data_wystawienia = naglowek.getElementsByTagName('data-wystawienia')[0].firstChild.data
    except:
        data_wystawienia = False
    try:
        data_sprzedazy = naglowek.getElementsByTagName('data-sprzedazy')[0].firstChild.data
    except:
        data_sprzedazy = False
    try:
        termin_platnosci = naglowek.getElementsByTagName('termin-platnosci')[0].firstChild.data
    except:
        termin_platnosci = False
    try:
        id_sprzedawcy = naglowek.getElementsByTagName('id-sprzedawcy')[0].firstChild.data
    except:
        id_sprzedawcy = False
    try:
        korekta = naglowek.getElementsByTagName('korekta')[0].firstChild.data
    except:
        korekta = False
    try:
        wartosc_netto = naglowek.getElementsByTagName('wartosc-netto')[0].firstChild.data
    except:
        wartosc_netto = False
    try:
        wartosc_brutto = naglowek.getElementsByTagName('wartosc-brutto')[0].firstChild.data
    except:
        wartosc_brutto = False

    return Faktura(nr_faktury= nr_faktury, data_wystawienia= data_wystawienia, data_sprzedazy= data_sprzedazy, termin_platnosci= termin_platnosci, id_sprzedawcy= id_sprzedawcy, korekta= korekta, wartosc_netto= wartosc_netto, wartosc_brutto= wartosc_brutto)


for towar in towary:
    _id = towar.getElementsByTagName('id-towaru')[0].firstChild.data
    id_list.append(id)
    try:
        _nazwa = towar.getElementsByTagName('id-towaru')[0].parentNode.getElementsByTagName('nazwa')[0].firstChild.data
    except:
        _nazwa = 'Brak nazwy'
    try:
        _BLOZ = towar.getElementsByTagName('id-towaru')[0].parentNode.getElementsByTagName('id-towaru-ks')[0].firstChild.data
    except:
        _BLOZ = False

    for pozycja in pozycje:
        ilosc = 0
        if pozycja.getElementsByTagName('id-towaru')[0].firstChild.data == _id:
            try:
                _jednostka = pozycja.getElementsByTagName('jednostka-miary')[0].firstChild.data
            except:
                _jednostka = False
            try:
                _seria = pozycja.getElementsByTagName('seria')[0].firstChild.data
            except:
                _seria= False
            try:
                _data_waznosci = pozycja.getElementsByTagName('data-waznosci')[0].firstChild.data
            except:
                _data_waznosci= False
            try:
                _cena_netto = pozycja.getElementsByTagName('cena-netto')[0].firstChild.data
            except:
                _cena_netto= False
            try:
                _cena_brutto = pozycja.getElementsByTagName('cena-brutto')[0].firstChild.data
            except:
                _cena_brutto= False
            try:
                _PKWiU = pozycja.getElementsByTagName('pkwiu')[0].firstChild.data
            except:
                _PKWiU= False
            try:
                _kod_kreskowy = pozycja.getElementsByTagName('kod-kreskowy')[0].firstChild.data
            except:
                _kod_kreskowy= False
            try:
                _faktura = naglowek.getElementsByTagName('nr-faktury')[0].firstChild.data
            except:
                _faktura= False
            try:
                _ilosc= pozycja.getElementsByTagName('ilosc')[0].firstChild.data

            except:
                _ilosc = 0
            ilosc += int(_ilosc)

        for i in range(ilosc):
            lek_list.append(Lek(id_towaru =_id, nazwa=_nazwa, BLOZ=_BLOZ, jednostka=_jednostka, seria=_seria, data_waznosci=_data_waznosci, cena_netto=_cena_netto, cena_brutto=_cena_brutto, PKWiU=_PKWiU, kod_kreskowy=_kod_kreskowy, faktura=_faktura))


for lek in lek_list:
    print(lek.nazwa)
