import sqlite3

conn = sqlite3.connect('db.sqlite3')

c = conn.cursor()
nr_faktur =[]
leki =[]
for row in c.execute('SELECT DISTINCT nr_faktury FROM zol_lek WHERE stan="A"'):
    nr_faktur.append(row)



for i in nr_faktur:
    f =open('%s.xml' % i, 'w+')
    f.write("<dokumenty>\n")
    f.write("<towary>\n")
    for row in c.execute('SELECT * FROM zol_lek WHERE stan="A" AND nr_faktury = %s' % i):
        f.write('<towar>\n')
        f.write('<id-towaru>')
        f.write(str(row.__getitem__(0)))
        f.write('</id-towaru>\n')
        f.write('<nazwa>')
        f.write(row.__getitem__(1))
        f.write('</nazwa> \n')
        f.write('<id-towaru-ks>')
        f.write('</id-towaru-ks>\n')
        f.write('</towar>\n')
    f.write('</towary>\n')
    f.write('<faktury>\n')
    f.write('<faktura>\n')
    f.write('<naglowek>\n')
    f.write('<data-wystawienia>' + row.__getitem__(10) + '</data-wystawienia>\n')
    f.write('<data-sprzedazy>' + row.__getitem__(10) + '</data-sprzedazy>\n')
    f.write('<termin-platnosci>1999-01-01</termin-platnosci>\n')
    f.write('<forma-platnosci>Przelew</forma-platnosci>\n <id-knt-sprzedawcy></id-knt-sprzedawcy>\n')
    f.write('<id-knt-nabywcy></id-knt-nabywcy>\n')
    f.write('<nr-faktury>')
    f.write(row.__getitem__(2))
    f.write('</nr-faktury>\n')
    f.write('<id-faktury></id-faktury> \n <czy-korekta></czy-korekta> \n <liczba-poz></liczba-poz> \n <wartosc-netto> 0 </wartosc-netto> \n <wartosc-vat></wartosc-vat> \n <wartosc-brutto> 0 </wartosc-brutto> \n <wartosc-brutto-slownie></wartosc-brutto-slownie> \n <id-hrt-p2></id-hrt-p2>\n')
    f.write('</naglowek> \n')
    f.write('<pozycje> \n')
    for row in c.execute('SELECT * FROM zol_lek WHERE stan="A" AND nr_faktury = %s' % i):
        f.write('<pozycja> \n')
        f.write('<id-poz-faktury></id-poz-faktury>\n')
        f.write('<nr-poz-faktury></nr-poz-faktury>\n')
        f.write('<id-towaru>'+str(row.__getitem__(0)) +'</id-towaru>\n')
        f.write('<cena-netto-bu> </cena-netto-bu>\n')
        f.write('<cena-netto></cena-netto>\n')
        f.write('<wartosc-netto></wartosc-netto>\n')
        f.write('<wartosc-netto></wartosc-netto>\n')
        f.write('<cena-brutto-bu>'+ row.__getitem__(3) +'</cena-brutto-bu>\n')
        f.write('<cena-brutto>'+ row.__getitem__(3)+'</cena-brutto>\n')
        f.write('<wartosc-brutto></wartosc-brutto>\n')
        f.write('<rodzaj-ceny></rodzaj-ceny>\n')
        f.write('<ilosc>'+  row.__getitem__(4) +'</ilosc>\n')
        f.write('<stawka-vat>'+str(row.__getitem__(8))+'</stawka-vat>\n')
        f.write('<cena-detal-brutto></cena-detal-brutto>\n')
        f.write('<upust></upust>\n')
        f.write('<data-waznosci>'+  row.__getitem__(9)    +'</data-waznosci>\n')
        f.write('<seria> '+  row.__getitem__(11)   +'</seria>\n')
        f.write('<pkwiu></pkwiu>\n')
        f.write('<kod-kreskowy> '+    row.__getitem__(7)   + '</kod-kreskowy>\n')
        f.write('<nr-rezerwacji></nr-rezerwacji>\n')
        f.write('<jednostka-miary> ' +    row.__getitem__(5)   +  ' </jednostka-miary>\n')
        f.write('</pozycja>\n')
    f.write('</pozycje>\n</faktura>\n</faktury>\n</dokumenty>\n')
    f.close()

#print(row.__getitem__(3))
