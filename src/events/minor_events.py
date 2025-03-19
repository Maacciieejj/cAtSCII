import time #import mehanizmu czasu
import random
from links.nagrobek import nagrobek #import asci artow




# ponizej definicja funkcji drobnych wydarzeń uruchamianej w wątku dodatkowym

def drobne_wydarzenia(kot): # definicja funkcji 
    global przelacznik1  # deklarujemy użycie zmiennej globalnej
    
    
    while True:
        if przelacznik1: # jeśli przełącznik włączony, czekamy w pierwszej pętli (sen)
            time.sleep(2)
            continue

        czas_oczekiwania = random.choice([120, 120, 120, 120, 120, 120, 60, 60, 60, 60, 180, 180, 300, 300])  # losuje czas oczekiwania w sekundach
        
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
        kot.zapisz_log(f"Drobne wydarzenie:{ wydarzenie}") # zapisuje log
        kot.pokaz_stan()
        print("(Menu: enter)")

