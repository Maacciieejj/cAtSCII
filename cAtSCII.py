import time #import mehanizmu czasu
import random #import mehanizmu losowego
import os #import komend systemowych
import threading  # import mehanizmu wątków
from links.karmione import kotykarmione #import asci artow
from links.glaskane import kotyglaskane #import asci artow
from links.ogladane import kotyogladane #import asci artow
from links.nagrobek import nagrobek #import asci artow
from links.portret import portret #import asci artow

def clear_screen(): # czysci ekran co petle w wind i linux
    os.system('cls' if os.name == 'nt' else 'clear')

def wydarzenie_losowe(kot): # definicja funkcji wydarzenie_losowe
    while True:
        time.sleep(1200)  # czeka X sekund
        if not kot.zyje():  # sprawdź czy kot żyje przed wydarzeniem
            print("\nTwój kot zmarł!") 
            print(nagrobek)
            break
        wydarzenie = random.choice(["sraczka", "smutek", "upolowanie_muchy", "mycie_futra", "szwędanie", "szwędanie", "szwędanie"])
        getattr(kot, wydarzenie)()  # wywołuje wylosowaną metodę na kocie
        print(f"\n\nWydarzenie losowe:{ wydarzenie}")  # pokazuje co się stało
        kot.pokaz_stan()
        print("\nNaciśnij Enter aby kontynuować...")    

#--------------------------------------------------------


class Cat: 
    def __init__(self): # konstruktor klasy Cat
        self.najedzenie = 10 #Tworzy zmienną przechowującą poziom najedzenia kota. Self oznacza, że zmienna należy do instancji klasy
        self.zadbanie = 10 # podobnie
        self.dostatekuwagi = 10

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
    def sraczka(self):
        self.najedzenie = max(0, self.najedzenie - 2) 
        self.zadbanie = max(0, self.zadbanie - 2) 

    def smutek(self):
        self.dostatekuwagi = max(0, self.dostatekuwagi - 2)

    def upolowanie_muchy(self):
        self.najedzenie = min(10, self.najedzenie + 1)

    def mycie_futra(self):
        self.dostatekuwagi = min(10, self.dostatekuwagi + 1)

    def szwędanie(self):
        pass  # ta metoda celowo nic nie robi


 #wyswietla menu i aktualizuje stan kota
    def pokaz_stan(self):
        print(f"\nStan kota:")
        print(f"Najedzenie: {round(self.najedzenie, 2)}") #pokazuje stan najedzenia do 2 miejsc po przecinku
        print(f"Zadbanie: {round(self.zadbanie, 2)}")
        print(f"Dostatek uwagi: {round(self.dostatekuwagi, 2)}")


#--------------ponizej jest główna funkcja programu ----------


def main():
    # To się wykonuje RAZ na początku programu
    kot = Cat() # tutaj wywołuje się __init__
    print(portret)
    time.sleep(4)  # czeka x sekundy
    clear_screen()
    ostatnia_aktualizacja = time.time()


    # Uruchom wątek wydarzeń losowych
    watek_wydarzen = threading.Thread(target=wydarzenie_losowe, args=(kot,)) #Tworzy nowy wątek i mówi, jaką funkcję ma wykonywać i rzekazuje argumenty do tej funkcj - tu kot
    watek_wydarzen.daemon = True  # wątek zakończy się gdy program się zakończy. "daemon" (usługowy)
    watek_wydarzen.start() #Uruchamia wątek. od tąd działa równolegle z głównym programem


    # While To jest pętla, która się powtarza, tak dlugo jak spelniony jest warunek
    while kot.zyje():
      
        # Aktualizacja statystyk za cały miniony czas
        teraz = time.time()

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
        print("\nCo chcesz zrobić?")
        print("1 - Nakarm kota")
        print("2 - Pogłaszcz kota")
        print("3 - Wyjdź z gry")
        print("4 - Spójrz na kota")
        
        wybor = input("Wybierz opcję: ") #wyswietla linie i zapisuje co wpisał użytkownik

        clear_screen() #wykonanie funkcji clear_screen

# Sprawdzenie wyboru użytkownika
        if wybor == "1":
            kot.karmienie()
            print("\nKarmisz kota")
            print(random.choice(kotykarmione))# wybiera losowo jedną z listy

        elif wybor == "2":
            kot.glaskanie()
            print("\nGłaszczesz kota")
            print(random.choice(kotyglaskane))# wybiera losowo jedną z listy

        elif wybor == "3":
            break

        elif wybor == "4":
            kot.patrzenie()
            print("\nWidzisz kota")
            print(random.choice(kotyogladane))# wybiera losowo jedną z listy


# wywołanie funkcji main (która jest wywoływana tylko gdy plik jest uruchamiany bezpośrednio)
if __name__ == "__main__":
    main()