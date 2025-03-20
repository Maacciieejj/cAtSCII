import time
import os  # bibioteka os do czyszczenia ekranu
import json  # Dodajemy import dla obsługi formatu JSON dla sejwowania
from src.utils.story_generator import generuj_historyjke  # import funkcji generującej historyjki
from src.utils.ascii_converter import wyszukaj_i_konwertuj  # import funkcji konwertującej obrazy na ASCII
from links.prompty import *

#   |\---/|
#   | o_o |
#    \_^_/

# poiżej klasa Cat -----------------------------------


class Cat: 


    def wyciagnij_tytul(self, historyjka):
        return historyjka[historyjka.find("**")+2:historyjka.find("**", historyjka.find("**")+2)]


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

    # najedzenie

    def najedz_down2(self):
        print()
        print(wyszukaj_i_konwertuj("cat shits"))
        historyjka = generuj_historyjke(prompt1 + " najedzenie (sytość) " + prompt2 + " utracił aż 2 " + prompt3)
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.najedzenie = max(0, self.najedzenie - 2) 
 
    def najedz_up2(self):
        print()
        print(wyszukaj_i_konwertuj("cat hunting mouse"))
        historyjka = generuj_historyjke(prompt1 + " najedzenie (sytość) " + prompt2 + " zyskał aż 2 " + prompt3)
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.najedzenie = min(10, self.najedzenie + 2)
 
    # zadbanie

    def zadb_down2(self):
        print()
        print(wyszukaj_i_konwertuj("aggressive dog"))
        historyjka = generuj_historyjke(prompt1 + " dobrostan psychiczny " + prompt2 + " utracił aż 2 " + prompt3)
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.zadbanie = max(0, self.zadbanie - 2) 

    def zadb_up2(self):
        print()
        print(wyszukaj_i_konwertuj("children cat"))
        historyjka = generuj_historyjke(prompt1 + " dobrostan psychiczny " + prompt2 + " zyskał aż 2 " + prompt3)
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.zadbanie = min(10, self.zadbanie + 2)


    # dostatek uwagi


    def dostatekuw_down2(self):
        print()
        print(wyszukaj_i_konwertuj("sad cat"))
        historyjka = generuj_historyjke(prompt1 + " przynależność społeczna (im jest niższa ta statystyka tym bardziej kot czuje sie samotny) " + prompt2 + " utracił aż 2 " + prompt3)
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.dostatekuwagi = max(0, self.dostatekuwagi - 2)


    def dostatekuw_up2(self):
        print()
        print(wyszukaj_i_konwertuj("cats meeting"))
        historyjka = generuj_historyjke(prompt1 + " przynależność społeczna (im jest niższa ta statystyka tym bardziej kot czuje sie samotny) " + prompt2 + " zyskał aż 2 " + prompt3)
        print(f"↑ WAŻNE WYDARZENIE: \n{historyjka}")
        self.dostatekuwagi = min(10, self.dostatekuwagi + 2)


    def szwedanie(self):
        print()
        print(wyszukaj_i_konwertuj("cat wandering"))
        historyjka = generuj_historyjke("Napisz krótką, 1-zdaniową historyjkę o tym że kot się szwęda i nic szczególnego się nie dzieje. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
        print(f"↑ {historyjka}")
        pass  # ta metoda celowo nic nie robi



    # ponizej metody - drobne wydarzenia***************************************************

    # zadbanie

    def zadb_up(self):
        print()
        # Najpierw generujemy historyjkę, ale jej nie wyświetlamy
        historyjka = generuj_historyjke(prompt1 + " dobrostan psychiczny " + prompt2 + " zyskał 0,25 " + prompt3)
        # Wyciągamy tytuł i generujemy ASCII art
        tytul = self.wyciagnij_tytul(historyjka)
        ascii_art = wyszukaj_i_konwertuj(f"kot i {tytul}")
        # Teraz wyświetlamy w odpowiedniej kolejności
        print(ascii_art)
        print(f"↑ Drobne wydarzenie: \n{historyjka[historyjka.find('**', historyjka.find('**')+2)+2:]}") # Wyświetla tekst po drugim **
        self.zadbanie = min(10, self.zadbanie + 0.25)  

                
    def zadb_down(self):
        print()
        historyjka = generuj_historyjke(prompt1 + " dobrostan psychiczny " + prompt2 + " utracił 0,25 " + prompt3)
        tytul = self.wyciagnij_tytul(historyjka)
        ascii_art = wyszukaj_i_konwertuj(f"kot i {tytul}")
        print(ascii_art)
        print(f"↑ Drobne wydarzenie: \n{historyjka[historyjka.find('**', historyjka.find('**')+2)+2:]}") # Wyświetla tekst po drugim **
        self.zadbanie = max(0, self.zadbanie - 0.25)  
  


    # najedzenie

    def najedz_up(self):
        print()
        historyjka = generuj_historyjke(prompt1 + " najedzenie (sytość) " + prompt2 + " zyskał 0,25 " + prompt3)
        tytul = self.wyciagnij_tytul(historyjka)
        ascii_art = wyszukaj_i_konwertuj(f"kot i {tytul}")
        print(ascii_art)
        print(f"↑ Drobne wydarzenie: \n{historyjka[historyjka.find('**', historyjka.find('**')+2)+2:]}") # Wyświetla tekst po drugim **
        self.najedzenie = min(10, self.najedzenie + 0.25)  

    def najedz_down(self):
        print()
        historyjka = generuj_historyjke(prompt1 + " najedzenie (sytość) " + prompt2 + " utracił 0,25 " + prompt3)
        tytul = self.wyciagnij_tytul(historyjka)
        ascii_art = wyszukaj_i_konwertuj(f"kot i {tytul}")
        print(ascii_art)
        print(f"↑ Drobne wydarzenie: \n{historyjka[historyjka.find('**', historyjka.find('**')+2)+2:]}") # Wyświetla tekst po drugim **
        self.najedzenie = max(0, self.najedzenie - 0.25) 

  

    # dostatekuwagi

    def dostatekuw_up(self):
        print()
        historyjka = generuj_historyjke(prompt1 + " przynależność społeczna (im jest niższa ta statystyka tym bardziej kot czuje sie samotny) " + prompt2 + " zyskał 0,25 " + prompt3)
        tytul = self.wyciagnij_tytul(historyjka)
        ascii_art = wyszukaj_i_konwertuj(f"kot i {tytul}")
        print(ascii_art)
        print(f"↑ Drobne wydarzenie: \n{historyjka[historyjka.find('**', historyjka.find('**')+2)+2:]}") # Wyświetla tekst po drugim **
        self.dostatekuwagi = min(10, self.dostatekuwagi + 0.25)  

    def dostatekuw_down(self):
        print()
        historyjka = generuj_historyjke(prompt1 + " przynależność społeczna (im jest niższa ta statystyka tym bardziej kot czuje sie samotny) " + prompt2 + " utracił 0,25 " + prompt3)
        tytul = self.wyciagnij_tytul(historyjka)
        ascii_art = wyszukaj_i_konwertuj(f"kot i {tytul}")
        print(ascii_art)
        print(f"↑ Drobne wydarzenie: \n{historyjka[historyjka.find('**', historyjka.find('**')+2)+2:]}") # Wyświetla tekst po drugim **
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


