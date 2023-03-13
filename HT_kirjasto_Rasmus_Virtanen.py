######################################################################
# CT60A0202 Ohjelmoinnin perusteet
# Tekijä: Rasmus Virtanen
# Opiskelijanumero: 0507975
# Päivämäärä: 7.11.2019
# Yhteistyö ja lähteet, nimi ja yhteistyön muoto:
# HUOM! KAIKKI KURSSIN TEHTÄVÄT OVAT HENKILÖKOHTAISIA!
######################################################################

import csv
import datetime
import sys
from collections import OrderedDict

#pyydetään käyttäjää antamaan havaintoaseman nimi ja vuosi
def valinta1():
    nimi = input("Anna havaintoaseman nimi: ")
    vuosi = int(input("Anna analysoitava vuosi: "))
    tiedosto = nimi + str(vuosi) + ".txt"
    print()
    return tiedosto, nimi, vuosi

#säätilatiedoston luku   
def valinta2(tiedosto):
    try:
        with open (tiedosto) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            rivien_määrä = 0
                    
            for row in reader:
                rivien_määrä += 1        
            print("Tiedosto '{}' luettu. Tiedostossa oli {} riviä.".format(tiedosto,rivien_määrä))
            print()
            csv_file.close()
    except FileNotFoundError or EOFError:
            print("Tiedoston '<{}>' avaaminen epäonnistui.".format(tiedosto))
                #print("Tiedoston '<Kumpula2018.txt>' avaaminen epäonnistui.")
            print()
            sys.exit(0)
                
    return tiedosto
    

#Analysoidaan päivittäiset säätilatiedot        
def valinta3(tiedosto, nimi):

    class PaisteRivi:
        pvm = "Pvm"
        aika=""
        paiste = nimi

    rivi = PaisteRivi()
    
    try:
        with open (tiedosto) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            paiva = 0
            kumulatiivinen_summa = 0
            pvmlista = []
            pvmlista.append(rivi.pvm)
            paistelista = []
            paistelista.append(rivi.paiste)
            next(reader)

            for row in reader:
                rivi.pvm = (row[0])
                rivi.aika = (row[1])
                rivi.paiste = (row[2])
                paivamaara = datetime.datetime.strptime(rivi.pvm, "%Y-%m-%d")
                #paiva muuttujan avulla tutkitaan summausta, samat päivät summataan
                #kun päivä muuttuu viedään päivämäärä ja summa listaan
                if paiva == paivamaara:
                    kumulatiivinen_summa = kumulatiivinen_summa + float(rivi.paiste)
                elif paiva == 0:
                    paiva = paivamaara
                else:
                    paistelista.append(int(kumulatiivinen_summa / 60))
                    paiva = paiva.strftime("%d.%m.%Y")
                    pvmlista.append(paiva)
                    paiva = paivamaara

            #viimeisen listan tulostus
            paistelista.append(int(kumulatiivinen_summa / 60))
            paiva = paiva.strftime("%d.%m.%Y")
            pvmlista.append(paiva)

            paistelista = (";".join(map(str, paistelista)))            
            pvmlista = (";".join(map(str, pvmlista)))    
            print("Data analysoitu ajalta {} - {}.".format(pvmlista[4:14],pvmlista[-10:]))
            print()
            csv_file.close()
    except UnboundLocalError:
            print("Lista on tyhjä. Analysoi data ennen tallennusta.")
            print()
    except StopIteration:
            print("Lista on tyhjä. Lue ensin tiedosto.")
            print()

        

    return pvmlista, paistelista

#Päivittäisten säätilatietojen tallennus tiedostoon
def valinta4(pvmlista, paistelista):

    #tarkistetaan, että listassa on tietoa, jos listan pituus on 1 se sisältää
    #pelkän otsikkorivin, ei paistetietoa    
    if len(pvmlista)==1:
        print("Lista on tyhjä. Lue ensin tiedosto.")
    else:    
        
        tulostiedosto = input("Anna tulostiedoston nimi: ")
        tiedosto = open(tulostiedosto, "w")
        tiedosto.write(pvmlista)
        tiedosto.write("\n")
        tiedosto.write(paistelista)
        tiedosto.write("\n")
        print("Paisteaika tallennettu tiedostoon '{}'.".format(tulostiedosto))
        print()
        tiedosto.close()
    return None

#Ilmatieteen laitoksen tiedoston luku
def valinta5(nimi, vuosi):


    tiedosto = (nimi + str(vuosi) + "_fmi.txt")
    with open (tiedosto) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        rivien_määrä = 0
        
        for row in reader:
            rivien_määrä += 1        
        print("Tiedosto '{}' luettu. Tiedostossa oli {} riviä.".format(tiedosto,rivien_määrä))
        print()
        csv_file.close()
    return tiedosto

#Ilmatieteen laitoksen kuukausittaisten säätilatietojen analysointi
def valinta6(tiedosto, nimi, vuosi):
    class PaisteRivi:
        kk = "Kk"
        paiste = nimi
        paiva =""
        paistevuosi=""
        

    rivi = PaisteRivi()
    with open (tiedosto) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        kuukausi = 0
        kumulatiivinen_summa = 0
        pvmlista = []
        pvmlista.append(rivi.kk)
        paistelista = []
        paistelista.append(nimi)
        paivamaaralista=[]
        next(reader)


        for row in reader:
            rivi.paistevuosi = (row[0])
            rivi.kk = (row[1])
            rivi.paiva= (row[2])
            rivi.paiste = (row[5])
            
            #käyttäjän antaman mukaisen vuoden rivit huomioidaan, muut skipataan yli
            if str(vuosi)==rivi.paistevuosi:
                paivamaaralista.append(rivi.paiva + "." + rivi.kk + "." + rivi.paistevuosi)

                #mikäli rivin paistearvo on tyhjää viedään arvoon nolla
                if rivi.paiste == "":
                        rivi.paiste = 0
                #kuukautta verrataan edelliseen kuukauteen, jos kuukausi vaihtuu, summataan
                elif kuukausi == rivi.kk:
                    kumulatiivinen_summa = kumulatiivinen_summa + int(rivi.paiste)
                elif kuukausi == 0:
                    kuukausi = rivi.kk
                else:
                    
                    paistelista.append(int(kumulatiivinen_summa/60))
                    pvmlista.append(kuukausi)
                    kuukausi = rivi.kk
                    kumulatiivinen_summa=0
                    kumulatiivinen_summa = kumulatiivinen_summa + int(rivi.paiste)

        #viimeisen rivin vienti listalle
        paistelista.append(int(kumulatiivinen_summa/60))
        pvmlista.append(kuukausi)
                
        paistelista = (";".join(map(str, paistelista)))            
        paivamaaralista = (";".join(map(str, paivamaaralista)))
        pvmlista = (";".join(map(str, pvmlista)))
        print("Data analysoitu ajalta {} - {}.".format(paivamaaralista[0:10],paivamaaralista[-10:]))
        print()

    return pvmlista, paistelista

#Ilmatieteen laitoksen kuukausittaisten tietojen tallennus
def valinta7(pvmlista, paistelista, avaus):
    kktiedosto = input("Anna kuukausitiedoston nimi: ")

    #avausmuuttuja alustettu pääohjelman alussa Falseksi, jotta saadaan ensimmäisellä
    #kerralla kuukaudet ja paisteajat, jos tiedostoja luetaan useampia, ei kirjoiteta
    #enää kuukausia, vaan lisätään uusi havaintoasema 
    if avaus == False:
        tiedosto = open(kktiedosto, "w")
        tiedosto.write(pvmlista)
        tiedosto.write("\n")
        avaus = True

    else:
        tiedosto = open(kktiedosto, "a")
        
    tiedosto.write(paistelista)
    tiedosto.write("\n")
    print("Paisteaika tallennettu tiedostoon '{}'.".format(kktiedosto))
    print()
    pvmlista = []
    paistelista = []
    tiedosto.close()
    return pvmlista, paistelista, avaus

