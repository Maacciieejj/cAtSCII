import time
import os  # bibioteka os do czyszczenia ekranu
import json  # Dodajemy import dla obsługi formatu JSON dla sejwowania
from src.utils.story_generator import generuj_historyjke  # import funkcji generującej historyjki
from src.utils.ascii_converter import wyszukaj_i_konwertuj  # import funkcji konwertującej obrazy na ASCII

#   |\---/|
#   | o_o |
#    \_^_/

# poiżej klasa Cat -----------------------------------


class Cat: 



    #poniżej konstruktor klasy Cat
    def __init__(self): # konstruktor klasy Cat
               
        # Próbujemy wczytać sejw, jeśli istnieje
        if os.path.exists('sejw.json'):
            self.wczytaj_sejw()
        else:
            # Inicjalizacja nowej gry
            self.najedzenie = 10 #Tworzy zmienną przechowującą poziom najedzenia kota. Self oznacza, że zmienna należy do instancji klasy
            self.zadbanie = 10 # podobnie
            self.dostatekuwagi = 10
            self.moment_adopcji = time.time()  # dodajemy czas startu jako właściwość kota
            self.ostatnia_aktualizacja = time.time()  # to tu ma niby usunac bledy z czasem


    # Nowa metoda do zapisywania stanu gry
    def zapisz_sejw(self):
        dane_sejwu = {
            'najedzenie': self.najedzenie,
            'zadbanie': self.zadbanie,
            'dostatekuwagi': self.dostatekuwagi,
            'moment_adopcji': self.moment_adopcji,
            'ostatnia_aktualizacja': time.time()  # Zapisujemy aktualny czas
        }

        with open('sejw.json', 'w', encoding='utf-8') as plik:
            json.dump(dane_sejwu, plik)


    # Nowa metoda do wczytywania stanu gry
    def wczytaj_sejw(self):
        try:
            with open('sejw.json', 'r', encoding='utf-8') as plik:
                dane_sejwu = json.load(plik)
                
            self.najedzenie = dane_sejwu['najedzenie']
            self.zadbanie = dane_sejwu['zadbanie']
            self.dostatekuwagi = dane_sejwu['dostatekuwagi']
            self.moment_adopcji = dane_sejwu['moment_adopcji']
            self.ostatnia_aktualizacja = dane_sejwu['ostatnia_aktualizacja'] ##to zamiast tego na dole. do obserwacji :)
            #### self.ostatnia_aktualizacja = time.time()  # Dodajemy to przed aktualizacją statystyk - sprawia ze kotu nie spadaja stasty za czas niedziaalnia programu)



            # Po wczytaniu sejwu, aktualizuj_statystyki() samo obliczy upływ czasu
            # i odpowiednio zaktualizuje statystyki kota
            self.aktualizuj_statystyki()
            print("\nWczytano stan kota:")
            self.zapisz_log("Wczytano sejw")
        
        except Exception as e:
            print(f"Błąd podczas wczytywania sejwu: {e}")
            print("Bierzesz nowego kota...")
            self.__init__()  # Po prostu wywołujemy konstruktor ponownie



    # funkcja zapisu logów do pliku
    def zapisz_log(self, akcja):
        with open('koci_pamietnik.txt', 'a', encoding='utf-8') as plik:
            czas_gry = int(time.time() - self.moment_adopcji)
            minuty = (czas_gry // 60) % 60
            godziny = (czas_gry // 3600) % 24
            dni = czas_gry // 86400
            
            log = f"\n[{dni}d {godziny}h {minuty}m] {akcja}\n"
            log += f"Najedzenie: {round(self.najedzenie, 2)}, "
            log += f"Zadbanie: {round(self.zadbanie, 2)}, "
            log += f"Dostatek uwagi: {round(self.dostatekuwagi, 2)}\n"

            plik.write(log)


    def aktualizuj_statystyki(self): # metoda aktualizująca statystyki kota jedna dla wszystkich procesow
        teraz = time.time()
        
        #ponizej zakomentowany emulator upływu 4 godzin (do testow co sie dzieje po snie)
        #if przelacznik1:  # jeśli kot śpi
        #    teraz += 14400  # dodaj 4 godziny (4 * 60 * 60 sekund)             

        minuty = int((teraz - self.ostatnia_aktualizacja) // 60)
        if minuty > 0:
            spadek = minuty / 120
            self.najedzenie = max(0, self.najedzenie - spadek)
            self.zadbanie = max(0, self.zadbanie - spadek)
            self.dostatekuwagi = max(0, self.dostatekuwagi - spadek)
            self.ostatnia_aktualizacja = teraz



    # ponizej są metody, które zmieniają wartość statystyk kota
    def karmienie(self): # definicja metody karmienie w klasie Cat
        self.najedzenie = min(10, self.najedzenie + 2)
        return wyszukaj_i_konwertuj("feeding cat")  #        # Zwracamy ASCII art zamiast go wyświetlać

        
    def glaskanie(self): #itd
        self.zadbanie = min(10, self.zadbanie + 2)
        return wyszukaj_i_konwertuj("petting cat")


    def patrzenie(self):
        self.dostatekuwagi = min(10, self.dostatekuwagi + 2)
        return wyszukaj_i_konwertuj("watching cat")


    def zyje(self):
        return self.najedzenie > 0 and self.zadbanie > 0 and self.dostatekuwagi > 0




    # ponizej metody - wazne wydarzenia 

    def biegunka(self):
        print()
        print(wyszukaj_i_konwertuj("cat shits"))
        historyjka = generuj_historyjke("Napisz krótką, 2-zdaniową historyjkę po polsku tym że kot dostał biegunki. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Zacznij od słowa kot. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.najedzenie = max(0, self.najedzenie - 2) 
 
    def upolowanie_myszy(self):
        print()
        print(wyszukaj_i_konwertuj("cat hunting mouse"))
        historyjka = generuj_historyjke("Napisz krótką, 2-zdaniową historyjkę po polsku tym że kot urządził polowanie na mysz i ją  i zjadł. Zacznij od słowa kot. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.najedzenie = min(10, self.najedzenie + 2)
 
 
    def psia_inwazja(self):
        print()
        print(wyszukaj_i_konwertuj("aggressive dog"))
        historyjka = generuj_historyjke("Napisz krótką, 2-zdaniową historyjkę po polsku tym że kot padł ofiarą agresji pas lub psów. Wyszedł bez uszczerbku fizycznego ale z psychicznym. Nie używaj imion i nie wskazuj na płeć.Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany. Zacznij od słowa kot. ")
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.zadbanie = max(0, self.zadbanie - 2) 

    def dzieci_głaszcza(self):
        print()
        print(wyszukaj_i_konwertuj("children cat"))
        historyjka = generuj_historyjke("Napisz krótką, 3-zdaniową historyjkę po polsku tym że dzieci głaskały lub pogłąskały kota co było dla niego miłe i poczuł się lepiej. Nie używaj imion i nie wskazuj na płeć.Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy ale niech będzie przyjemne. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.zadbanie = min(10, self.zadbanie + 2)


    def smutek(self):
        print()
        print(wyszukaj_i_konwertuj("sad cat"))
        historyjka = generuj_historyjke("Napisz krótką, 2-zdaniową historyjkę po polsku tym że kot poczuł się samotny i smutny. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.dostatekuwagi = max(0, self.dostatekuwagi - 2)

    def spotkanie_kocich_znajomych(self):
        print()
        print(wyszukaj_i_konwertuj("cats meeting"))
        historyjka = generuj_historyjke("Napisz krótką, 2-zdaniową pozytywną historyjkę po polsku tym że kot spotkał swoich  kocich znajomych. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy, ale niech będzie pozytywne. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.dostatekuwagi = min(10, self.dostatekuwagi + 2)


    def szwedanie(self):
        print()
        print(wyszukaj_i_konwertuj("cat wandering"))
        historyjka = generuj_historyjke("Napisz krótką, 1-zdaniową historyjkę o tym że kot się szwęda i nic szczególnego się nie dzieje. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ {historyjka}")
        pass  # ta metoda celowo nic nie robi



    # ponizej metody - drobne wydarzenia

    # zadbanie

    def przeciaganie(self):
        print()
        print(wyszukaj_i_konwertuj("cat stretching"))
        historyjka = generuj_historyjke("Napisz krótką, 1-zdaniową historyjkę po polsku o tym że kot się przeciągnął. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy ale niech to będzie pozytywne. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.zadbanie = min(10, self.zadbanie + 0.25)  

    def upadek_z_krzesla(self):
        print()
        print(wyszukaj_i_konwertuj("cat fall"))
        historyjka = generuj_historyjke("Napisz krótką, 1-zdaniową historyjkę po polsku o tym że niefortunnie kot spadł z mebla. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.zadbanie = max(0, self.zadbanie - 0.25)  

    def mruczenie(self):
        print()
        print(wyszukaj_i_konwertuj("cat purrs"))
        historyjka = generuj_historyjke("Napisz krótką, 1-zdaniową historyjkę po polsku o kocie, który mruczy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy ale niech będzie przyjemne. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.zadbanie = min(10, self.zadbanie + 0.25)  

    def kaslanie(self):
        print()
        print(wyszukaj_i_konwertuj("cat cough"))
        historyjka = generuj_historyjke("Napisz krótką, 1-zdaniową historyjkę po polsku o kocie, który kaszle, lub zakasłał. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.zadbanie = max(0, self.zadbanie - 0.25) 


    # najedzenie

    def upolowanie_muchy(self):
        print()
        print(wyszukaj_i_konwertuj("fly"))
        historyjka = generuj_historyjke("Napisz krótką, 1-zdaniową historyjkę po polsku tym że kot urządził polowanie na muchę i ją upolował a potem zjadł. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany w narracji.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.najedzenie = min(10, self.najedzenie + 0.25)  

    def gonitwa_po_meblach(self):
        print()
        print(wyszukaj_i_konwertuj("cat run"))
        historyjka = generuj_historyjke("Napisz krótką, 2-zdaniową historyjkę po polsku tym że kot urządził sobie gonitwę po meblach. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy.  Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.najedzenie = max(0, self.najedzenie - 0.25) 

    def upolowanie_pajaka(self):
        print()
        print(wyszukaj_i_konwertuj("spider"))
        historyjka = generuj_historyjke("Napisz krótką, 1-zdaniową historyjkę po polsku tym że kot urządził polowanie na pająka i go upolował i zjadł. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.najedzenie = min(10, self.najedzenie + 0.25)  

    def wycieczka_na_dach(self):
        print()
        print(wyszukaj_i_konwertuj("cat roof"))
        historyjka = generuj_historyjke("Napisz krótką, 2-zdaniową historyjkę po polsku o wycieczce kota na dach. Nie używaj imion i nie wskazuj na płeć. Zacznij od słowa kot. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.najedzenie = max(0, self.najedzenie - 0.25) 


    # dostatekuwagi

    def wizyta_kota_sasiada(self):
        print()
        print(wyszukaj_i_konwertuj("2 cats"))
        historyjka = generuj_historyjke("Napisz krótką, 2-zdaniową historyjkę po polsku tym że do kota przyszedł znajomy kot sąsiada. Zacznij od słowa kot. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy, ale niech to będzie pozytywne. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.dostatekuwagi = min(10, self.dostatekuwagi + 0.25)  

    def utkniecie_pod_zlewem(self):
        print()
        print(wyszukaj_i_konwertuj("sink"))
        historyjka = generuj_historyjke("Napisz krótką, 2-zdaniową historyjkę po polsku tym że kot utknął pod zlewem gdzie go nikt nie widział i poczuł się tam trochę samotny. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.dostatekuwagi = max(0, self.dostatekuwagi - 0.25) 

    def spotkanie_z_jezem(self):
        print()
        print(wyszukaj_i_konwertuj("hedgehog"))
        historyjka = generuj_historyjke("Napisz krótką, 2-zdaniową historyjkę po polsku o pozywtywnym spotkaniu kota i znajomego jeża. Nie używaj imion i nie wskazuj na płeć. Zacznij od słowa kot. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy ale niech będzie pozytywne. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.dostatekuwagi = min(10, self.dostatekuwagi + 0.25)  

    def koci_marazm(self):
        print()
        print(wyszukaj_i_konwertuj("lazy cat"))
        historyjka = generuj_historyjke("Napisz krótką, 2-zdaniową historyjkę po polsku tym że kot przeżywa marazm i czuje się rtoche samotny. Nie używaj imion i nie wskazuj na płeć. Zacznij od słowa kot. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ Drobne wydarzenie: \n{historyjka}")
        self.dostatekuwagi = max(0, self.dostatekuwagi - 0.25) 




    #wyswietla menu i aktualizuje stan kota
    def pokaz_stan(self):
        # ponizej konstruowanie licznika czasu gry
        czas_gry = int(time.time() - self.moment_adopcji)  # całkowity czas w sekundach
        minuty = (czas_gry // 60) % 60
        godziny = (czas_gry // 3600) % 24
        dni = czas_gry // 86400
        #ponizej wyswietlanie licznikow
        print(f"""\nNajedzenie:{round(self.najedzenie, 2)} Zadbanie:{round(self.zadbanie, 2)} Dostatek uwagi:{round(self.dostatekuwagi, 2)}""")
        print("Czas opieki:" f"{dni} d. {godziny} h. {minuty} m.")
        print("....................................................")


