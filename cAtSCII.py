import time #import mehanizmu czasu
import random #import mehanizmu losowego
import threading  # import mehanizmu wątków
import os  # bibioteka os do czyszczenia ekranu
from links.karmione import kotykarmione #import asci artow
from links.glaskane import kotyglaskane #import asci artow
from links.ogladane import kotyogladane #import asci artow
from links.nagrobek import nagrobek #import asci artow
from links.portret import portret #import asci artow

def clear_screen(): #  czyszczenie ekran startowy
    os.system('cls' if os.name == 'nt' else 'clear')

def wydarzenie_losowe(kot): # definicja funkcji wydarzenie_losowe
    ostatnia_aktualizacja = time.time() # aktualizacja czasu ostatniej aktualizacji by pokazywaly sie aktualne statsy podczas wydarzen losowych
    while True:
        czas_oczekiwania = random.choice([300, 600, 600, 900, 900, 1200, 1500])  # losuje czas oczekiwania w sekundach
        time.sleep(czas_oczekiwania)  # czeka wylosowaną liczbę sekund

# aktualizacja statsow przed wydarzeniami
        teraz = time.time()
        minuty = int((teraz - ostatnia_aktualizacja) // 60)
        if minuty > 0:
            kot.najedzenie -= minuty / 60
            kot.zadbanie -= minuty / 60
            kot.dostatekuwagi -= minuty / 60
            ostatnia_aktualizacja = teraz

        if not kot.zyje():  # sprawdź czy kot żyje przed wydarzeniem
            print("\nTwój kot zmarł!") 
            print(nagrobek)
            break
        wydarzenie = random.choice(["biegunka", "smutek", "upolowanie_muchy", "spotkanie_kocich_znajomych", "spotkanie_kocich_znajomych", "szwędanie", "szwędanie", "szwędanie"])
        getattr(kot, wydarzenie)()  # wywołuje wylosowaną metodę na kocie
        print(f"\n\nWydarzenie losowe:{ wydarzenie}")  # pokazuje co się stało
        kot.zapisz_log(f"Wydarzenie losowe: {wydarzenie}") # zapisuje log
        kot.pokaz_stan()
        print("(enter)")    

#--------------------------------------------------------


class Cat: 
    #poniżej konstruktor klasy Cat
    def __init__(self): # konstruktor klasy Cat
        self.najedzenie = 10 #Tworzy zmienną przechowującą poziom najedzenia kota. Self oznacza, że zmienna należy do instancji klasy
        self.zadbanie = 10 # podobnie
        self.dostatekuwagi = 10
        self.moment_adopcji = time.time()  # dodajemy czas startu jako właściwość kota

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


# ponizej są metody, które zmieniają wartość statystyk kota
    def karmienie(self): # definicja metody karmienie w klasie Cat
        self.najedzenie = min(10, self.najedzenie + 2)
        
    def glaskanie(self): #itd
        self.zadbanie = min(10, self.zadbanie + 2)

    def patrzenie(self):
        self.dostatekuwagi = min(10, self.dostatekuwagi + 2)

    def zyje(self):
        return self.najedzenie > 0 and self.zadbanie > 0 and self.dostatekuwagi > 0

# ponizej metody - wydarzenia losowe
    def biegunka(self):
        self.najedzenie = max(0, self.najedzenie - 2) 
        self.zadbanie = max(0, self.zadbanie - 2) 

    def smutek(self):
        self.dostatekuwagi = max(0, self.dostatekuwagi - 2)

    def upolowanie_muchy(self):
        self.najedzenie = min(10, self.najedzenie + 1)

    #def mycie_futra(self): wyłączone
        #self.dostatekuwagi = min(10, self.dostatekuwagi + 1) wyłączone

    def szwędanie(self):
        pass  # ta metoda celowo nic nie robi

    def spotkanie_kocich_znajomych(self):
        self.dostatekuwagi = min(10, self.dostatekuwagi + 1)


 #wyswietla menu i aktualizuje stan kota
    def pokaz_stan(self):
        # ponizej konstruowanie licznika czasu gry
        czas_gry = int(time.time() - self.moment_adopcji)  # całkowity czas w sekundach
        minuty = (czas_gry // 60) % 60
        godziny = (czas_gry // 3600) % 24
        dni = czas_gry // 86400
        #ponizej wyswietlanie licznikow
        print(f"\nStan kota:")
        print(f"Najedzenie: {round(self.najedzenie, 2)}") #pokazuje stan najedzenia do 2 miejsc po przecinku
        print(f"Zadbanie: {round(self.zadbanie, 2)}")
        print(f"Dostatek uwagi: {round(self.dostatekuwagi, 2)}")
        print("Czas opieki:")
        print(f"{dni} d. {godziny} h. {minuty} m.")




#--------------ponizej jest główna funkcja programu ----------


def main():
    # To się wykonuje RAZ na początku programu
    kot = Cat() # tutaj wywołuje się __init__
    print(portret)
    time.sleep(4)  # czeka x sekundy
    clear_screen() #-  czyszczenie ekranu startoweego
    ostatnia_aktualizacja = time.time()


    # Uruchom wątek wydarzeń losowych
    watek_wydarzen = threading.Thread(target=wydarzenie_losowe, args=(kot,)) #Tworzy nowy wątek i mówi, jaką funkcję ma wykonywać i rzekazuje argumenty do tej funkcj - tu kot
    watek_wydarzen.daemon = True  # wątek zakończy się gdy program się zakończy. "daemon" (usługowy)
    watek_wydarzen.start() #Uruchamia wątek. od tąd działa równolegle z głównym programem


    # While To jest pętla, która się powtarza, tak dlugo jak spelniony jest warunek
    while kot.zyje():
      
        # Aktualizacja statystyk za cały miniony czas
        teraz = time.time()

        teraz = time.time() #aktualizacja czasu by pokazywaly się aktualne statystyki pod wydarzeniami losowymi
        minuty = int((teraz - ostatnia_aktualizacja) // 60)  # ile minut minęło - dotyczy opadania statystyk
        if minuty > 0:
            kot.najedzenie -= minuty / 60  # odejmij 1/60 punktu za każdą minutę
            kot.zadbanie -= minuty / 60
            kot.dostatekuwagi -= minuty / 60
            ostatnia_aktualizacja = teraz #???

        if not kot.zyje(): #jesli zyje jest false to wyświetla się to
            print("\nTwój kot zmarł!") 
            print(nagrobek)
            break


        # Wyświetl stan i menu
        kot.pokaz_stan()
        print("\n1 - Nakarm kota")
        print("2 - Pogłaszcz kota")
        print("3 - Spójrz na kota")
        print("0 - Wyjdź z gry")
        
        wybor = input("?: ") #wyswietla linie i zapisuje co wpisał użytkownik

        # clear_screen() - - wylaczone czyszczenie ekranu

# Sprawdzenie wyboru użytkownika
        if wybor == "1":
            kot.karmienie()
            kot.zapisz_log("Akcja: Karmienie kota") #zapis logu
            print(random.choice(kotykarmione))# wybiera losowo jedną z listy
            print("\nKarmisz kota")

        elif wybor == "2":
            kot.glaskanie()
            kot.zapisz_log("Akcja: Głaskanie kota") #zapis logu
            print(random.choice(kotyglaskane))# wybiera losowo jedną z listy
            print("\nGłaszczesz kota")


        elif wybor == "0":
            break

        elif wybor == "3":
            kot.patrzenie()
            kot.zapisz_log("Akcja: Patrzenie na kota") #zapis logu
            print(random.choice(kotyogladane))# wybiera losowo jedną z listy
            print("\nWidzisz kota")



# wywołanie funkcji main (która jest wywoływana tylko gdy plik jest uruchamiany bezpośrednio)
if __name__ == "__main__":
    main()