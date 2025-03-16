import time #import mehanizmu czasu
import random #import mehanizmu losowego
import threading  # import mehanizmu wątków
import os  # bibioteka os do czyszczenia ekranu

from links.nagrobek import nagrobek #import asci artow
from links.portret import portret #import asci arto
from links.ASCIIdrobne_wydarzenia import *
from links.ASCIIwazne_wydarzenia import *
from links.ASCIIinne import *
import sys  # by zapisywaz zawartosc konsoli  TeeOutput:
from PIL import Image
import requests
from io import BytesIO
from duckduckgo_search import DDGS
import json  # Dodajemy import dla obsługi formatu JSON dla sejwowania

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


#**** ponizej funkcje z programu gasci (wyszukiwanie obrazow i zamienianie na ascii)***************

def obraz_na_ascii(sciezka_lub_url, szerokosc_wyjscia=100):
    """Konwertuje obraz na ASCII art. Obsługuje zarówno lokalne pliki jak i URL-e."""

    try:
        # Sprawdź czy to URL czy ścieżka lokalna
        if sciezka_lub_url.startswith(('http://', 'https://')):
            # Pobierz obraz z URL
            response = requests.get(sciezka_lub_url)
            obraz = Image.open(BytesIO(response.content)).convert('L')
        else:
            # Otwórz lokalny plik
            obraz = Image.open(sciezka_lub_url).convert('L') # Otwórz obraz i przekonwertuj na skalę szarości ('L')
    except Exception as e:
        return f"Błąd podczas otwierania obrazu: {str(e)}"

    szerokosc_obrazu, wysokosc_obrazu = obraz.size
    stosunek_aspektu = wysokosc_obrazu / szerokosc_obrazu
    wysokosc_wyjscia = int(szerokosc_wyjscia * stosunek_aspektu * 0.5) # Dostosowanie wysokości, 0.5 bo znaki nie są kwadratowe

    obraz = obraz.resize((szerokosc_wyjscia, wysokosc_wyjscia))
    piksele = obraz.getdata()

    znaki_ascii = [" ", ".", ",", "-", "+", "*", "#", "@"] # Im dalej w prawo, tym gęstszy znak
    dlugosc_znakow = len(znaki_ascii)

    ascii_art = ""
    for i in range(0, wysokosc_wyjscia):
        for j in range(0, szerokosc_wyjscia):
            piksel_index = i * szerokosc_wyjscia + j
            jasnosc_piksela = piksele[piksel_index]
            index_znaku = int(jasnosc_piksela / 255 * (dlugosc_znakow - 1)) # Mapowanie jasności na index znaku
            ascii_art += znaki_ascii[index_znaku]
        ascii_art += "\n" # Nowa linia po każdym rzędzie

    return ascii_art

def wyszukaj_i_konwertuj(zapytanie, max_wynikow=20):
    """Wyszukuje obrazy za pomocą DuckDuckGo, losuje jeden i konwertuje na ASCII art."""
    try:
        with DDGS() as ddgs:
            # Pobieramy więcej wyników, aby mieć większą pulę do losowania
            wyniki = list(ddgs.images(zapytanie, max_results=max_wynikow))
        
        if not wyniki:
            raise Exception("Nie znaleziono wyników")
        
        # Używamy miniatur zamiast pełnych obrazów (a nie jak to zakomentowane ponizej)
        url_obrazow = [wynik['thumbnail'] for wynik in wyniki]        

        # Wyciągnij URL-e obrazów z wyników
        #url_obrazow = [wynik['image'] for wynik in wyniki] #tu pobierane byly pelne obrazy
        
        # Losowo wybierz jeden obraz
        losowy_url = random.choice(url_obrazow)
        
        # Konwertuj na ASCII art
        return obraz_na_ascii(losowy_url)
    except Exception as e:
        print(f"Błąd podczas wyszukiwania obrazów: {str(e)}")
        print("Napotkano limit zapytań. Używanie alternatywnej metody...")
        
        # Alternatywna metoda - używamy przykładowego URL-a obrazu
        przykladowy_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
        
        # Konwertuj na ASCII art
        return obraz_na_ascii(przykladowy_url)

#******** koniec funcji z programu gasci (wyszukiwanie i zamienianie na asci)**********



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
            print("Wczytano stan kota:")
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
        print(wyszukaj_i_konwertuj("cat shits"))
        self.najedzenie = max(0, self.najedzenie - 2) 
 
    def upolowanie_myszy(self):
        print(wyszukaj_i_konwertuj("cat hunting mouse"))
        self.najedzenie = min(10, self.najedzenie + 2)
 
 
    def psia_inwazja(self):
        print(wyszukaj_i_konwertuj("aggressive dog"))
        self.zadbanie = max(0, self.zadbanie - 2) 

    def dzieci_głaszcza(self):
        print(wyszukaj_i_konwertuj("children cat"))
        self.zadbanie = min(10, self.zadbanie + 2)


    def smutek(self):
        print(wyszukaj_i_konwertuj("sad cat"))
        self.dostatekuwagi = max(0, self.dostatekuwagi - 2)

    def spotkanie_kocich_znajomych(self):
        print(wyszukaj_i_konwertuj("cats meeting"))
        self.dostatekuwagi = min(10, self.dostatekuwagi + 2)


    def szwedanie(self):
        print(wyszukaj_i_konwertuj("cat wandering"))
        pass  # ta metoda celowo nic nie robi



    # ponizej metody - drobne wydarzenia

    # zadbanie

    def przeciaganie(self):
        print(wyszukaj_i_konwertuj("cat stretching"))
        self.zadbanie = min(10, self.zadbanie + 0.25)  

    def upadek_z_krzesla(self):
        print(wyszukaj_i_konwertuj("cat fall"))
        self.zadbanie = max(0, self.zadbanie - 0.25)  

    def mruczenie(self):
        print(wyszukaj_i_konwertuj("cat purrs"))
        self.zadbanie = min(10, self.zadbanie + 0.25)  

    def kaslanie(self):
        print(wyszukaj_i_konwertuj("cat cough"))
        self.zadbanie = max(0, self.zadbanie - 0.25) 


    # najedzenie

    def upolowanie_muchy(self):
        print(wyszukaj_i_konwertuj("fly"))
        self.najedzenie = min(10, self.najedzenie + 0.25)  

    def gonitwa_po_meblach(self):
        print(wyszukaj_i_konwertuj("cat run"))
        self.najedzenie = max(0, self.najedzenie - 0.25) 

    def upolowanie_pajaka(self):
        print(wyszukaj_i_konwertuj("spider"))
        self.najedzenie = min(10, self.najedzenie + 0.25)  

    def wycieczka_na_dach(self):
        print(wyszukaj_i_konwertuj("cat roof"))
        self.najedzenie = max(0, self.najedzenie - 0.25) 


    # dostatekuwagi

    def wizyta_kota_sasiada(self):
        print(wyszukaj_i_konwertuj("2 cats"))
        self.dostatekuwagi = min(10, self.dostatekuwagi + 0.25)  

    def utkniecie_pod_zlewem(self):
        print(wyszukaj_i_konwertuj("sink"))
        self.dostatekuwagi = max(0, self.dostatekuwagi - 0.25) 

    def spotkanie_z_jezem(self):
        print(wyszukaj_i_konwertuj("hedgehog"))
        self.dostatekuwagi = min(10, self.dostatekuwagi + 0.25)  

    def koci_marazm(self):
        print(wyszukaj_i_konwertuj("lazy cat"))
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
    if not os.path.exists('sejw.json'):  # Wyświetl portret tylko przy nowej grze
        print(portret)
        time.sleep(4)  # czeka x sekundy


    def auto_sejw(kot):
        while True:
            time.sleep(60)  # Czekamy minutę
            if kot.zyje():
                kot.zapisz_sejw()
    
    # Uruchamiamy wątek automatycznego zapisywania
    watek_sejwu = threading.Thread(target=auto_sejw, args=(kot,))
    watek_sejwu.daemon = True
    watek_sejwu.start()


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
            print(wyszukaj_i_konwertuj("cat eat"))
            print("↑ Karmisz kota")

        elif wybor == "2":
            kot.glaskanie()
            kot.zapisz_log("Akcja: Głaskanie kota") #zapis logu
            print(wyszukaj_i_konwertuj("petting cat"))
            print("↑ Głaszczesz kota")


        elif wybor == "0":
            break

        elif wybor == "3":
            kot.patrzenie()
            kot.zapisz_log("Akcja: Patrzenie na kota") #zapis logu
            print(wyszukaj_i_konwertuj("cat portrait"))
            print("↑ Widzisz kota")

        elif wybor == "4":            
            przelacznik1 = not przelacznik1  # zmienia wartość na przeciwną
            print(wyszukaj_i_konwertuj("sleeping cat" if przelacznik1 else "waking up cat"))
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




