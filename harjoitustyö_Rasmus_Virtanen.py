######################################################################
# CT60A0202 Ohjelmoinnin perusteet
# Tekijä: Rasmus Virtanen
# Opiskelijanumero: 0507975
# Päivämäärä: 7.11.2019
# Yhteistyö ja lähteet, nimi ja yhteistyön muoto:
# HUOM! KAIKKI KURSSIN TEHTÄVÄT OVAT HENKILÖKOHTAISIA!
######################################################################

import HT_kirjasto_Rasmus_Virtanen

def main():
    #avauslippua käytetään myöhemmin aliohjelmassa 7 kun tutkitaan onko kyseessä ensimmäinen
    #tiedostoonkirjoitus jolloin avataan "w" moodissa ja kirjoitetaan otsikkorivi
    #mahdolliset myöhemmät kirjotukset sisältävät vain paistearvoja
    avaus = False
    while True:
        print("Mitä haluat tehdä:")
        print("1) Anna havaintoasema ja vuosi")
        print("2) Lue säätilatiedosto")
        print("3) Analysoi päivittäiset säätilatiedot")
        print("4) Tallenna päivittäiset säätilatiedot")
        print("5) Lue Ilmatieteen laitoksen tiedosto")
        print("6) Analysoi kuukausittaiset säätilatiedot")
        print("7) Tallenna kuukausittaiset säätilatiedot")
        print("0) Lopeta")
        try:
            valinta = int(input("Valintasi: "))
        except ValueError:
            print("Anna valinta kokonaislukuna.")
            print()
            
        #1) Anna havaintoasema ja vuosi
        if valinta == 1:
            try:
                tiedosto, nimi, vuosi = HT_kirjasto_Rasmus_Virtanen.valinta1()
            except ValueError:
                print("Anna vuosi kokonaislukuna.")
                print()
                
        #2) Lue säätilatiedosto        
        elif valinta == 2:
            try:
                tiedosto = HT_kirjasto_Rasmus_Virtanen.valinta2(tiedosto)
            except UnboundLocalError:
                print("Valitse havaintoasema ja vuosi ennen tiedostonlukua.")
                print()
                
        #3) Analysoi päivittäiset säätilatiedot         
        elif valinta == 3:
            try:
                pvmlista, paistelista = HT_kirjasto_Rasmus_Virtanen.valinta3(tiedosto, nimi)
            except UnboundLocalError:
                pvmlista=""
                paistelista=""
                print("Lista on tyhjä. Lue ensin tiedosto.")
                print()
                
        #4) Tallenna päivittäiset säätilatiedo            
        elif valinta == 4:
            try:
                HT_kirjasto_Rasmus_Virtanen.valinta4(pvmlista, paistelista)
            except UnboundLocalError:
                print("Lista on tyhjä. Analysoi data ennen tallennusta.")
                print()
                
        #5) Lue Ilmatieteen laitoksen tiedosto
        elif valinta == 5:
            tiedosto = HT_kirjasto_Rasmus_Virtanen.valinta5(nimi, vuosi)

        #6) Analysoi kuukausittaiset säätilatiedot
        elif valinta == 6:
            pvmlista, paistelista = HT_kirjasto_Rasmus_Virtanen.valinta6(tiedosto, nimi, vuosi)
                
        #7) Tallenna kuukausittaiset säätilatiedot
        elif valinta == 7:
            pvmlista, paistelista, avaus = HT_kirjasto_Rasmus_Virtanen.valinta7(pvmlista, paistelista, avaus)


        #0) Lopeta            
        elif valinta == 0:
            print("Kiitos ohjelman käytöstä.")
            break
        else:
            print("Valintaa ei tunnistettu, yritä uudestaan.")
            print()

main()
