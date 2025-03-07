import time #import mehanizmu czasu
import random #import mehanizmu losowego
import os #import komend systemowych
from links.karmione import kotykarmione
from links.glaskane import kotyglaskane
from links.ogladane import kotyogladane
from links.nagrobek import nagrobek

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Cat:
    def __init__(self):
        self.najedzenie = 10
        self.zadbanie = 10
        self.dostatekuwagi = 10

    def karmienie(self):
        self.najedzenie = min(10, self.najedzenie + 2)
        
    def glaskanie(self):
        self.zadbanie = min(10, self.zadbanie + 2)

    def patrzenie(self):
        self.dostatekuwagi = min(10, self.dostatekuwagi + 2)

    def zyje(self):
        return self.najedzenie > 0 and self.zadbanie > 0 and self.dostatekuwagi > 0

    def pokaz_stan(self):
        print(f"\nStan kota:")
        print(f"Najedzenie: {round(self.najedzenie, 2)}")
        print(f"Zadbanie: {round(self.zadbanie, 2)}")
        print(f"Dostatek uwagi: {round(self.dostatekuwagi, 2)}")

def main():
    kot = Cat()
    ostatnia_aktualizacja = time.time()

    while kot.zyje():
      
        # Aktualizacja statystyk za cały miniony czas
        teraz = time.time()
        minuty = int((teraz - ostatnia_aktualizacja) // 60)  # ile minut minęło
        if minuty > 0:
            kot.najedzenie -= minuty / 60  # odejmij 1/60 punktu za każdą minutę
            kot.zadbanie -= minuty / 60
            kot.dostatekuwagi -= minuty / 60
            ostatnia_aktualizacja = teraz

        if not kot.zyje():
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
        
        wybor = input("Wybierz opcję: ")

        clear_screen()

        if wybor == "1":
            kot.karmienie()
            print("\nKarmisz kota")
            print(random.choice(kotykarmione))
        elif wybor == "2":
            kot.glaskanie()
            print("\nGłaszczesz kota")
            print(random.choice(kotyglaskane))


        elif wybor == "3":
            break
        elif wybor == "4":
            kot.patrzenie()
            print("\nWidzisz kota")
            print(random.choice(kotyogladane))



if __name__ == "__main__":
    main()