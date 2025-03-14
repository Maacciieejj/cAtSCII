import time #import mehanizmu czasu
import random #import mehanizmu losowego
import threading  # import mehanizmu wątków
import os  # bibioteka os do czyszczenia ekranu
from links.karmione import kotykarmione #import asci artow
from links.glaskane import kotyglaskane #import asci artow
from links.ogladane import kotyogladane #import asci artow
from links.nagrobek import nagrobek #import asci artow
from links.portret import portret #import asci arto
from links.ASCIIdrobne_wydarzenia import *
from links.ASCIIwazne_wydarzenia import *
from links.ASCIIinne import *
import sys  # by zapisywaz zawartosc konsoli  TeeOutput:
przelacznik1 = False #przełącznik, który pozwala na włączanie i wyłączanie wątku wydarzeń losowych

# ponizej funkcja zapisuje zawartość konsoli do pliku
class TeeOutput:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, 'a', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)
        self.logfile.flush()

    def flush(self):
        self.terminal.flush()
        self.logfile.flush()

sys.stdout = TeeOutput('zawartosc.txt')


# ponizej definicja funkcji wazne wydarzenia uruchamianej w wątku dodatkowym

def wazne_wydarzenia(kot): # definicja funkcji 
    global przelacznik1  # deklarujemy użycie zmiennej globalnej
    
    while True:
        if przelacznik1: # jeśli przełącznik włączony, czekamy w pierwszej pętli (sen)
            time.sleep(2)
            continue

        czas_oczekiwania = random.choice([600, 900, 900, 1200, 1500])  # losuje czas oczekiwania w sekundach

        # zamiast jednego długiego czekania, dzielimy je na sekundowe interwały i co sekunde sprawdzamy czy nie włączylismy kociego spanka
        for _ in range(czas_oczekiwania): #tworzy pętlę, która będzie wykonywać się tyle razy, ile wynosi wartość czas_oczekiwania
            if przelacznik1:  # sprawdzamy przełącznik co 1 sekunde
                break  # jeśli włączony, przerywamy czekanie
            time.sleep(1)           
        if przelacznik1:  # jeśli przełącznik został włączony, wracamy na początek głównej pętli
            continue
        

        kot.aktualizuj_statystyki() # aktualizacja statsow przed wydarzeniami


        if not kot.zyje():  # sprawdź czy kot żyje przed wydarzeniem
            print("\nTwój kot zmarł!") 
            print(nagrobek)
            kot.zapisz_log("R. I. P.") #zapis logu
            break

        wydarzenie = random.choice(["biegunka", "smutek", "upolowanie_myszy", "spotkanie_kocich_znajomych", "psia_inwazja", "dzieci_głaszcza", "szwedanie"]) # losowanie wydarzenia
        getattr(kot, wydarzenie)()  # Wywołuje metodę o nazwie wylosowanego wydarzenia na obiekcie kot . Na przykład, jeśli wylosowano "biegunka", to wykona się kot.biegunka()
        print(f"↑ WAŻNE WYDARZENIE: {wydarzenie}")  # pokazuje co się stało
        kot.zapisz_log(f"WAŻNE WYDARZENIE: {wydarzenie}") # zapisuje log
        kot.pokaz_stan()
        print("(Menu: enter)")


# ponizej definicja funkcji drobnych wydarzeń uruchamianej w wątku dodatkowym

def drobne_wydarzenia(kot): # definicja funkcji 
    global przelacznik1  # deklarujemy użycie zmiennej globalnej
    
    
    while True:
        if przelacznik1: # jeśli przełącznik włączony, czekamy w pierwszej pętli (sen)
            time.sleep(2)
            continue

        czas_oczekiwania = random.choice([120, 120, 120, 120, 120, 120, 60, 60, 60, 60, 180, 180, 300, 300, 10])  # losuje czas oczekiwania w sekundach
        
        # zamiast jednego długiego czekania, dzielimy je na sekundowe interwały i co sekunde sprawdzamy czy nie włączylismy kociego spanka
        for _ in range(czas_oczekiwania): #tworzy pętlę, która będzie wykonywać się tyle razy, ile wynosi wartość czas_oczekiwania
            if przelacznik1:  # sprawdzamy przełącznik co 1 sekunde
                break  # jeśli włączony, przerywamy czekanie
            time.sleep(1)           
        if przelacznik1:  # jeśli przełącznik został włączony, wracamy na początek głównej pętli
            continue


        kot.aktualizuj_statystyki() # aktualizacja statsow przed wydarzeniami


        if not kot.zyje():  # sprawdź czy kot żyje przed wydarzeniem
            print("\nTwój kot zmarł!") 
            print(nagrobek)
            kot.zapisz_log("R. I. P.") #zapis logu
            break

        wydarzenie = random.choice(["szwedanie","przeciaganie", "upadek_z_krzesla", "mruczenie", "kaslanie", "upolowanie_muchy", "gonitwa_po_meblach", "upolowanie_pajaka", "wycieczka_na_dach", "wizyta_kota_sasiada", "utkniecie_pod_zlewem", "spotkanie_z_jezem", "koci_marazm"]) # losowanie wydarzenia
        getattr(kot, wydarzenie)()  # Wywołuje metodę o nazwie wylosowanego wydarzenia na obiekcie kot . Na przykład, jeśli wylosowano "biegunka", to wykona się kot.biegunka()
        print(f"↑ Drobne wydarzenie:{ wydarzenie}")  # pokazuje co się stało
        kot.zapisz_log(f"Drobne wydarzenie:{ wydarzenie}") # zapisuje log
        kot.pokaz_stan()
        print("(Menu: enter)")



#   |\---/|
#   | o_o |
#    \_^_/

# poiżej klasa Cat -----------------------------------


class Cat: 



    #poniżej konstruktor klasy Cat
    def __init__(self): # konstruktor klasy Cat
        self.najedzenie = 10 #Tworzy zmienną przechowującą poziom najedzenia kota. Self oznacza, że zmienna należy do instancji klasy
        self.zadbanie = 10 # podobnie
        self.dostatekuwagi = 10
        self.moment_adopcji = time.time()  # dodajemy czas startu jako właściwość kota
        self.ostatnia_aktualizacja = time.time()  # to tu ma niby usunac bledy z czasem



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
        
    def glaskanie(self): #itd
        self.zadbanie = min(10, self.zadbanie + 2)

    def patrzenie(self):
        self.dostatekuwagi = min(10, self.dostatekuwagi + 2)

    def zyje(self):
        return self.najedzenie > 0 and self.zadbanie > 0 and self.dostatekuwagi > 0




    # ponizej metody - wazne wydarzenia 

    def biegunka(self):
        print(random.choice(ASCIIbiegunka))  # wybiera losowo jeden art
        self.najedzenie = max(0, self.najedzenie - 2) 
 
    def upolowanie_myszy(self):
        print(random.choice(ASCIIupolowanie_myszy))  # wybiera losowo jeden art
        self.najedzenie = min(10, self.najedzenie + 2)
 
 
    def psia_inwazja(self):
        print(random.choice(ASCIIpsia_inwazja))  # wybiera losowo jeden art
        self.zadbanie = max(0, self.zadbanie - 2) 

    def dzieci_głaszcza(self):
        print(random.choice(ASCIIdzieci_głaszcza))  # wybiera losowo jeden art
        self.zadbanie = min(10, self.zadbanie + 2)


    def smutek(self):
        print(random.choice(ASCIIsmutek))  # wybiera losowo jeden art
        self.dostatekuwagi = max(0, self.dostatekuwagi - 2)

    def spotkanie_kocich_znajomych(self):
        print(random.choice(ASCIIspotkanie_kocich_znajomych))  # wybiera losowo jeden art
        self.dostatekuwagi = min(10, self.dostatekuwagi + 2)


    def szwedanie(self):
        print(random.choice(ASCIIszwedanie))  # wybiera losowo jeden art ze szwedania
        pass  # ta metoda celowo nic nie robi



    # ponizej metody - drobne wydarzenia

    # zadbanie

    def przeciaganie(self):
        print(random.choice(ASCIIprzeciaganie))  # wybiera losowo jeden art
        self.zadbanie = min(10, self.zadbanie + 0.25)  

    def upadek_z_krzesla(self):
        print(random.choice(ASCIIupadek_z_krzesla))  # wybiera losowo jeden art
        self.zadbanie = max(0, self.zadbanie - 0.25)  

    def mruczenie(self):
        print(random.choice(ASCIImruczenie))  # wybiera losowo jeden art
        self.zadbanie = min(10, self.zadbanie + 0.25)  

    def kaslanie(self):
        print(random.choice(ASCIIkaslanie))  # wybiera losowo jeden art
        self.zadbanie = max(0, self.zadbanie - 0.25) 


    # najedzenie

    def upolowanie_muchy(self):
        print(random.choice(ASCIIupolowanie_muchy))  # wybiera losowo jeden art
        self.najedzenie = min(10, self.najedzenie + 0.25)  

    def gonitwa_po_meblach(self):
        print(random.choice(ASCIIgonitwa_po_meblach))  # wybiera losowo jeden art
        self.najedzenie = max(0, self.najedzenie - 0.25) 

    def upolowanie_pajaka(self):
        print(random.choice(ASCIIupolowanie_pajaka))  # wybiera losowo jeden art
        self.najedzenie = min(10, self.najedzenie + 0.25)  

    def wycieczka_na_dach(self):
        print(random.choice(ASCIIwycieczka_na_dach))  # wybiera losowo jeden art
        self.najedzenie = max(0, self.najedzenie - 0.25) 


    # dostatekuwagi

    def wizyta_kota_sasiada(self):
        print(random.choice(ASCIIwizyta_kota_sasiada))  # wybiera losowo jeden art
        self.dostatekuwagi = min(10, self.dostatekuwagi + 0.25)  

    def utkniecie_pod_zlewem(self):
        print(random.choice(ASCIIutkniecie_pod_zlewem))  # wybiera losowo jeden art
        self.dostatekuwagi = max(0, self.dostatekuwagi - 0.25) 

    def spotkanie_z_jezem(self):
        print(random.choice(ASCIIspotkanie_z_jezem))  # wybiera losowo jeden art
        self.dostatekuwagi = min(10, self.dostatekuwagi + 0.25)  

    def koci_marazm(self):
        print(random.choice(ASCIIkoci_marazm))  # wybiera losowo jeden art
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





#--------------ponizej jest GŁÓWNA FUNKCJA PROGRAMU -----------------------------



def main():
    
    global przelacznik1 #deklaracja uzycia

    # To się wykonuje RAZ na początku programu
    kot = Cat() # tutaj wywołuje się __init__
    print(portret)
    time.sleep(4)  # czeka x sekundy
    # clear_screen() #-  wyłączoneczyszczenie ekranu startoweego



    # Ponizej wątki - funkcje, które będą działać równolegle z główną funkcją programu

    # Uruchom WĄTEK wydarzeń losowych
    watek_waznych = threading.Thread(target=wazne_wydarzenia, args=(kot,)) #Tworzy nowy wątek i mówi, jaką funkcję ma wykonywać i rzekazuje argumenty do tej funkcj - tu kot
    watek_waznych.daemon = True  # wątek zakończy się gdy program się zakończy. "daemon" (usługowy)
    watek_waznych.start() #Uruchamia wątek. od tąd działa równolegle z głównym programem


    # Uruchom WĄTEK drobnych wydarzeń
    watek_drobnych = threading.Thread(target=drobne_wydarzenia, args=(kot,)) #Tworzy nowy wątek i mówi, jaką funkcję ma wykonywać i rzekazuje argumenty do tej funkcj - tu kot
    watek_drobnych.daemon = True  # wątek zakończy się gdy program się zakończy. "daemon" (usługowy)
    watek_drobnych.start() #Uruchamia wątek. od tąd działa równolegle z głównym programem





    # ----- JAKBY GŁÓWNA PETLA PROGRAMU ---- , While To jest pętla, która się powtarza, tak dlugo jak spelniony jest warunek

    while kot.zyje():
      


        kot.aktualizuj_statystyki() # aktualizacja statsow przed wydarzeniami


        if not kot.zyje(): #jesli zyje jest false to wyświetla się to
            print("\nTwój kot zmarł!") 
            print(nagrobek)
            kot.zapisz_log("R. I. P.") #zapis logu
            break



        # Wyświetl stan i menu
        kot.pokaz_stan()
        if przelacznik1:
            print("\nKot śpi. By go obudzić wpisz 4")
        else:
            print("\n1 - Nakarm kota")
            print("2 - Pogłaszcz kota")
            print("3 - Spójrz na kota")
            print("4 - Połóż kota spać")
            print("h - Help")
            print("0 - Wyjdź z gry")
        
        wybor = input("?: ") #wyswietla linie i zapisuje co wpisał użytkownik




        # Sprawdzenie wyboru użytkownika
        if wybor == "1":
            kot.karmienie()
            kot.zapisz_log("Akcja: Karmienie kota") #zapis logu
            print(random.choice(kotykarmione))# wybiera losowo jedną z listy
            print("↑ Karmisz kota")

        elif wybor == "2":
            kot.glaskanie()
            kot.zapisz_log("Akcja: Głaskanie kota") #zapis logu
            print(random.choice(kotyglaskane))# wybiera losowo jedną z listy
            print("↑ Głaszczesz kota")


        elif wybor == "0":
            break

        elif wybor == "3":
            kot.patrzenie()
            kot.zapisz_log("Akcja: Patrzenie na kota") #zapis logu
            print(random.choice(kotyogladane))# wybiera losowo jedną z listy
            print("↑ Widzisz kota")

        elif wybor == "4":            
            przelacznik1 = not przelacznik1  # zmienia wartość na przeciwną
            print((random.choice(ASCIIzasypia))if przelacznik1 else(random.choice(ASCIIsiebudzi)))# wybiera losowo jedną z listy
            print(f"Kot {'zasypia' if przelacznik1 else 'się budzi'}")
            kot.zapisz_log("Kot zasypia" if przelacznik1 else "Kot się budzi") #zapis logu

        elif wybor == "h":
            print("""
\nObserwuj jak żyje twój kot. Dbaj o niego, karmiąc, 
głaszcząc i poświęcając mu uwagę. 
tan kota (najedzenie, zadbanie, dostatek uwagi) 
ciągle powoli spada. W międzyczasie pojawią się 
drobne wydarzenia które lekko wpłyną na jego 
samopoczucie – pozytywnie lub negatywnie. Rzadziej 
pojawią się ważne wydarzenia które znacznie mocniej 
wpływają na kota (oprócz szwendania które w ogóle nie 
zmienia statystyk kota). Jakie wydarzenia jak wpływają 
na kota? Tego dowiesz się obserwując jego stan. 
By nie spotkała kota żadna zła przygoda możesz położyć 
go spać w czasie gdy nie możesz do niego zaglądać. 
Jednak jego statystyki opadają też gdy śpi."""
)




# wywołanie funkcji main (która jest wywoływana tylko gdy plik jest uruchamiany bezpośrednio)
if __name__ == "__main__":
    main()