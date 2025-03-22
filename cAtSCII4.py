import time #import mehanizmu czasu
import random #import mehanizmu losowego
import threading  # import mehanizmu wątków
import os  # bibioteka os do czyszczenia ekranu
import sys  # by zapisywaz zawartosc konsoli  TeeOutput:
from PIL import Image
import requests
from io import BytesIO
from duckduckgo_search import DDGS
import json  # Dodajemy import dla obsługi formatu JSON dla sejwowania
import requests #potrzebne do komunikacji z api llm

from links.nagrobek import nagrobek #import asci artow
from links.portret import portret #import asci arto
from links.ASCIIdrobne_wydarzenia import *
from links.ASCIIwazne_wydarzenia import *
from links.ASCIIinne import *
from links.api_key import api_key  #api key do llm
from links.prompty import *

from src.utils.ascii_converter import obraz_na_ascii, wyszukaj_i_konwertuj
from src.utils.logger import TeeOutput
from src.utils.help import HELP_TEXT
from src.utils.story_generator import generuj_historyjke, formatuj_do_wyswietlenia  #  import formatowania historyjek

from src.minor_events import drobne_wydarzenia
from src.major_events import wazne_wydarzenia

from src.cat import Cat

from src.switches import przelacznik1, set_switch_state

sys.stdout = TeeOutput('zawartosc.txt')



#**** ponizej glowna funkcja programu ---------------------------

def main():  # 
    
    global przelacznik1 #deklaracja uzycia

    # To się wykonuje RAZ na początku programu
    kot = Cat() # tutaj wywołuje się __init__
    if not os.path.exists('sejw.json'):  # Wyświetl portret tylko przy nowej grze
        print(portret)
        time.sleep(4)  # czeka x sekundy
        print("""
...i niby jest on normalnym kotkiem, ale w nocy wykrada
się i prowadzi inne życie. Jest członkiem ruchu oporu przeciwko psim 
imperialnym siłom. Zmutowane promieniowaniem psy chcą rzdzić podwórkami 
postapokaliptycznego Radomia 2050.

Gdy po zabraniu kota ze schroniska pierwszy raz wypuściłeś go na podwórko,
napadł go Burek, miejscowy złoczyńca. Ale z pomocą kotu przyszedł Jeż.
Odtąd Burek jest wrogiem kota a Jeż przyjacielem.\n""")

    def auto_sejw(kot):
        while True:
            time.sleep(20)  # co tyle sek jest zapis
            if kot.zyje():
                kot.zapisz_sejw()
    
    # Uruchamiamy wątek automatycznego zapisywania
    watek_sejwu = threading.Thread(target=auto_sejw, args=(kot,))
    watek_sejwu.daemon = True
    watek_sejwu.start()


    # Uruchom WĄTEK waznychwydarzeń losowych
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
            print("0 - Połóż kota spać i wyjdź")
        
        wybor = input("?: ") #wyswietla linie i zapisuje co wpisał użytkownik




        # Sprawdzenie wyboru użytkownika
        if wybor == "1":
            kot.karmienie()
            kot.zapisz_log("Akcja: Karmienie kota") #zapis logu
            print(wyszukaj_i_konwertuj("cat eat"))
            historyjka = generuj_historyjke("Napisz krótką, 1-zdaniową historyjkę po polsku, w drugiej osobie liczby pojedynczej, czas teraźniejszy, o tym jak właśnie nakarmiono kota. Zastanów się nad pokarmami jakie jada kot i wybierz jeden (wylosuj) . Nie używaj imion i ni wskazuj na płcie. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
            print(f"\n↑ {formatuj_do_wyswietlenia(historyjka)}") # wyswietla i lamie historyjke
            kot.zapisz_sejw()  # Save

        elif wybor == "2":
            kot.glaskanie()
            kot.zapisz_log("Akcja: Głaskanie kota") #zapis logu
            print(wyszukaj_i_konwertuj("petting cat"))
            historyjka = generuj_historyjke("Napisz krótką, 1-zdaniową historyjkę po polsku, w drugiej osobie liczby pojedynczej, czas teraźniejszy, o tym jak pogłaskano kota. Nie pisz że kot się wygina lub wibruje podczas głaskania. Nie używaj imion i nie wskazuj na płeć. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy. Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany.")
            print(f"\n↑ {formatuj_do_wyswietlenia(historyjka)}") # wyswietla i lamie historyjke
            kot.zapisz_sejw()  # Save


        elif wybor == "0":
            print("\nWyjście z gry")
            break

        elif wybor == "3":
            kot.patrzenie()
            kot.zapisz_log("Akcja: Patrzenie na kota") #zapis logu
            print(wyszukaj_i_konwertuj("cat portrait"))
            historyjka = generuj_historyjke("Napisz krótką, 1-zdaniową historyjkę po polsku, w drugiej osobie liczby pojedynczej, czas teraźniejszy, o tym jak nawiązano kontakt wzrokowy ze swoim kotem. Nie używaj imion i ni wskazuj na płcie. Niech historyjka nie będzie zbyt słodka i niech nie brzmi jak tekst z reklamy ale niech to będzie pozytywne. Nie używaj imion i nie wskazuj na płeć.  Nie zwracaj się w tekście bezpośrednio do czytającego, nie przełamuj czwartej ściany. Nie pisz że ktoś siedziałi sie patrzył w ścianę.")
            print(f"\n↑ {formatuj_do_wyswietlenia(historyjka)}") # wyswietla i lamie historyjke
            kot.zapisz_sejw()  # Save

        elif wybor == "4":            
            przelacznik1 = not przelacznik1  # zmienia wartość na przeciwną
            set_switch_state(przelacznik1)  # zapisujemy nowy stan do pliku
            print((random.choice(ASCIIzasypia))if przelacznik1 else wyszukaj_i_konwertuj("waking up cat"))# wybiera losowo aaciart gdy zasypia i sciaga z netu gdy wstaje
            print(f"Kot {'zasypia' if przelacznik1 else 'się budzi'}")
            kot.zapisz_log("Kot zasypia" if przelacznik1 else "Kot się budzi") #zapis logu

        elif wybor == "h":
            print(HELP_TEXT)
            kot.zapisz_sejw()  # Save

        #elif wybor == "d": #####DEBUG zakomanrtowany
             #kot.dobrostan_emo_up()  # Debug: test drobnego wydarzenia dobrostanu z printem calego promptu




# wywołanie funkcji main (która jest wywoływana tylko gdy plik jest uruchamiany bezpośrednio)
if __name__ == "__main__":
    main()


