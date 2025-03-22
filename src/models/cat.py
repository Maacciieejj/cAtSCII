import time
import os  # bibioteka os do czyszczenia ekranu
import json  # Dodajemy import dla obsługi formatu JSON dla sejwowania
import win32api #do wlaczania capslocka debugu prompta dla duckduckgo 
from src.utils.ascii_converter import wyszukaj_i_konwertuj  # import funkcji konwertującej obrazy na ASCII
from src.utils.story_generator import generuj_historyjke, formatuj_do_wyswietlenia  # import funkcji generującej historyjki i formatującej tekst
from links.prompty import *

with open('links/spis_wydarzen.txt', 'r', encoding='utf-8') as file:
    ze_spisu_wydarzen = file.read()

#print(spis_wydarzen) # Wyświetlamy cały tekst

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
            self.dobrostan_emocjonalny = 10 # podobnie
            self.przynaleznosc = 10
            self.moment_adopcji = time.time()  # dodajemy czas startu jako właściwość kota
            self.ostatnia_aktualizacja = time.time()  # to tu ma niby usunac bledy z czasem


    # Nowa metoda do zapisywania stanu gry
    def zapisz_sejw(self):
        dane_sejwu = {
            'najedzenie': self.najedzenie,
            'dobrostan_emocjonalny': self.dobrostan_emocjonalny,
            'przynaleznosc': self.przynaleznosc,
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
            self.dobrostan_emocjonalny = dane_sejwu['dobrostan_emocjonalny']
            self.przynaleznosc = dane_sejwu['przynaleznosc']
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
            log += f"Dobrostan emocjonalny: {round(self.dobrostan_emocjonalny, 2)}, "
            log += f"Przynależność: {round(self.przynaleznosc, 2)}\n"

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
            self.dobrostan_emocjonalny = max(0, self.dobrostan_emocjonalny - spadek)
            self.przynaleznosc = max(0, self.przynaleznosc - spadek)
            self.ostatnia_aktualizacja = teraz



    # ponizej są metody, które zmieniają wartość statystyk kota
    def karmienie(self): # definicja metody karmienie w klasie Cat
        self.najedzenie = min(10, self.najedzenie + 2)
        return wyszukaj_i_konwertuj("feeding cat")  #        # Zwracamy ASCII art zamiast go wyświetlać

        
    def glaskanie(self): #itd
        self.dobrostan_emocjonalny = min(10, self.dobrostan_emocjonalny + 2)
        return wyszukaj_i_konwertuj("petting cat")


    def patrzenie(self):
        self.przynaleznosc = min(10, self.przynaleznosc + 2)
        return wyszukaj_i_konwertuj("watching cat")


    def zyje(self):
        return self.najedzenie > 0 and self.dobrostan_emocjonalny > 0 and self.przynaleznosc > 0


#      _                                               
#  ___| |_ _ __ ___  ___ _______ ___ ______ _  ___ ____
# / __| __| '__/ _ \/ __|_  / __/ __|_  / _` |/ __|_  /
# \__ \ |_| | |  __/\__ \/ / (_| (__ / / (_| | (__ / / 
# |___/\__|_|  \___||___/___\___\___/___\__,_|\___/___|
# To poniżej w epicki sposób zapisuje treść historyjek do pliku spis_wydarzen.txt i po osiągnięciu 80 linijek, piwrwsze 40 linijek zostaje wysłane dostereszczenia do ai, skasowane z pliku, potem streszczenie jest zapisywane na początku pliku a niestreszczeone na końcu pliku. Na końcu dopisana zostaje nowe ydażenie.


    # ponizej metoda zpisu historyjki do spis_wydarzen
    def zapisz_historyjke(self, historyjka):
        # Wyciągamy samą treść historyjki (bez tytułu)
        tresc = historyjka[historyjka.find('**', historyjka.find('**')+2)+2:].strip()

        # Czytamy istniejące historyjki
        with open('links/spis_wydarzen.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Jeśli mamy 80 lub więcej linii
        if len(lines) >= 80:
            # Bierzemy pierwsze 40 linii do streszczenia
            pierwsza_polowa = ''.join(lines[:40])
            # Bierzemy pozostałe linie
            druga_polowa = lines[40:]
            
            # Generujemy streszczenie pierwszej połowy
            prompt_streszczenia = f"Streść poniższe wydarzenia z życia kota w 5 zdaniach, zachowując najważniejsze momenty i stan relacji:\n{pierwsza_polowa}"
            streszczenie = generuj_historyjke(prompt_streszczenia)
            # Wyciągamy samą treść streszczenia bez tytułu
            streszczenie = streszczenie.strip()
            
            # Zapisujemy: streszczenie + druga połowa + nowa historyjka
            with open('links/spis_wydarzen.txt', 'w', encoding='utf-8') as file:
                file.write(f"Streszczenie wcześniejszych wydarzeń: {streszczenie} Kolejne wydarzenia:\n")
                file.writelines(druga_polowa)
                file.write(f"\n{tresc}")
        else:
            # Jeśli mniej niż 80 linii, po prostu dopisujemy nową historyjkę
            with open('links/spis_wydarzen.txt', 'a', encoding='utf-8') as file:
                file.write(f"\n{tresc}")


# __        ____        ____        ____        ____        __
# \ \      / /\ \      / /\ \      / /\ \      / /\ \      / /
#  \ \    / /  \ \    / /  \ \    / /  \ \    / /  \ \    / / 
#   \ \  / /    \ \  / /    \ \  / /    \ \  / /    \ \  / /  
#    \_\/_/      \_\/_/      \_\/_/      \_\/_/      \_\/_/   



    def get_prompt_stats(self):   # to tworzy prompt z aktualnymi statystykami kota (do 2 miejsc po przecinku)
        return f" W tym momencie kot ma 'najedzenie': {round(self.najedzenie, 2)}, 'dobrostan emocjonalny':{round(self.dobrostan_emocjonalny, 2)}, 'przynaleznosc': {round(self.przynaleznosc, 2)}. " 
    


    #ponizej - kawalek kodu co sie powtarza się w każdej z metod poniżej wiec jest zapisany jako metoda. po rostu skompresowany kawalek kodu
    def kawalek_kodu_wydarzenwydarzen(self, historyjka, waga=""):
        # Wyciągamy tytuł i generujemy ASCII art
        tytul = self.wyciagnij_tytul(historyjka)
        if win32api.GetKeyState(0x14):  # Sprawdza czy Caps Lock jest włączony
            print("Debug frazy. Wyłącz capslock "), print(f"cat and {tytul}")
        ascii_art = wyszukaj_i_konwertuj(f"cat and {tytul}")
        # Teraz wyświetlamy w odpowiedniej kolejności
        print(ascii_art)
        tekst_do_wyswietlenia = historyjka[historyjka.find('**', historyjka.find('**')+2)+2:] #polamany text z  story_generator
        print(f"↑ {waga} wydarzenie: \n{formatuj_do_wyswietlenia(tekst_do_wyswietlenia)}") # Wyświetla tekst po drugim **
        self.zapisz_historyjke(historyjka)  # Zapisujemy historyjkę do pliku


#      _           _                                     _                          _       
#   __| |_ __ ___ | |__  _ __   ___  __      ___   _  __| | __ _ _ __ _______ _ __ (_) __ _ 
#  / _` | '__/ _ \| '_ \| '_ \ / _ \ \ \ /\ / / | | |/ _` |/ _` | '__|_  / _ \ '_ \| |/ _` |
# | (_| | | | (_) | |_) | | | |  __/  \ V  V /| |_| | (_| | (_| | |   / /  __/ | | | | (_| |
#  \__,_|_|  \___/|_.__/|_| |_|\___|   \_/\_/  \__, |\__,_|\__,_|_|  /___\___|_| |_|_|\__,_|
#                                              |___/        


    # dobrostan_emocjonalny

    def dobrostan_emo_up(self):#drobne DEBUGOWANE POD D <<<******
        print()
        #### DEBUG PONIZEJ zakomentowany
        #print("DEBUG PROMPT:         ", prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " zyskał 0,25 Dobrostanu emocjonalnego.  " + prompt4)
        # Najpierw generujemy historyjkę, ale jej nie wyświetlamy
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " zyskał 0,25 Dobrostanu emocjonalnego.  " + prompt4)     
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Drobne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.dobrostan_emocjonalny = min(10, self.dobrostan_emocjonalny + 0.25)  

                
    def dobrostan_emo_down(self):#drobne
        print()
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " utracił 0,25 Dobrostanu emocjonalnego.  " + prompt4)      
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Drobne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.dobrostan_emocjonalny = max(0, self.dobrostan_emocjonalny - 0.25)  
  
  
    # najedzenie

    def najedz_up(self):#drobne
        print()
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " zyskał 0,25  Najedzenia.  " + prompt4)
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Drobne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.najedzenie = min(10, self.najedzenie + 0.25)  

    def najedz_down(self):#drobne
        print()
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " utracił 0,25 Najedzenia.  " + prompt4)
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Drobne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.najedzenie = max(0, self.najedzenie - 0.25) 

  

    # przynaleznosc

    def przynalez_up(self): #drobne
        print()
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " zyskał 0,25 Przynależności.  " + prompt4)
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Drobne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.przynaleznosc = min(10, self.przynaleznosc + 0.25)  

    def przynalez_down(self): #drobne
        print()
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " utracił 0,25  Przynależności.  " + prompt4)     
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Drobne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.przynaleznosc = max(0, self.przynaleznosc - 0.25) 


#                                                    _ 
# __      ____ _ _____ __   ___  __      ___   _  __| |
# \ \ /\ / / _` |_  / '_ \ / _ \ \ \ /\ / / | | |/ _` |
#  \ V  V / (_| |/ /| | | |  __/  \ V  V /| |_| | (_| |
#   \_/\_/ \__,_/___|_| |_|\___|   \_/\_/  \__, |\__,_|
#                                          |___/       

    # najedzenie

    def najedz_down2(self): #Wazne
        print()
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " utracił aż 2 pkt  Najedzenia.  " + prompt4)
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Ważne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.najedzenie = max(0, self.najedzenie - 2) 
 
    def najedz_up2(self): #Wazne
        print()
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " zyskał aż 2 pkt  Najedzenia.  " + prompt4)
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Ważne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.najedzenie = min(10, self.najedzenie + 2)
 
    # dobrostan_emocjonalny

    def dobrostan_emo_down2(self): #Wazne
        print()
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " utracił aż 2 pkt Dobrostanu emocjonalnego.  " + prompt4)
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Ważne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.dobrostan_emocjonalny = max(0, self.dobrostan_emocjonalny - 2) 

    def dobrostan_emo_up2(self): #Wazne
        print()
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " zyskał aż 2 pkt Dobrostanu emocjonalnego.  " + prompt4)
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Ważne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.dobrostan_emocjonalny = min(10, self.dobrostan_emocjonalny + 2)


    # przynaleznosc


    def przynalez_down2(self): #Wazne
        print()
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " stracił aż 2 pkt Przynależności.  " + prompt4)
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Ważne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.przynaleznosc = max(0, self.przynaleznosc - 2)


    def przynalez_up2(self):#Wazne
        print()
        historyjka = generuj_historyjke(prompt1 +" " +ze_spisu_wydarzen +" "+prompt2+  self.get_prompt_stats() + prompt3 + " zyskał aż 2 pkt Przynależności.  " + prompt4)
        self.kawalek_kodu_wydarzenwydarzen(historyjka, "Ważne") #skompresowany kawalek kodu co sie powtarza w wydarzeniach
        self.przynaleznosc = min(10, self.przynaleznosc + 2)






#-------------------------------------------------------------------------------------------------------


    #wyswietla menu i aktualizuje stan kota
    def pokaz_stan(self):
        # ponizej konstruowanie licznika czasu gry
        czas_gry = int(time.time() - self.moment_adopcji)  # całkowity czas w sekundach
        minuty = (czas_gry // 60) % 60
        godziny = (czas_gry // 3600) % 24
        dni = czas_gry // 86400
        #ponizej wyswietlanie licznikow
        print(f"""\nNajedzenie:{round(self.najedzenie, 2)} Dobrostan emocjonalny:{round(self.dobrostan_emocjonalny, 2)} Przynaleznosc:{round(self.przynaleznosc, 2)}""")
        print("Czas opieki:" f"{dni} d. {godziny} h. {minuty} m.")
        print("....................................................")


